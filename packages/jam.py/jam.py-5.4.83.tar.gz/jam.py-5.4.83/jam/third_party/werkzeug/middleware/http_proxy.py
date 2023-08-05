"""
Basic HTTP Proxy
================

.. autoclass:: ProxyMiddleware

:copyright: 2007 Pallets
:license: BSD-3-Clause
"""
import socket

from ..datastructures import EnvironHeaders
from ..http import is_hop_by_hop_header
from ..urls import url_parse
from ..urls import url_quote
from ..wsgi import get_input_stream

try:
    from http import client
except ImportError:
    import httplib as client


class ProxyMiddleware(object):
    """Proxy requests under a path to an external server, routing other
    requests to the app.

    This middleware can only proxy HTTP requests, as that is the only
    protocol handled by the WSGI server. Other protocols, such as
    websocket requests, cannot be proxied at this layer. This should
    only be used for development, in production a real proxying server
    should be used.

    The middleware takes a dict that maps a path prefix to a dict
    describing the host to be proxied to::

        app = ProxyMiddleware(app, {
            "/static/": {
                "target": "http://127.0.0.1:5001/",
            }
        })

    Each host has the following options:

    ``target``:
        The target URL to dispatch to. This is required.
    ``remove_prefix``:
        Whether to remove the prefix from the URL before dispatching it
        to the target. The default is ``False``.
    ``host``:
        ``"<auto>"`` (default):
            The host header is automatically rewritten to the URL of the
            target.
        ``None``:
            The host header is unmodified from the client request.
        Any other value:
            The host header is overwritten with the value.
    ``headers``:
        A dictionary of headers to be sent with the request to the
        target. The default is ``{}``.
    ``ssl_context``:
        A :class:`ssl.SSLContext` defining how to verify requests if the
        target is HTTPS. The default is ``None``.

    In the example above, everything under ``"/static/"`` is proxied to
    the server on port 5001. The host header is rewritten to the target,
    and the ``"/static/"`` prefix is removed from the URLs.

    :param app: The WSGI application to wrap.
    :param targets: Proxy target configurations. See description above.
    :param chunk_size: Size of chunks to read from input stream and
        write to target.
    :param timeout: Seconds before an operation to a target fails.

    .. versionadded:: 0.14
    """

    def __init__(self, app, targets, chunk_size=2 << 13, timeout=10):
        def _set_defaults(opts):
            opts.setdefault("remove_prefix", False)
            opts.setdefault("host", "<auto>")
            opts.setdefault("headers", {})
            opts.setdefault("ssl_context", None)
            return opts

        self.app = app
        self.targets = dict(
            ("/%s/" % k.strip("/"), _set_defaults(v)) for k, v in targets.items()
        )
        self.chunk_size = chunk_size
        self.timeout = timeout

    def proxy_to(self, opts, path, prefix):
        target = url_parse(opts["target"])

        def application(environ, start_response):
            headers = list(EnvironHeaders(environ).items())
            headers[:] = [
                (k, v)
                for k, v in headers
                if not is_hop_by_hop_header(k)
                and k.lower() not in ("content-length", "host")
            ]
            headers.append(("Connection", "close"))

            if opts["host"] == "<auto>":
                headers.append(("Host", target.ascii_host))
            elif opts["host"] is None:
                headers.append(("Host", environ["HTTP_HOST"]))
            else:
                headers.append(("Host", opts["host"]))

            headers.extend(opts["headers"].items())
            remote_path = path

            if opts["remove_prefix"]:
                remote_path = "%s/%s" % (
                    target.path.rstrip("/"),
                    remote_path[len(prefix) :].lstrip("/"),
                )

            content_length = environ.get("CONTENT_LENGTH")
            chunked = False

            if content_length not in ("", None):
                headers.append(("Content-Length", content_length))
            elif content_length is not None:
                headers.append(("Transfer-Encoding", "chunked"))
                chunked = True

            try:
                if target.scheme == "http":
                    con = client.HTTPConnection(
                        target.ascii_host, target.port or 80, timeout=self.timeout
                    )
                elif target.scheme == "https":
                    con = client.HTTPSConnection(
                        target.ascii_host,
                        target.port or 443,
                        timeout=self.timeout,
                        context=opts["ssl_context"],
                    )
                else:
                    raise RuntimeError(
                        "Target scheme must be 'http' or 'https', got '{}'.".format(
                            target.scheme
                        )
                    )

                con.connect()
                remote_url = url_quote(remote_path)
                querystring = environ["QUERY_STRING"]

                if querystring:
                    remote_url = remote_url + "?" + querystring

                con.putrequest(environ["REQUEST_METHOD"], remote_url, skip_host=True)

                for k, v in headers:
                    if k.lower() == "connection":
                        v = "close"

                    con.putheader(k, v)

                con.endheaders()
                stream = get_input_stream(environ)

                while 1:
                    data = stream.read(self.chunk_size)

                    if not data:
                        break

                    if chunked:
                        con.send(b"%x\r\n%s\r\n" % (len(data), data))
                    else:
                        con.send(data)

                resp = con.getresponse()
            except socket.error:
                from ..exceptions import BadGateway

                return BadGateway()(environ, start_response)

            start_response(
                "%d %s" % (resp.status, resp.reason),
                [
                    (k.title(), v)
                    for k, v in resp.getheaders()
                    if not is_hop_by_hop_header(k)
                ],
            )

            def read():
                while 1:
                    try:
                        data = resp.read(self.chunk_size)
                    except socket.error:
                        break

                    if not data:
                        break

                    yield data

            return read()

        return application

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        app = self.app

        for prefix, opts in self.targets.items():
            if path.startswith(prefix):
                app = self.proxy_to(opts, path, prefix)
                break

        return app(environ, start_response)

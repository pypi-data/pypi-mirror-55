from aiohttp import BasicAuth, web


def handle_401():
    return web.Response(status=401, headers={"WWW-Authenticate": 'Basic realm="Access to staging site"'})


def parse_auth_header(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        auth = BasicAuth.decode(auth_header)
    except ValueError:
        auth = None
    return auth


def bam_factory(login, password):
    @web.middleware
    async def wrapper(request, handler):
        auth = parse_auth_header(request)
        if not (auth and auth.login == login and auth.password == password):
            return handle_401()

        resp = await handler(request)
        return resp

    return wrapper

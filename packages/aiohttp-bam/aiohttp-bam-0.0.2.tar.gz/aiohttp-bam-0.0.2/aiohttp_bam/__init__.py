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


def bam_factory(login, password, bypass_ws=False):
    """创建一个basic auth的middleware

    :param login: basic auth username
    :param password: basic auth password
    :param bypass_ws: 绕过websocket请求，默认为Flase，不绕过

    :return: A aiohttp middleware
    """
    @web.middleware
    async def wrapper(request, handler):
        if bypass_ws:
            connection = request.headers.get('Connection')
            if connection == 'Upgrade':
                return await handler(request)

        auth = parse_auth_header(request)
        if not (auth and auth.login == login and auth.password == password):
            return handle_401()

        return await handler(request)

    return wrapper

aiohttp basic auth middleware
===================================

HTTP basic authentication middleware for aiohttp.

Parameters
------------

def bam_factory(login, password, bypass_ws=False)
    创建一个basic auth的middleware

    :login: username
    :password: password
    :bypass_ws: 绕过websocket请求，默认为Flase，不绕过

Usage
--------

.. code-block:: py

    # server_simple.py
    from aiohttp import web
    from aiohttp_bam import bam_factory


    async def handle(request):
        return web.Response(text="Hello")


    app = web.Application(middlewares=[bam_factory('your username', 'your password')])
    app.add_routes([web.get("/", handle)])

    web.run_app(app)

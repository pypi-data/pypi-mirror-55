aiohttp basic auth middleware
===================================

HTTP basic authentication middleware for aiohttp.

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

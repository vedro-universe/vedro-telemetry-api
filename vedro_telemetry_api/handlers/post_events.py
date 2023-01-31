from http import HTTPStatus

from aiohttp.web import Request, Response, json_response

__all__ = ("post_events",)


async def post_events(request: Request) -> Response:
    payload = await request.json()
    print("payload", payload)
    return json_response(payload, status=HTTPStatus.OK)

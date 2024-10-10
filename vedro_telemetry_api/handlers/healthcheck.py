from http import HTTPStatus

from aiohttp.web import Request, Response, json_response

__all__ = ("healthcheck",)


async def healthcheck(request: Request) -> Response:
    """
    Perform a health check for the service.

    :param request: The HTTP request object (unused).
    :return: A JSON response with an HTTP 200 OK status.
    """
    return json_response({"status": "OK"}, status=HTTPStatus.OK)

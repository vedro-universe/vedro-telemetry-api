from http import HTTPStatus

from aiohttp.web import Request, Response, json_response
from aiohttp_valera_validator import validate

from ..app_keys import session_repo_key
from ..schemas import EventListSchema
from ._group_sessions import _group_sessions

__all__ = ("post_events",)


@validate(json=EventListSchema)
async def post_events(request: Request) -> Response:
    """
    Handle the POST request to save telemetry events.

    This asynchronous function processes telemetry events received in the request body,
    groups them by session, and saves them to the session repository. It returns a JSON
    response with the list of saved session IDs, or an error message if the operation
    fails.

    :param request: The HTTP request containing telemetry event data in JSON format.
    :return: A JSON response with the saved session IDs and an HTTP 200 OK status, or
             an error message with an HTTP 500 Internal Server Error status.
    """
    session_repo = request.app[session_repo_key]

    payload = await request.json()

    saved = []
    sessions = _group_sessions(payload)
    for session_id, session_info in sessions.items():
        try:
            await session_repo.save_session(session_info)
        except Exception as e:
            print("Error: ", type(e), e)
            return json_response({"errors": ["Internal server error"]},
                                 status=HTTPStatus.INTERNAL_SERVER_ERROR)
        saved.append(str(session_id))

    return json_response(saved, status=HTTPStatus.OK)

from http import HTTPStatus

from aiohttp.web import Request, Response, json_response
from aiohttp_valera_validator import validate

from ..repositories import SessionRepository
from ..schemas import EventListSchema
from ._group_sessions import _group_sessions

__all__ = ("post_events",)


@validate(json=EventListSchema)
async def post_events(request: Request) -> Response:
    session_repo: SessionRepository = request.app["session_repo"]

    payload = await request.json()

    sessions = _group_sessions(payload)
    for _, session in sessions.items():
        try:
            await session_repo.save_session(session)
        except Exception as e:
            print("Error: ", type(e), e)
            return json_response({"errors": ["Internal server error"]},
                                 status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return json_response({}, status=HTTPStatus.OK)

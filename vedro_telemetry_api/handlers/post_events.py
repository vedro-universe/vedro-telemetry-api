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

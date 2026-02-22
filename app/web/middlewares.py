import typing
import json
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from app.web.utils import error_json_response
from aiohttp_session import get_session
from marshmallow import ValidationError

if typing.TYPE_CHECKING:
    from app.web.app import Application

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request, handler):
    try:
        return await handler(request)
    except (HTTPUnprocessableEntity, ValidationError) as e:
        if isinstance(e, ValidationError):
            error_data = e.messages
        else:
            try:
                error_data = json.loads(e.text) if e.text else {}
            except:
                error_data = {}

        return error_json_response(
            http_status=400,
            status="bad_request",
            message="Unprocessable Entity",
            data={"json": error_data}
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES.get(e.status, "unknown_error"),
            message=str(e.reason),
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status="internal_server_error",
            message=str(e),
        )


@middleware
async def auth_middleware(request, handler):
    request.admin = None
    session = await get_session(request)

    if session.get("admin"):
        email = session["admin"]["email"]
        admin = await request.app.store.admins.get_by_email(email)
        request.admin = admin

    return await handler(request)

def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(auth_middleware)
    app.middlewares.append(validation_middleware)
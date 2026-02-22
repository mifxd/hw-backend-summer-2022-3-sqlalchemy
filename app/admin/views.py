from aiohttp_session import new_session, get_session
from aiohttp_apispec import request_schema
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response, error_json_response


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        payload = AdminSchema().load(data)

        email = payload["email"]
        password = payload["password"]

        admin = await self.store.admins.get_by_email(email)
        if not admin or not admin.is_password_valid(password):
            return error_json_response(
                http_status=403,
                status="forbidden",
                message="Invalid credentials"
            )

        session = await new_session(self.request)
        admin_data = {"id": admin.id, "email": email}
        session["admin"] = admin_data

        return json_response(data=admin_data)


class AdminCurrentView(View):
    async def get(self):
        admin = self.request.admin

        if not admin:
            return error_json_response(
                http_status=401,
                status="unauthorized",
                message="Not authorized"
            )

        return json_response(data={
            "id": admin.id,
            "email": admin.email
        })
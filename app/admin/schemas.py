from pydantic import BaseModel
from app.db.models import UserRole


class RoleUpdateRequest(BaseModel):
    role: UserRole

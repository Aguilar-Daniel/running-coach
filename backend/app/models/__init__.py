from app.models.user import User
from app.models.profile import Profile

__all__ = ["User", "Profile"] #Used in case from app.models import * is done.If it is done, then only the imports in __all__ would get imported not EVERY one
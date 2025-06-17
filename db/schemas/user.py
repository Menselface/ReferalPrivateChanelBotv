from pydantic import BaseModel
from typing import Optional

class UserCreateDTO(BaseModel):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str]
    ref_token: Optional[str]
from typing import Dict, List, Optional

from pydantic import BaseModel, root_validator

# Response Model(s)

class RegenerateNamesAPIResponse(BaseModel):
    """Level regeneration response model"""

    status_code: int
    error: Optional[bool]
    message: Optional[str] = ""
    data: Optional[dict] = {}

    # work around (waiting on https://github.com/samuelcolvin/pydantic/pull/2625)
    @root_validator
    def compute_error(cls, values) -> Dict:
        error = False if values.get("status_code") < 400 else True

        values["error"] = error
        return values

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "error": False,
                "message": "Success",
                "data": {},
            }
        }

class NameData(BaseModel):
    name: str
    email: str
    role: str

    class Config:
        schema_extra = {
                "name": "John Doe",
                "email": "johndoe@gmail.com",
                "role": "customer",
            }
        

class SearchAPIResponse(BaseModel):
    """Level regeneration response model"""

    status_code: int
    error: Optional[bool]
    message: Optional[str] = ""
    data: Optional[List[NameData]] = []

    # work around (waiting on https://github.com/samuelcolvin/pydantic/pull/2625)
    @root_validator
    def compute_error(cls, values) -> Dict:
        error = False if values.get("status_code") < 400 else True

        values["error"] = error
        return values

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "error": False,
                "message": "Success",
                "data": [],
            }
        }
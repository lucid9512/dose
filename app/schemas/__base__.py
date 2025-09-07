import re
from typing import Any, Dict
from pydantic import BaseModel

# -------------------
# util functions
# -------------------
def to_camel(string: str) -> str:
    """snake_case → camelCase"""
    if string == "root":
        return string
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])

def to_snake(string: str) -> str:
    """camelCase → snake_case"""
    if string == "root":
        return string
    first_underscore = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", first_underscore).lower()

def keys_to_snake_case(data: Dict[str, Any]) -> Dict[str, Any]:
    return {to_snake(k): v for k, v in data.items()}

def keys_to_camel_case(data: Dict[str, Any]) -> Dict[str, Any]:
    return {to_camel(k): v for k, v in data.items()}

# -------------------
# Base Request Model
# -------------------
class VaModelReq(BaseModel):
    """
    camelCase → snake_case 변환해서 내부에서 사용
    """
    class Config:
        alias_generator = to_camel   # snake → camel alias 자동 생성
        populate_by_name = True      # snake_case 입력도 허용
        from_attributes = True
        arbitrary_types_allowed = True


# -------------------
# Base Response Model
# -------------------
class VaModelRes(BaseModel):
    """
    snake_case 모델을 camelCase로 응답 변환
    """
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True

    def resp(self) -> Dict[str, Any]:
        return self.dict(by_alias=True, exclude_none=True)

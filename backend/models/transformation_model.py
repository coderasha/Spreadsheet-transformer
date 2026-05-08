from pydantic import BaseModel


class TransformationRequest(BaseModel):
    column_name: str
    operation: str
from pydantic import BaseModel


class ExpressionInput(BaseModel):
    expression: str
    variables: dict

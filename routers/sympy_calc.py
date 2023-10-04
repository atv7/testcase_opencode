from fastapi import APIRouter
from models import ExpressionInput
import sympy

router = APIRouter(
    prefix="/sympy_calc",
    tags=["sympy_calc"],
    responses={401: {"description": "not found"}}
)


def calculate_expression(expression_str, variables):
    try:
        expression = sympy.sympify(expression_str)
    except sympy.SympifyError:
        raise ValueError("Неверное выражение")

    for var_name, var_value in variables.items():
        var = sympy.symbols(var_name)
        expression = expression.subs(var, var_value)

    try:
        result = float(expression)
        return result
    except ValueError:
        raise ValueError("Результат не может быть вычислен")

@router.post("/sympy_culc/")
async def calculate(expression_input: ExpressionInput):
    expression = expression_input.expression
    variables = expression_input.variables

    try:
        result = calculate_expression(expression, variables)
        return {"result": result}
    except ValueError as e:
        return {"result": None, "error": str(e)}
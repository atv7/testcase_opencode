from fastapi import APIRouter
from models import ExpressionInput
import math

router = APIRouter(
    prefix="/rpn_calc",
    tags=["rpn_calc"],
    responses={401: {"description": "not found"}}
)


def rpn(expression):
    """Алгоритм для вычисления формулы в обратной польской записи с использованием стека"""
    lex = parse(expression)
    s2 = []
    r = []
    operators = ["+", "-", "*", "/", "(", ")", "^", "lg", "ln", "sin", "cos", "tan", "asin", "acos", "atan"]
    for a in lex:
        if a == "(":
            s2 = [a] + s2
        elif a in operators:
            if not s2:
                s2 = [a]
            elif a == ")":
                while True:
                    q = s2[0]
                    s2 = s2[1:]
                    if q == "(":
                        break
                    r += [q]
            elif priority(s2[0]) < priority(a):
                s2 = [a] + s2
            else:
                while True:
                    if not s2:
                        break
                    q = s2[0]
                    if priority(q) < priority(a):
                        break
                    r += [q]
                    s2 = s2[1:]
                s2 = [a] + s2
        else:
            r += [a]
    while s2:
        q = s2[0]
        r += [q]
        s2 = s2[1:]
    return r


def priority(operation):
    if operation in ["+", "-"]:
        return 1
    elif operation in ["*", "/", "sin", "cos", "tan", "asin", "acos", "atan"]:
        return 2
    elif operation in ["^", "lg", "ln"]:
        return 3
    elif operation == "(":
        return 0


def parse(expression):
    operators = ["+", "-", "*", "/", "(", ")", "^", "lg", "ln", "sin", "cos", "tan", "asin", "acos", "atan"]
    lex = []
    tmp = ""
    i = 0
    while i < len(expression):
        a = expression[i]
        if a != " ":
            if a in operators:
                if tmp != "":
                    lex += [tmp]
                if a == "^" and (i + 1 < len(expression) and expression[i + 1] == "-"):
                    lex += ["^"]
                    i += 1
                else:
                    lex += [a]
                tmp = ""
            else:
                tmp += a
        i += 1
    if tmp != "":
        lex += [tmp]
    return lex


def rpn_calc(formula, values):
    list_of_values = []
    alpha_names = []
    for lex in formula:
        if lex[0].isalpha():
            if lex in ["lg", "ln", "sin", "cos", "tan", "asin", "acos", "atan"]:
                continue
            try:
                if lex[0] not in values.keys():
                    alpha_names.append(formula[formula.index(lex[0])])
                formula[formula.index(lex[0])] = str(values.get(lex[0]))
            except ValueError:
                raise ValueError('Неверное выражение')
    for lex in formula:
        if lex in ["lg", "ln", "sin", "cos", "tan", "asin", "acos", "atan"]:
            list_of_values.append(lex)
        if lex[0].isdigit():
            list_of_values.append(float(lex))
        elif lex == 'None':
            raise TypeError(f"Не хватает переменной {alpha_names}")
        elif lex in ["+", "-", "*", "/", "^", "lg", "ln", "sin", "cos", "tan", "asin", "acos", "atan"]:
            a2 = list_of_values.pop()
            a1 = list_of_values.pop()
            match lex:
                case '+':
                    list_of_values.append(a1 + a2)
                case '-':
                    list_of_values.append(a1 - a2)
                case '*':
                    list_of_values.append(a1 * a2)
                case '/':
                    list_of_values.append(a1 / a2)
                case '^':
                    list_of_values.append(math.pow(a1, a2))
                case 'lg':
                    list_of_values.append(math.log10(a1))
                case 'ln':
                    list_of_values.append(math.log(a1))
                case 'sin':
                    list_of_values.append(math.sin(a1))
                case 'cos':
                    list_of_values.append(math.cos(a1))
                case 'tan':
                    list_of_values.append(math.tan(a1))
                case 'asin':
                    list_of_values.append(math.asin(a1))
                case 'acos':
                    list_of_values.append(math.acos(a1))
                case 'atan':
                    list_of_values.append(math.atan(a1))

    return list_of_values.pop()


@router.post("/")
async def calculate_expression(expression_input: ExpressionInput):
    expression = expression_input.expression
    variables = expression_input.variables

    try:
        result = rpn_calc(rpn(expression), variables)
        return {"result": result}
    except ValueError as e:
        return {"result": None, "error": str(e)}
    except TypeError as e:
        return {"result": None, "error": str(e)}

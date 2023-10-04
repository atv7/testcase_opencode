from fastapi import FastAPI
from routers import rpn_calc, sympy_calc

app = FastAPI()


@app.get('/')
async def root():
    return {"status_code": 200, "description":
        "/rpn_calc - калькулятор с использованием алгоритма обратной польской записи"
        "/sympy_calc - калькулятор с использованием библиотеки sympy"}

app.include_router(rpn_calc.router)
app.include_router(sympy_calc.router)

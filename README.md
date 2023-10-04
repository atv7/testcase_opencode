# Калькулятор

Создайте веб-сервис для вычисления алгебраических выражений. Сервис принимает запросы вида:

```json
{
  "expression": "4-2*a/(5*x-3)",
  "variables": {
    "a": 2.5,
    "x": 0
  }
}
}
```
ответ:
```json
{
"result": 3.8333333333333335
}
```
Или запрос:
```json
{
"expression": "4-2*a/(5*x-3)",
"variables": {
"a": 2.5
}
}
```
Ответ:
```json
{
"result": null,
"error": "Требуемая переменная x не определена"
}
```
В выражении допустимы числа, имена переменных, знаки арифметических действий,
возведение в степень (в том числе нецелую) ^, функции lg (десятичный логарифм), ln
(натуральный логарифм), тригонометрические функции sin, cos, tan, asin, acos, atan.
Требуется корректно (и, желательно, информативно) возвращать ошибки, если они
случились.

#Инструкция по запуску
  -Создать виртуальное окружение
  -Установить зависимости из файла requirements.txt
  -Запустить веб сервис через команду:
  ```
  uvicorn main:app --host 127.0.0.1 --port 8000 --reload
  ```


##Для отправки POST-запросов используйте следующие URL-адреса:

 -/rpn_calc для вычислений в обратной польской записи.
 -/sympy_calc для вычислений с использованием библиотеки SymPy.

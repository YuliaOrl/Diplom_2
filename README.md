## :green_book: Дипломный проект. Задание 2: API тесты

### Автотесты для проверки программы заказа бургеров в Stellar Burgers

### :computer: Использованный стек технологий

* Pytest
* Requests
* Allure

### :pushpin: Реализованные сценарии

Созданы API тесты для эндпоинтов: `.../auth/register`, `.../auth/login`, `.../auth/user`, `.../orders`
, `.../ingredients`.

### :books: Структура проекта

- `Diplom_2` - проект, содержащий тесты и вспомогательные файлы.
- `tests` - пакет, содержащий тесты, разделенные по классам: `test_create_user.py`, `test_login_user.py`
  , `test_update_user.py`, `test_create_order.py`, `test_get_orders.py`.

### :running: Запуск автотестов

**Установка зависимостей**

> `$ pip install -r requirements.txt`

**Запуск автотестов из корня проекта `Diplom_2` и создание HTML-отчета в Allure**

> `pytest tests\ --alluredir=allure_results`
> `allure serve allure_results`

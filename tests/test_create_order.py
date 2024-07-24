import pytest
import allure
import requests
from data import *
from helpers import *


class TestCreateOrder:

    @classmethod
    def setup_class(cls):
        cls.user = register_new_user_and_return_email_password()
        cls.payload = {
            'email': cls.user[0],
            'password': cls.user[1],
            'name': cls.user[2]
        }
        login_response = requests.post(LOGIN_URL, data=cls.payload)
        cls.user_token = login_response.json()['accessToken']

    @allure.title('Позитивная проверка создания заказа с ингредиентами и авторизацией')
    @allure.description('Проверяется статус код 200 и тело ответа')
    def test_create_order_with_authorization_true(self):
        order_data = {
            'ingredients': set_ingredients_for_order(4)
        }
        r = requests.post(ORDERS_URL, headers={'Authorization': self.user_token}, data=order_data)
        assert r.status_code == 200 and r.json()['success'] == True and 'бургер' in r.json()['name'] \
               and r.json()['order']['number']

    @allure.title('Позитивная проверка создания заказа с ингредиентами без авторизации')
    @allure.description('Проверяется статус код 200 и тело ответа')
    def test_create_order_without_authorization_true(self):
        order_data = {
            'ingredients': set_ingredients_for_order(4)
        }
        r = requests.post(ORDERS_URL, data=order_data)
        assert r.status_code == 200 and r.json()['success'] == True and 'бургер' in r.json()['name'] \
               and r.json()['order']['number']

    data_auth = [[[], 400, ERROR_EXPECTED_MESSAGE_400],
                 [[generate_random_string(24), generate_random_string(24)], 500, ERROR_EXPECTED_MESSAGE_500]]

    @allure.title('Негативная проверка создания заказа без ингредиентов или c невалидным хешем с авторизацией')
    @allure.description('Проверяется статус код и тело ответа c ошибкой')
    @pytest.mark.parametrize('ingredients, code, expected_message', data_auth)
    def test_create_order_incorrect_ingredients_with_authorization(self, ingredients, code, expected_message):
        order_data = {
            'ingredients': ingredients
        }
        r = requests.post(ORDERS_URL, headers={'Authorization': self.user_token}, data=order_data)
        assert r.status_code == code and expected_message in r.text

    data = [[[], 400, ERROR_EXPECTED_MESSAGE_400],
            [[generate_random_string(24), generate_random_string(24)], 500, ERROR_EXPECTED_MESSAGE_500]]

    @allure.title('Негативная проверка создания заказа без ингредиентов или c невалидным хешем без авторизации')
    @allure.description('Проверяется статус код и тело ответа c ошибкой')
    @pytest.mark.parametrize('ingredients, code, expected_message', data)
    def test_create_order_incorrect_ingredients_without_authorization(self, ingredients, code, expected_message):
        order_data = {
            'ingredients': ingredients
        }
        r = requests.post(ORDERS_URL, data=order_data)
        assert r.status_code == code and expected_message in r.text

    @classmethod
    def teardown_class(cls):
        requests.delete(USER_URL, headers={'Authorization': cls.user_token})

import pytest
import allure
import requests
from data import *
from helpers import *


class TestGetOrders:

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

    @allure.title('Позитивная проверка получения заказов пользователя с авторизацией')
    @allure.description('Проверяется статус код 200 и тело ответа с данными заказа')
    def test_user_orders_true(self):
        order_data = {
            'ingredients': set_ingredients_for_order(5)
        }
        requests.post(ORDERS_URL, headers={'Authorization': self.user_token}, data=order_data)
        r = requests.get(ORDERS_URL, headers={'Authorization': self.user_token})
        assert r.status_code == 200 and r.json()['success'] == True and \
               r.json()['orders'][0]['ingredients'] == order_data['ingredients']

    @allure.title('Негативная проверка получения заказов пользователя без авторизации')
    @allure.description('Проверяется статус код 401 и тело ответа с сообщением "You should be authorised"')
    def test_user_orders_without_authorization(self):
        r = requests.get(ORDERS_URL)
        assert r.status_code == 401 and r.json() == AUTHORIZATION_EXPECTED_MESSAGE_401

    @classmethod
    def teardown_class(cls):
        requests.delete(USER_URL, headers={'Authorization': cls.user_token})

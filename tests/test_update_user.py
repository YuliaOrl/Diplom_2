import pytest
import allure
import requests
from data import *
from helpers import *


class TestUpdateUser:

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

    @allure.title('Позитивная проверка изменения данных пользователя с авторизацией')
    @allure.description('Проверяется статус код 200 и тело ответа c измененными данными пользователя')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_update_user_true(self, field):
        payload = {
            'email': self.user[0],
            'password': self.user[1],
            'name': self.user[2]
        }
        payload[field] = payload[field].replace(payload[field][0:6], generate_random_string(6))
        r = requests.patch(USER_URL, headers={'Authorization': self.user_token}, data=payload)
        assert r.status_code == 200 and r.json()['success'] == True and r.json()['user']['email'] == payload['email'] \
               and r.json()['user']['name'] == payload['name']

    @allure.title('Негативная проверка изменения данных пользователя без авторизации')
    @allure.description('Проверяется статус код 401 и тело ответа с сообщением "You should be authorised"')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_update_user_without_authorization(self, field):
        payload = {
            'email': self.user[0],
            'password': self.user[1],
            'name': self.user[2]
        }
        payload[field] = payload[field].replace(payload[field][0:6], generate_random_string(6))
        r = requests.patch(USER_URL, data=payload)
        assert r.status_code == 401 and r.json() == AUTHORIZATION_EXPECTED_MESSAGE_401

    @classmethod
    def teardown_class(cls):
        requests.delete(USER_URL, headers={'Authorization': cls.user_token})

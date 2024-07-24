import pytest
import allure
import requests
from data import *
from helpers import *


class TestLoginUser:

    @classmethod
    def setup_class(cls):
        cls.user = register_new_user_and_return_email_password()
        cls.payload = {
            'email': cls.user[0],
            'password': cls.user[1],
            'name': cls.user[2]
        }

    @allure.title('Позитивная проверка авторизации пользователя с корректными данными')
    @allure.description('Проверяется статус код 200 и тело ответа c данными пользователя')
    def test_login_user_true(self):
        r = requests.post(LOGIN_URL, data=self.payload)
        assert r.status_code == 200 and r.json()['success'] == True and r.json()['accessToken'] \
               and r.json()['refreshToken'] and r.json()['user']['email'] == self.payload['email'] \
               and r.json()['user']['name'] == self.payload['name']

    @allure.title('Негативная проверка авторизации пользователя с неверными данными')
    @allure.description('Проверяется статус код 401 и тело ответа с сообщением "email or password are incorrect"')
    @pytest.mark.parametrize('field', ['email', 'password'])
    def test_login_user_with_incorrect_email_or_password(self, field):
        payload = {
            'email': self.user[0],
            'password': self.user[1]
        }
        payload[field] = payload[field][1:]
        r = requests.post(LOGIN_URL, data=payload)
        assert r.status_code == 401 and r.json() == LOGIN_EXPECTED_MESSAGE_401

    @classmethod
    def teardown_class(cls):
        login_response = requests.post(LOGIN_URL, data=cls.payload)
        user_token = login_response.json()['accessToken']
        requests.delete(USER_URL, headers={'Authorization': user_token})

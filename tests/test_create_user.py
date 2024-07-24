import pytest
import allure
import requests
from data import *
from helpers import *


class TestCreateUser:

    @allure.title('Позитивная проверка создания нового пользователя с корректными данными')
    @allure.description('Проверяется статус код 200 и тело ответа c данными пользователя')
    def test_create_user_true(self):
        payload = generate_random_payload()
        r = requests.post(REGISTER_URL, data=payload)
        assert r.status_code == 200 and r.json()['success'] == True and r.json()['user']['email'] == payload['email'] \
               and r.json()['user']['name'] == payload['name']

    @allure.title('Негативная проверка создания пользователя с зарегестрированным email')
    @allure.description('Проверяется статус код 403 и тело ответа c сообщением "User already exists"')
    def test_create_user_once(self):
        payload = generate_random_payload()
        requests.post(REGISTER_URL, data=payload)
        r = requests.post(REGISTER_URL, data=payload)
        assert r.status_code == 403 and r.json() == CREATE_EXPECTED_MESSAGE_403

    @allure.title('Проверка обязательных полей при создании пользователя')
    @allure.description('Проверяется возвращение ошибки 403 при отсутствии обязательного поля в запросе')
    @pytest.mark.parametrize('required_field', ['email', 'password', 'name'])
    def test_create_courier_without_required_field(self, required_field):
        payload = generate_random_payload()
        del payload[required_field]
        r = requests.post(REGISTER_URL, data=payload)
        assert r.status_code == 403 and r.json() == CREATE_REQUIRED_EXPECTED_MESSAGE_403

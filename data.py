MAIN_URL = 'https://stellarburgers.nomoreparties.site/api'
REGISTER_URL = MAIN_URL + '/auth/register'
LOGIN_URL = MAIN_URL + '/auth/login'
USER_URL = MAIN_URL + '/auth/user'
ORDERS_URL = MAIN_URL + '/orders'
INGREDIENTS_URL = MAIN_URL + '/ingredients'

CREATE_EXPECTED_MESSAGE_403 = {'success': False, 'message': 'User already exists'}
CREATE_REQUIRED_EXPECTED_MESSAGE_403 = {'success': False, 'message': 'Email, password and name are required fields'}
LOGIN_EXPECTED_MESSAGE_401 = {'success': False, 'message': 'email or password are incorrect'}
AUTHORIZATION_EXPECTED_MESSAGE_401 = {'success': False, 'message': 'You should be authorised'}
ERROR_EXPECTED_MESSAGE_400 = '{"success":false,"message":"Ingredient ids must be provided"}'
ERROR_EXPECTED_MESSAGE_500 = 'Internal Server Error'

import os
from typing import Callable
from unittest import mock

from src.hyperplane.secret_utils import get_secret


def test_get_secret_when_running_local_and_secret_env_var_is_set_return_secret():
    secret_key = "a_secret_name"
    expected_secret_value = "secret_value"
    with mock.patch.dict(os.environ, {f"HYPERPLANE_SECRET_{secret_key}": expected_secret_value}, clear=True):
        actual_secret_value = get_secret(secret_key)

        assert actual_secret_value == expected_secret_value


def mock_get_secret_by_user_token(expected_secret_value: str) -> Callable[[str, str], str]:
    def inner(secret_name, user_token):
        return expected_secret_value

    return inner


def test_get_secret_when_running_local_and_user_token_env_var_is_set_return_secret():
    secret_key = "a_secret_name"
    expected_secret_value = "secret_value"
    user_token = "user_token"
    with mock.patch.dict(os.environ, {"HYPERPLANE_USER_TOKEN": user_token}, clear=True):
        with mock.patch('hyperplane_server_utils.get_secret_by_user_token', mock_get_secret_by_user_token(expected_secret_value)):
            actual_secret_value = get_secret(secret_key)

            assert actual_secret_value == expected_secret_value

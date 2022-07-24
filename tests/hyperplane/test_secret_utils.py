import os
from unittest import mock

import pytest
from src.hyperplane.secret_utils import get_secret


def test_get_secret_when_running_local_and_env_var_is_not_set_then_raise():
    with pytest.raises(ValueError):
        get_secret("UNSET_ENV_VAR")


def test_get_secret_when_running_local_and_env_var_is_set_return_it():
    secret_key = "ENV_VAR_IS_SET"
    expected_secret_value = "is_set"
    with mock.patch.dict(os.environ, {secret_key: expected_secret_value}, clear=True):
        actual_secret_value = get_secret(secret_key)

        assert actual_secret_value == expected_secret_value

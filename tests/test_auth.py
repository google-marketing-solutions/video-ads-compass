# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test file for the auth module."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, g-importing-member, g-import-not-at-top

import sys

sys.path.append('.')
from unittest.mock import MagicMock

from google.oauth2.credentials import Credentials

from utils.auth import _get_credentials


def test_get_credentials_valid(monkeypatch):
    """Tests the get_credentials function with valid credentials.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    mock_config = {
        'client_id': 'test_client_id',
        'refresh_token': 'test_refresh_token',
        'client_secret': 'test_client_secret',
    }
    mock_creds = MagicMock(spec=Credentials)
    mock_creds.expired = False
    monkeypatch.setattr(
        'utils.auth.Credentials.from_authorized_user_info',
        MagicMock(return_value=mock_creds),
    )

    creds = _get_credentials(mock_config)
    assert creds is not None
    assert isinstance(creds, Credentials)


def test_get_credentials_invalid(monkeypatch):
    """Tests the get_credentials function with invalid credentials.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    mock_config = {
        'client_id': 'test_client_id',
        'refresh_token': 'test_refresh_token',
        'client_secret': 'test_client_secret',
    }
    mock_creds = MagicMock(spec=Credentials)
    mock_creds.expired = True
    mock_creds.refresh.side_effect = Exception('invalid_scope')
    monkeypatch.setattr(
        'utils.auth.Credentials.from_authorized_user_info',
        MagicMock(return_value=mock_creds),
    )

    creds = _get_credentials(mock_config)
    assert creds is not None
    assert isinstance(creds, Credentials)

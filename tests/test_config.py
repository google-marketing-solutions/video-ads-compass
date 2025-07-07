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

"""Test file for the config module."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, g-importing-member, g-explicit-bool-comparison, g-import-not-at-top

import sys

sys.path.append('.')
from unittest.mock import MagicMock

from utils.config import Config


def test_config_initialization_default(monkeypatch):
    """Tests the Config class initialization with default values.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    monkeypatch.setattr(
        'utils.config.Config.load_config_from_file', MagicMock(return_value={})
    )

    config = Config()

    assert config.client_id == ''
    assert config.client_secret is None
    assert config.refresh_token == ''
    assert config.ai_api_key == ''
    assert config.project_id == ''
    assert config.bucket_name == ''
    assert config.location == ''
    assert config.model == ''


def test_config_initialization_from_file(monkeypatch):
    """Tests the Config class initialization with values from a file.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    mock_config = {
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'refresh_token': 'test_refresh_token',
        'ai_api_key': 'test_ai_api_key',
        'project_id': 'test_project_id',
        'bucket_name': 'test_bucket_name',
        'location': 'test_location',
        'model': 'test_model',
    }
    monkeypatch.setattr(
        'utils.config.Config.load_config_from_file',
        MagicMock(return_value=mock_config),
    )

    config = Config()

    assert config.client_id == 'test_client_id'
    assert config.client_secret == 'test_client_secret'
    assert config.refresh_token == 'test_refresh_token'
    assert config.ai_api_key == 'test_ai_api_key'
    assert config.project_id == 'test_project_id'
    assert config.bucket_name == 'test_bucket_name'
    assert config.location == 'test_location'
    assert config.model == 'test_model'


def test_config_credentials_valid(monkeypatch):
    """Tests the credentials property with valid credentials.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    mock_creds = MagicMock()
    monkeypatch.setattr(
        'utils.config.auth._get_credentials', MagicMock(return_value=mock_creds)
    )

    config = Config()

    assert config.credentials == mock_creds


def test_config_credentials_invalid(monkeypatch):
    """Tests the credentials property with invalid credentials.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    monkeypatch.setattr(
        'utils.config.auth._get_credentials', MagicMock(return_value=None)
    )

    config = Config()

    assert config.credentials is None

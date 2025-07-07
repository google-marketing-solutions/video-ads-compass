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

"""Test file for the sheets module."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, g-importing-member, g-import-not-at-top

import sys

sys.path.append('.')
from unittest.mock import MagicMock

import pandas as pd
import pytest

from utils.config import Config
from utils.sheets import GoogleSheetsHandler


class TestConfig(Config):
    def __init__(self):
        self.bucket_name = 'test_bucket'


@pytest.fixture
def test_config(monkeypatch):
    """Mocks the configuration object for testing."""
    mock_creds = MagicMock()
    monkeypatch.setattr(
        'utils.config.auth._get_credentials', MagicMock(return_value=mock_creds)
    )
    return TestConfig()


def test_create_spreadsheet(monkeypatch, mock_config):
    """Tests the create_spreadsheet method.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        mock_config: Mock configuration object.
    """
    mock_gc = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_gc.create.return_value = mock_spreadsheet
    monkeypatch.setattr(
        'utils.sheets.gspread.Client', MagicMock(return_value=mock_gc)
    )

    sheets_handler = GoogleSheetsHandler(mock_config)

    spreadsheet = sheets_handler.create_spreadsheet()

    assert spreadsheet is not None


def test_upload_dataframe(monkeypatch, mock_config):
    """Tests the upload_dataframe method.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        mock_config: Mock configuration object.
    """
    mock_gc = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_worksheet = MagicMock()
    mock_spreadsheet.sheet1 = mock_worksheet
    mock_gc.create.return_value = mock_spreadsheet
    monkeypatch.setattr(
        'utils.sheets.gspread.Client', MagicMock(return_value=mock_gc)
    )

    sheets_handler = GoogleSheetsHandler(mock_config)

    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data)

    sheets_handler.upload_dataframe(mock_spreadsheet, df)

    expected_data = [['col1', 'col2'], [1, 3], [2, 4]]
    mock_worksheet.update.assert_called_once_with(expected_data)


def test_format_spreadsheet(monkeypatch, mock_config):
    """Tests the format_spreadsheet method.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        mock_config: Mock configuration object.
    """
    mock_gc = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_worksheet = MagicMock()
    mock_spreadsheet.sheet1 = mock_worksheet
    mock_gc.create.return_value = mock_spreadsheet
    monkeypatch.setattr(
        'utils.sheets.gspread.Client', MagicMock(return_value=mock_gc)
    )
    mock_worksheet.get_all_records.return_value = []

    sheets_handler = GoogleSheetsHandler(mock_config)

    sheets_handler.format_spreadsheet(mock_spreadsheet)

    assert mock_worksheet.format.call_count > 0

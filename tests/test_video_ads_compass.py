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

"""Tests for the Video Ads Compass application."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, g-importing-member, g-import-not-at-top

import sys

sys.path.append('.')
from unittest.mock import MagicMock

import pandas as pd
import pytest

from utils.config import Config
from video_ads_compass import (
    download_and_list_video_files_gcs,
    main,
    process_videos_and_create_df,
)


class MockConfig(Config):
    def __init__(self):
        self.bucket_name = 'test_bucket'


@pytest.fixture
def mock_config(monkeypatch):
    """Mocks the configuration object for testing.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    Returns:
        MockConfig: A mock configuration object.
    """
    mock_creds = MagicMock()
    monkeypatch.setattr(
        'utils.config.auth.get_credentials', MagicMock(return_value=mock_creds)
    )
    return MockConfig()


def test_download_and_list_video_files_gcs(monkeypatch, test_config):
    """Tests the download_and_list_video_files_gcs function.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        test_config: A mock configuration object.
    """
    mock_client = MagicMock()
    mock_blob = MagicMock()
    mock_blob.name = 'test_video.mp4'
    mock_client.list_blobs.return_value = [mock_blob]
    monkeypatch.setattr(
        'video_ads_compass.storage.Client', MagicMock(return_value=mock_client)
    )

    video_files = download_and_list_video_files_gcs(test_config)
    assert len(video_files) == 1
    assert 'test_video.mp4' in video_files[0]


def test_process_videos_and_create_df(monkeypatch, test_config):
    """Tests the process_videos_and_create_df function.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        test_config: A mock configuration object.
    """
    mock_vertex_ai_handler = MagicMock()
    mock_vertex_ai_handler.analyze_video.return_value = (
        '{"rules": [], "overall_compliance_assessment": "Compliant"}'
    )
    monkeypatch.setattr(
        'video_ads_compass.VertexAIHandler',
        MagicMock(return_value=mock_vertex_ai_handler),
    )

    video_uris = ['test_video.mp4']
    df = process_videos_and_create_df(video_uris, test_config)
    assert isinstance(df, pd.DataFrame)


def test_main(monkeypatch):
    """Tests the main function.
    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    monkeypatch.setattr(
        'video_ads_compass.download_and_list_video_files_gcs',
        MagicMock(return_value=['test_video.mp4']),
    )
    monkeypatch.setattr(
        'video_ads_compass.process_videos_and_create_df',
        MagicMock(return_value=pd.DataFrame()),
    )
    monkeypatch.setattr('video_ads_compass.GoogleSheetsHandler', MagicMock())

    main()

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

"""Test file for the vertex ai module."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, g-importing-member, g-import-not-at-top

import sys

sys.path.append('.')
from unittest.mock import MagicMock

import pytest

from utils.config import Config
from utils.vertex_ai import VertexAIHandler


class TestConfig(Config):
    def __init__(self):
        self.ai_api_key = 'test_api_key'
        self.model = 'test_model'


@pytest.fixture
def test_config():
    """Mocks the configuration object for testing."""
    return TestConfig()


def test_analyze_video(monkeypatch, mock_config):
    """Tests the analyze_video method.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        mock_config: Mock configuration object.
    """
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = (
        '{"rules": [], ' '"overall_compliance_assessment": "Compliant"}'
    )
    mock_client.models.generate_content.return_value = mock_response
    monkeypatch.setattr(
        'utils.vertex_ai.genai.Client', MagicMock(return_value=mock_client)
    )
    mock_open = MagicMock()
    mock_open.return_value.read.return_value = b'test video content'
    monkeypatch.setattr('builtins.open', mock_open)

    vertex_ai_handler = VertexAIHandler(mock_config)

    result = vertex_ai_handler.analyze_video('test_video.mp4')

    assert isinstance(result, str)


def test_response_mime_type(mock_config):
    """Tests the response_mime_type property.
    Args:
        mock_config: Mock configuration object.
    """
    vertex_ai_handler = VertexAIHandler(mock_config)

    mime_type = vertex_ai_handler.response_mime_type

    assert mime_type == 'application/json'


def test_response_schema(mock_config):
    """Tests the response_schema property.
    Args:
        mock_config: Mock configuration object.
    """
    vertex_ai_handler = VertexAIHandler(mock_config)

    schema = vertex_ai_handler.response_schema

    assert isinstance(schema, dict)
    assert 'type' in schema
    assert 'properties' in schema


def test_prompt(monkeypatch, mock_config):
    """Tests the prompt property.
    Args:
        monkeypatch: pytest monkeypatch fixture.
        mock_config: Mock configuration object.
    """
    monkeypatch.setattr('builtins.open', MagicMock())

    vertex_ai_handler = VertexAIHandler(mock_config)

    prompt = vertex_ai_handler.prompt

    assert isinstance(prompt, str)

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

"""Module responsible for reading the app configurations."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, protected-access

from typing import Any, Dict

import smart_open
import yaml

from utils import auth
from utils.logging import logger

_CONFIG_FILE_PATH = './config.yaml'


class Config:
    """Class responsible for all of the app configurations.
    Some app configurations can be modified by the user and others cannot.
    Attributes:
        client_id: OAuth client ID.
        client_secret: OAuth client secret.
        refresh_token: OAuth refresh token.
        ai_api_key: Gemini API Key
        project_id: GCP Project ID
        location: GCP location
        model: AI Model
        video_source: Where to read videos from - drive/GCS
        bucket_name: Bucket name if videos from GCS
        drive_folder_url: Drive link if videos from drive
    """

    def __init__(self) -> None:
        """Initializes the instance of the config file."""
        config = self.load_config_from_file()
        if config is None:
            config = {}

        self.client_id = config.get('client_id', '')
        self.client_secret = config.get('client_secret')
        self.refresh_token = config.get('refresh_token', '')
        self.ai_api_key = config.get('ai_api_key', '')
        self.project_id = config.get('project_id', '')
        self.bucket_name = config.get('bucket_name', '')
        self.location = config.get('location', '')
        self.model = config.get('model', '')

    def load_config_from_file(self) -> Dict[str, Any]:
        """Loads configuration file from GCS.
        Returns:
            loaded configuration.
        """
        try:
            config_content = smart_open.open(_CONFIG_FILE_PATH, 'rb')
        except FileNotFoundError as e:
            logger.error(f'Could not find config file at: {_CONFIG_FILE_PATH}')
            raise e
        config = yaml.load(config_content, Loader=yaml.SafeLoader)
        return config

    @property
    def credentials(self) -> Any:
        """Gets the OAuth credentials object for the client id and secret.
        Returns:
            crendtials object.
        """
        return auth._get_credentials(self.__dict__)

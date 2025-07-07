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

"""Credentials validation for Google Sheets, Drive and Vertex AI APIs."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, broad-exception-caugh

from typing import Any, Final

from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from utils import logging as log

_SCOPES: Final[list[str]] = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/devstorage.read_only',
]


def _get_credentials(config: dict[str, Any]) -> Credentials:
    """Validates the users credentials have the needed scope.
    Args:
        config: dictionary of user credentials to validate
    Returns:
        Crednetials object if the credentials are valid
    """
    creds = None
    user_info = {
        'client_id': config['client_id'],
        'refresh_token': config['refresh_token'],
        'client_secret': config['client_secret'],
    }

    creds = Credentials.from_authorized_user_info(user_info, _SCOPES)

    if creds.expired:
        try:
            creds.refresh(Request())
        except exceptions.RefreshError as error:
            if 'invalid_scope' in error.args[0]:
                log.logger.error(
                    'Refresh token with invalid scope.'
                    'Regenerate a new one from the OAuthPlayground'
                    '(Refer to README for more information)'
                )
                creds = Credentials.from_authorized_user_info(
                    user_info, _SCOPES
                )
    if not creds.valid:
        creds = None
    return creds

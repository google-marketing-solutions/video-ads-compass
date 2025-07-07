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

"""Module responsible for interacting with Google Sheets."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary, g-importing-member, broad-exception-caught

from datetime import datetime

import gspread
import pandas as pd

from utils import logging as log
from utils.config import Config


class GoogleSheetsHandler:
    """Class for handeling Google Sheets."""

    def __init__(self, config: Config):
        """Inititate the handler.
        Args:
            config: The Config object containing configuration parameters.
        """
        self.gc = gspread.Client(config.credentials)

    def create_spreadsheet(
        self, spreadsheet_name_prefix: str = 'Video Ads Compass Output'
    ) -> gspread.Spreadsheet:
        """Creates a new Google Sheet.
        Args:
            spreadsheet_name_prefix: The prefix for the spreadsheet name.
        Returns:
            The created spreadsheet.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        spreadsheet_name = f'{spreadsheet_name_prefix} {timestamp}'
        try:
            return self.gc.create(spreadsheet_name)
        except Exception as e:
            log.logging.error(f'Error creating spreadsheet: {e}')

    def upload_dataframe(
        self, spreadsheet: gspread.Spreadsheet, dataframe: pd.DataFrame
    ) -> None:
        """Uploads a Pandas DataFrame to a Google Sheet.
        Args:
            spreadsheet: The Google Sheet to upload the DataFrame to.
            dataframe: The Pandas DataFrame to upload.
        """
        try:
            worksheet = spreadsheet.sheet1
            worksheet.update(
                [dataframe.columns.values.tolist()] + dataframe.values.tolist()
            )
        except Exception as e:
            log.logging.error(f'Error uploading dataframe to spreadsheet: {e}')

    def format_spreadsheet(self, spreadsheet: gspread.Spreadsheet) -> str:
        """Formats the Google Sheet according to the provided instructions.
        Args:
            spreadsheet: The Google Sheet to format.
        Returns:
            The URL of the formatted spreadsheet.
        """
        worksheet = spreadsheet.sheet1

        worksheet.format(
            'A1:I1',
            {
                'textFormat': {
                    'bold': True,
                },
                'backgroundColor': {
                    'red': 0.8,
                    'green': 0.9,
                    'blue': 1.0,
                },
            },
        )

        df = pd.DataFrame(worksheet.get_all_records())
        for index, row in df.iterrows():
            if row.get('rule_violation') == 'TRUE':
                worksheet.format(
                    f'A{index+2}:I{index+2}',
                    {
                        'backgroundColor': {
                            'red': 1.0,
                            'green': 0.8,
                            'blue': 0.8,
                        },
                    },
                )

        current_video_key = None
        for index, row in df.iterrows():
            if row.get('video_key') != current_video_key:
                worksheet.format(
                    f'A{index+2}:I{index+2}',
                    {
                        'borders': {
                            'top': {
                                'style': 'SOLID',
                                'width': 2,
                                'color': {
                                    'red': 0,
                                    'green': 0,
                                    'blue': 0,
                                },
                            },
                        }
                    },
                )
                current_video_key = row.get('video_key')

        return spreadsheet.url

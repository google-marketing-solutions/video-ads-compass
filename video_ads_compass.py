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

"""Main module for the Video Ads Compass application."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary

import json
import os
import traceback
from typing import List

import pandas as pd
from google.cloud import storage

from utils.config import Config
from utils.sheets import GoogleSheetsHandler
from utils.vertex_ai import VertexAIHandler

_DESTINATION_DIR = './temp_videos'


def download_and_list_video_files_gcs(config: Config) -> List[str]:
    """Lists and downloads MP4 files within the specified GCS bucket.

    Args:
        config: The Config object containing configuration parameters.
    Returns:
        A list of paths to the downloaded video files.
    """
    client = storage.Client(credentials=config.credentials)
    video_files = []
    for blob in client.list_blobs(config.bucket_name):
        blob_file_path = f'{_DESTINATION_DIR}/{blob.name}'
        if 'mp4' in blob.name:
            if not os.path.exists(blob_file_path):
                blob.download_to_filename(blob_file_path)
            video_files.append(blob_file_path)
    return video_files


def process_videos_and_create_df(
    video_uris: List[str], config: Config
) -> pd.DataFrame:
    """Processes video URIs and analyzes them.
    Creates a flattened DataFrame.

    Args:
        video_uris: A list of video URIs to process.
        config: The Config object containing configuration parameters.
    Returns:
        A flattened DataFrame containing the analysis results.
    """

    all_results = []
    vertex_ai_handler = VertexAIHandler(config)

    for key, file_path in enumerate(video_uris):
        try:
            result_text = vertex_ai_handler.analyze_video(file_path)
            if result_text:
                result = json.loads(result_text)
                for rule in result['rules']:
                    rule['video_type'] = 'all'
                    rule['video_key'] = key
                    rule['video_uri'] = file_path
                    rule['overall_compliance_assessment'] = result[
                        'overall_compliance_assessment'
                    ]
                all_results.extend(result['rules'])
        except ValueError as e:
            print(f'Error processing URI {file_path}: {e}')
            traceback.print_exc()

    if not all_results:
        return pd.DataFrame()

    df = pd.DataFrame(all_results)
    df = df[
        [
            'video_type',
            'video_key',
            'video_uri',
            'overall_compliance_assessment',
            'rule_index',
            'rule_violation',
            'violation_score',
            'violation_reason',
            'violation_time',
        ]
    ]

    return df


def main():
    """Main function to orchestrate the Video Ads Compass workflow.

    Args:
        None
    Returns:
        None
    """

    config = Config()

    video_uris = download_and_list_video_files_gcs(config)

    df_results = process_videos_and_create_df(video_uris, config)

    if not df_results.empty:
        sheets_handler = GoogleSheetsHandler(config)
        spreadsheet = sheets_handler.create_spreadsheet()
        sheets_handler.upload_dataframe(spreadsheet, df_results)
        output_url = sheets_handler.format_spreadsheet(spreadsheet)
        print(
            'Finished Video Ads Compass analysis. '
            f'Find results here: {output_url}'
        )
    else:
        print('No results to upload to Google Sheets.')


if __name__ == '__main__':
    main()

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

"""Module responsible for interacting with Vertex AI API."""
# pylint: disable=C0330, g-bad-import-order, g-multiple-import, bad-indentation, g-no-space-after-docstring-summary

from typing import Any, Dict

from google import genai
from google.genai import types

from utils.config import Config


class VertexAIHandler:
    """Class for handeling Vertex AI API."""

    def __init__(self, config: Config) -> None:
        """Initiate the Vertex AI API handler.
        Args:
            config: The Config object containing configuration parameters.
        """
        self.client = genai.Client(api_key=config.ai_api_key)
        self.model = config.model
        self.response_mime_type = 'application/json'

    def analyze_video(self, video_path: str) -> str:
        """Calls the genai generate content api to analyze video.
        Args:
            video_path: The path to the video file.
        Returns:
            The GenAI generated content in the form of a string.
        """

        video_file_name = video_path
        video_bytes = open(video_file_name, 'rb').read()

        response = self.client.models.generate_content(
            model=self.model,
            contents=types.Content(
                parts=[
                    types.Part(
                        text=self.prompt,
                    ),
                    types.Part(
                        inline_data=types.Blob(
                            data=video_bytes,
                            mime_type='video/mp4',
                        )
                    ),
                ]
            ),
            config={
                'response_mime_type': self.response_mime_type,
                'response_schema': self.response_schema,
            },
        )

        if response:
            return response.text
        return None

    @property
    def response_schema(self) -> Dict[str, Any]:
        """Generates correct response schema.
        Returns:
            The response schema.
        """
        rule_schema = {
            'type': 'object',
            'properties': {
                'rule_index': {'type': 'integer'},
                'rule_violation': {'type': 'boolean'},
                'violation_score': {'type': 'integer'},
                'violation_reason': {'type': 'string'},
                'violation_time': {'type': 'string'},
            },
            'required': [
                'rule_index',
                'rule_violation',
                'violation_score',
                'violation_reason',
                'violation_time',
            ],
        }

        response_schema = {
            'type': 'object',
            'properties': {
                'overall_compliance_assessment': {'type': 'number'},
                'rules': {
                    'type': 'array',
                    'items': rule_schema,
                },
            },
            'required': ['overall_compliance_assessment', 'rules'],
        }
        return response_schema

    @property
    def prompt(self) -> None:
        """Build the prompt for GenAI model from base prompt and rules file.
        Returns:
            The prompt for the GenAI model.
        """
        # Load rules file
        with open('rules.csv', 'r') as file:
            rules_content = file.read()

        prompt = f"""You are an experienced advertising content reviewer.
            You specialize in determining whether or not a video ad violates google ads policy or not.
            Please conduct a strict content review of the video ad provided according to the detailed review tags - added below in csv format.
            Your judgment will directly affect the launch and promotion of this video ad, so please take every detail seriously.
            Based on the attached policy rules, analyze the video and for each policy rule determine if it violates it or not.
            If it does violate it, score the seriousness of the violation on a scale of 1 to 5,
            explain the reason for your decision, and provide the timestamp for the violation part.

            Video Ad Policy Review Instructions:
            - Carefully watch the entire video ad from start to finish
            - Analyze each frame and content element against the attached policy rules
            - Be thorough and objective in your assessment
            - Consider context, intent, and potential viewer interpretation

            Detailed Review Methodology:
            1. For each policy rule, provide a comprehensive analysis
            2. If a rule is violated, clearly document:
               - Specific timestamp(s) of violation
               - Exact content causing the violation
               - Visual or contextual details

            3. Assess violation severity and potential impact

            Output Format (for each rule):
            {{
                "rule_index": int,                 # Policy rule index number
                "rule_violation": bool,             # Whether rule is violated
                "violation_score": int,             # Severity (1-5)
                "confidence_score": float,          # Confidence in assessment (0.0-1.0)
                "violation_reason": str,            # Detailed explanation
                "violation_timestamp": str,         # Specific timestamp of violation
            }}

            Final Report Requirements:
            - Overall Compliance Assessment: Provide a summary percentage of policy compliance
            - The answer for each rule according to the provided format

            Here are the review tags, in a CSV format:
            {rules_content}
            """
        return prompt

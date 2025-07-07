# Implementation Guide

> [!WARNING]
> The analysis is for reference only and does not constitute the final interpretation or enforcement of Google Ads policies. Whether or not an ad violates the policy is still subject to the latest version of Google Ads policies.

## What is Video Ads Compass?

Video Ads Compass is a self-service solution that aims to coach advertisers on which parts of their video ads might be in violation of a specific Google Ads Policy. This tool relies on the public policy rules and best practices curated by the user based on their experience.

The Video Ads Compass tool will analyze the videos against an AI-generated rules file and will determine if and when each rule was violated in the video ad. Clients can use this output to better understand which parts of the video might be in violation of the specific policy.

---

## Prerequisites

1.  A GCP project with billing attached.
2.  The Vertex AI API enabled.
3.  A policy rules file in CSV format, named `rules.csv` with the following columns: `Rule ID`, `Rule Description`.

---

## How do I deploy it?

1.  Make a copy of the desired version of the Colab notebook.
2.  To create the basic rule file, we recommend using Gemini with the following prompt:
    > "You are an expert in digital advertising policy and compliance. Your task is to create a rules file in CSV format for a Video Ads Compass Tool. This tool will scan video ads to ensure they adhere to the Ads policy outlined at `[Insert Public Policy URL here]`.
    >
    > Generate a list of ## distinct rules. The CSV file must contain the following columns:
    > - **RuleID:** A numeric unique identifier for each rule (01, 02).
    > - **RuleDescription:** A clear and concise explanation of the rule."

3.  Upload the `rules.csv` file to the "Files" tab on the left side of the Colab interface.
4.  Have your videos ready in either a GCP Cloud Storage Bucket or a Google Drive folder.
    - It is recommended to use a shortened version of the videos, containing only the first minute.
    - There is a code block in the Colab that creates a shortened version of the videos in the folder.
5.  Run the Colab cells one by one and enter configuration details where needed.
6.  If using a Google Drive folder as the source of videos, you need to provide the base path of this folder, depending on whether it's your drive or a shared drive, using one of these formats:
    - `MyDrive/Path/To/Folder`
    - `SharedDrive/Path/To/Folder`
7.  When finished, you will receive a Google Spreadsheet URL to access the tool's output.

You can use an existing GCP project or create a new one. See the guide on [setting up Vertex AI API access](https://cloud.google.com/vertex-ai/docs/start/cloud-project).

---

## Configuration within the Colab

-   `PROJECT_ID`: Your GCP Project ID.
-   `LOCATION`: The GCP location/region (e.g., `us-central1`).
-   `MODEL`: The Gen AI Model to use. The most recommended is `gemini-1.5-pro-preview-0409` for the best validation.
-   `VIDEO_SOURCE`: Select if the videos you would like to validate are located in a GCP Bucket or a Google Drive folder.

---

## Analyzing the Validation Results

> [!IMPORTANT]
> **Disclaimer:** This analysis is for reference only and does not constitute the final interpretation or enforcement of Google Ads policies. Whether or not an ad violates the policy is still subject to the latest version of Google Ads policies.

> [!NOTE]
> Do not review the tool analysis as a binary indication on whether the video will be approved or disapproved. The Video Ads Compass is an educational tool to provide an indication and education on Google Ads Policy and to help advertisers learn what, within a video, might be a violation of Google Ads policy as described in the public policy knowledgebase.

### Output Fields

-   **Video_key**: Each video stored in the Bucket or Drive Folder will receive a number in chronological order. `Video_Key` is the number of the specific video.
-   **Video_url**: The URL or path to the analyzed video.
-   **Overall_compliance_assessment**: A score that combines the total compliance validation of the video.
-   **Rule_index**: The rule number within the `rules.csv` file to which the validation refers.
-   **Rule_Violation (TRUE/FALSE)**: Indicates if the analyzed video was flagged for the specific rule within the `rules.csv` file.
-   **Violation_score**: A rank of the violation of that specific rule, ranging from 0 to 5.
-   **Violation_Reason**: An explanation by the model as to why the video is flagged for that specific rule.

### Recommendation

> For rules where `Rule_Violation` = `TRUE`, we recommend reviewing the `violation_score`. If it is **above 3**, review the `Violation_Reason` to decide if and which changes to make to your video.

---

## How much will it cost me?

Please see [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing) for details on the cost associated with using the underlying services.

import os
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage

# Configuration
PROJECT_ID = "hr-analytics-data-warehouse"
BUCKET_NAME = "hr-analytics-data-lake"
DATASET_SLUG = "rhuebner/human-resources-data-set"

# Local download directory
DOWNLOAD_DIR = Path("data") / "raw" / "hr_kaggle"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # 1. Validate credentials
    if not os.getenv("KAGGLE_API_TOKEN"):
        raise EnvironmentError(
            "KAGGLE_API_TOKEN is missing. Set it in this terminal."
        )

    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS is missing. "
            "Set it to your GCP service-account JSON key path."
        )

    # 2. Authenticate with Kaggle
    print("Connecting to Kaggle...")
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()
    print("Kaggle authentication successful.")

    # 3. Download and extract the dataset
    print("Downloading HR dataset from Kaggle...")
    kaggle_api.dataset_download_files(
        DATASET_SLUG,
        path=str(DOWNLOAD_DIR),
        unzip=True,
        quiet=False,
    )
    print("Dataset download completed.")

    # 4. Find CSV files
    csv_files = list(DOWNLOAD_DIR.rglob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {DOWNLOAD_DIR.resolve()}"
        )

    print(f"Found {len(csv_files)} CSV files.")

    # 5. Connect to GCS
    print("Connecting to Google Cloud Storage...")
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)

    # 6. Upload CSV files to GCS
    for file_path in csv_files:
        relative_path = file_path.relative_to(DOWNLOAD_DIR).as_posix()
        blob_name = f"raw/{relative_path}"

        blob = bucket.blob(blob_name)
        blob.upload_from_filename(
            str(file_path),
            content_type="text/csv",
        )

        print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

    print("\nHR dataset ingestion completed successfully!")
    print(f"Files uploaded: {len(csv_files)}")
    print(f"GCS location: gs://{BUCKET_NAME}/raw/")


if __name__ == "__main__":
    main()

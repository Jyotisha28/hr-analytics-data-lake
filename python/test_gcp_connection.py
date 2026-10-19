from google.cloud import storage
from google.cloud import bigquery

HR_PROJECT_ID = "hr-analytics-data-warehouse"

storage_client = storage.Client(project=HR_PROJECT_ID)
bigquery_client = bigquery.Client(project=HR_PROJECT_ID)

print("GCS client project:", storage_client.project)
print("BigQuery client project:", bigquery_client.project)

print("\nBigQuery datasets:")
for dataset in bigquery_client.list_datasets():
    print(dataset.dataset_id)

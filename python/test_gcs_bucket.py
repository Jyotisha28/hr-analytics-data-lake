from google.cloud import storage

PROJECT_ID = "hr-analytics-data-warehouse"

client = storage.Client(project=PROJECT_ID)

print("Accessible GCS buckets:")

for bucket in client.list_buckets():
    print(bucket.name)

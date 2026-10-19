import google.auth

credentials, project_id = google.auth.default()

print("Authentication successful!")
print("Project ID:", project_id)
print("Credentials type:", type(credentials).__name__)
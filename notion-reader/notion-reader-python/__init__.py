import os
import csv
import json
import datetime
import requests
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

notion_api_key = os.environ["NOTION_API_KEY"]
notion_page_id = os.environ["NOTION_PAGE_ID"]
connection_string = os.environ["AzureWebJobsStorage"]

headers = {
    "Notion-Version": "2022-05-13",
    "Authorization": f"Bearer {notion_api_key}",
}

url = f"https://api.notion.com/v1/blocks/{notion_page_id}/children"

response = requests.get(url, headers=headers)
response_json = response.json()

with open("notion-api.log", "w") as log_file:
    json.dump(response_json, log_file, indent=4)

blocks = response_json["results"]

extracted_data = []

for block in blocks:
    if "plain_text" in block:
        extracted_data.append(
            {
                "id": block["id"],
                "timestamp": datetime.datetime.now().isoformat(),
                "plain_text": block["plain_text"],
            }
        )

with open("notion-page-croll.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["id", "timestamp", "plain_text"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in extracted_data:
        writer.writerow(row)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "csv-container"
blob_container_client = blob_service_client.get_container_client(container_name)

try:
    blob_container_client.create_container()
except:
    pass

with open("notion-api.log", "rb") as log_file:
    blob_client = blob_container_client.get_blob_client("notion-api.log")
    blob_client.upload_blob(log_file, overwrite=True)

with open("notion-page-croll.csv", "rb") as csvfile:
    blob_client = blob_container_client.get_blob_client("notion-page-croll.csv")
    blob_client.upload_blob(csvfile, overwrite=True)

# Arun Kulkarni

import azure.functions as func
import logging
import os
import json
from azure.data.tables import TableServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_table_client():
    connection_string = os.environ["COSMOS_DB_CONNECTION_STRING"]
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_name = "VisitorCount"  # Replace with your table name
    return table_service.get_table_client(table_name)

def get_visitor_count(table_client):
    try:
        entity = table_client.get_entity(partition_key="visitorCounter", row_key="0")
        return entity['count']
    except Exception as e:
        logging.error(f"Error fetching entity: {str(e)}")
        return 0  # Assuming count starts at 0 if not found

def update_visitor_count(table_client, count):
    table_client.upsert_entity({"PartitionKey": "visitorCounter", "RowKey": "0", "count": count})

def process_visitor_count():
    table_client = get_table_client()
    current_count = get_visitor_count(table_client)
    updated_count = current_count + 1
    update_visitor_count(table_client, updated_count)
    return updated_count

@app.route(route="update_visitor_count")
def update_visitor_count_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        visitor_count = process_visitor_count()
        return func.HttpResponse(
            json.dumps({"visitorCount": visitor_count}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

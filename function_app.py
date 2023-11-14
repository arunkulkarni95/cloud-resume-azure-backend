import azure.functions as func
import logging
import os
from azure.data.tables import TableServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Initialize Table Service Client
connection_string = os.environ["COSMOS_DB_CONNECTION_STRING"]
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_name = "VisitorCount"  # Replace with your table name
table_client = table_service.get_table_client(table_name)

def get_and_update_visitor_count():
    # Try to fetch the existing count
    try:
        entity = table_client.get_entity(partition_key="visitorCounter", row_key="0")
        current_count = entity['count']
    except Exception as e:
        logging.error(f"Error fetching entity: {str(e)}")
        # If the entity doesn't exist, start with count = 0
        current_count = 0

    # Update the count
    updated_count = current_count + 1
    table_client.upsert_entity({"PartitionKey": "visitorCounter", "RowKey": "0", "count": updated_count})

    return updated_count

@app.route(route="update_visitor_count")
def update_visitor_count(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        visitor_count = get_and_update_visitor_count()
        return func.HttpResponse(f"Visitor count updated. Current count: {visitor_count}", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

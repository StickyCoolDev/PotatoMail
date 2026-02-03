from appwrite.client import Client
from appwrite.services.tables_db import TablesDB
from appwrite.id import ID
import os


client = Client()
client.set_endpoint(os.getenv("APPWRITE_ENDPOINT")) # Your API Endpoint
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))              # Your Project ID
client.set_key(os.getenv("APPWRITE_API_KEY"))

db = TablesDB(client)
def create_new_email(to_email : str, subject : str, body :str, html_body: str | None = None):
    try:
        result = db.create_row(
            database_id=os.getenv("APPWRITE_DATABASE_ID", ""),
            table_id='emails',
            row_id=ID.unique(),
            data={
                # These keys must match the Schema in Image 2 exactly (Case Sensitive)
                'Subject': subject,
                'Body': body,
                'ReceiverEmail': to_email,
                'HtmlBody': html_body # 
            }
        )
        print("Row added successfully:", result)
    except Exception as e:
        print("Error adding row:", e)

# Example usage:
# create_new_email('john@example.com', 'Welcome!', 'Thanks for signing up.')


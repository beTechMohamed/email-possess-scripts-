import os
import sqlite3
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def authenticate_gmail():
    """Authenticate to Gmail API and return credentials."""
    creds = None
    # Load credentials from file
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            logging.info("Loaded credentials from token.json")
        except ValueError as e:
            logging.error("Error loading credentials: %s", e)
            creds = None
    # Refresh or generate new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                request = Request()
                creds.refresh(request)
                logging.info("Token refreshed successfully")
            except requests.exceptions.RequestException as e:
                logging.error("Request exception during token refresh: %s", e)
                raise
            except Exception as e:
                logging.error("Error refreshing token: %s", e)
                creds = None
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                logging.info("New token saved to token.json")
            except Exception as e:
                logging.error("Error during authentication: %s", e)
                raise

    logging.info("Authentication completed")
    return creds

def fetch_emails(service):
    """Fetch emails from Gmail and return them as a list of dictionaries."""
    try:
        logging.info("Fetching emails...")
        results = service.users().messages().list(userId='me', maxResults=1).execute()
        logging.info("Fetched results: %s", results)
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload'].get('headers', [])
            sender = next((header['value'] for header in headers if header['name'] == 'From'), None)
            email_data = {
                'id': msg['id'],
                'snippet': msg['snippet'],
                'sender': sender
            }
            emails.append(email_data)
        logging.info("Emails fetched")
        return emails
    except Exception as e:
        logging.error("Error fetching emails: %s", e)
        raise

def save_emails_to_db(emails):
    """Save email data to an SQLite database."""
    try:
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS emails
                     (id TEXT PRIMARY KEY, snippet TEXT, sender TEXT)''')
        for email in emails:
            c.execute('INSERT OR IGNORE INTO emails (id, snippet, sender) VALUES (?, ?, ?)', (email['id'], email['snippet'], email['sender']))
        conn.commit()
        conn.close()
        logging.info("Emails saved")
    except Exception as e:
        logging.error("Error saving emails to database: %s", e)
        raise

def main():
    """Main function to authenticate, fetch, and save emails."""
    try:
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)
        emails = fetch_emails(service)
        save_emails_to_db(emails)
        logging.info("Emails have been saved")
    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == '__main__':
    main()

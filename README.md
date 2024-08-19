# Email Processing Script

This repository contains scripts to authenticate with the Gmail API, fetch emails, apply user-defined rules, and save the results to an SQLite database.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [License](#license)

## Prerequisites

- Python 3.x and venv
- `pip` (Python package installer)

You will need the following Python libraries:
- `google-auth`
- `google-auth-oauthlib`
- `google-api-python-client`
- `requests`
- `sqlite3`

Install the required libraries using:

```bash
pip install google-auth google-auth-oauthlib google-api-python-client requests
```

(OR)

```bash
pip install -r requirements.txt
```


Setup
Google API Credentials:

Create a Google Cloud project and enable the Gmail API.
Download the credentials.json file and place it in the root directory of this repository. This file is used for OAuth2 authentication with the Gmail API.
Rules Configuration:

Create a rules.json file in the root directory with the rules for processing emails. Here is an example format:
```bash
{
  "collection_predicate": "Any",
  "rules": [
    {
      "field": "From",
      "predicate": "Contains",
      "value": "example@example.com",
      "actions": ["Mark as read"]
    },
    {
      "field": "Subject",
      "predicate": "Contains",
      "value": "Important",
      "actions": ["Mark as unread"]
    }
  ]
}
```
## Database:

The script will create an SQLite database file named emails.db in the root directory if it does not already exist. This database will store the fetched emails.
## Usage
### Authenticate and Fetch Emails:

To authenticate with the Gmail API, fetch emails, and save them to the database, run the following script:

```bash
python fetch_emails.py
```
### Apply Rules:

To apply rules to the fetched emails and perform the specified actions, run:

```bash
python apply_rules.py
```
## File Structure

- `fetch_emails.py`: Script for authenticating with the Gmail API, fetching emails, and saving them to the SQLite database.
- `apply_rules.py`: Script for loading rules from `rules.json`, applying them to emails, and performing actions.
- `credentials.json`: Google API credentials file required for authentication.
- `rules.json`: JSON file containing rules for processing emails.
- `emails.db`: SQLite database file for storing fetched emails (created automatically).

## Configuration

### Token Management

The `fetch_emails.py` script will generate and manage a `token.json` file for OAuth2 tokens. Ensure this file is kept secure and is not exposed publicly.

### Error Handling

If you encounter errors, check the log messages for details. Adjust the scripts as necessary based on the error messages you receive.
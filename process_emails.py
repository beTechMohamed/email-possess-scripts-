import json
import sqlite3
import logging

def load_rules():
    """Load rules from a JSON file."""
    try:
        with open('rules.json') as file:
            return json.load(file)
    except Exception as e:
        logging.error("Error loading rules: %s", e)
        raise

def apply_rules_to_emails(rules, emails):
    """Apply rules to emails and perform actions if rules match."""
    for email in emails:
        matches = []
        for rule in rules['rules']:
            if rule['field'] == "From" and rule['predicate'] == "Contains" and rule['value'] in email[2]:
                matches.append(True)
            elif rule['field'] == "Subject" and rule['predicate'] == "Contains" and rule['value'] in email[1]:
                matches.append(True)

        if (rules['collection_predicate'] == "All" and all(matches)) or (rules['collection_predicate'] == "Any" and any(matches)):
            apply_actions(rule['actions'], email)

def apply_actions(actions, email):
    """Apply actions to an email based on the rules."""
    for action in actions:
        if action == "Mark as read":
            print(f"Marking email {email[0]} as read.")
        elif action == "Mark as unread":
            print(f"Marking email {email[0]} as unread.")
        # Implement other actions like move message here...

def fetch_emails_from_db():
    """Fetch emails from the SQLite database."""
    try:
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        c.execute('SELECT id, snippet, sender FROM emails')
        emails = c.fetchall()
        conn.close()
        logging.info("Emails fetched from database")
        return emails
    except Exception as e:
        logging.error("Error fetching emails from database: %s", e)
        raise

def main():
    """Main function to load rules, fetch emails, and apply rules."""
    try:
        rules = load_rules()
        emails = fetch_emails_from_db()
        apply_rules_to_emails(rules, emails)
    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

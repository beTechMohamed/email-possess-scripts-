import json
import sqlite3

def load_rules():
    with open('rules.json') as file:
        return json.load(file)

def apply_rules_to_emails(rules, emails):
    for email in emails:
        matches = []
        for rule in rules['rules']:
            if rule['field'] == "From" and rule['predicate'] == "Contains" and rule['value'] in email['snippet']:
                matches.append(True)
            elif rule['field'] == "Subject" and rule['predicate'] == "Contains" and rule['value'] in email['snippet']:
                matches.append(True)

        if (rules['collection_predicate'] == "All" and all(matches)) or (rules['collection_predicate'] == "Any" and any(matches)):
            apply_actions(rule['actions'], email)

def apply_actions(actions, email):
    for action in actions:
        if action == "Mark as read":
            print(f"Marking email {email['id']} as read.")
        elif action == "Mark as unread":
            print(f"Marking email {email['id']} as unread.")
        # Implement other actions like move message here...

def fetch_emails_from_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('SELECT * FROM emails')
    emails = c.fetchall()
    conn.close()
    return emails

def main():
    rules = load_rules()
    emails = fetch_emails_from_db()
    apply_rules_to_emails(rules, emails)

if __name__ == '__main__':
    main()

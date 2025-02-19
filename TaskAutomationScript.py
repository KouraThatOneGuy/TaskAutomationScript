import imaplib
import email
from email.parser import BytesParser
import os

class EmailCategorizer:
    def __init__(self, imap_server, username, password):
        self.mailbox = imaplib.IMAP4_SSL(imap_server)
        self.mailbox.login(username, password)
        self.categories = {}
        
    def connect(self):
        self.mailbox.select('inbox')
        
    def get_new_emails(self):
        _, search_data = self.mailbox.search(None, 'UNSEEN')
        return search_data[0].split()
        
    def categorize_email(self, msg_id):
        _, msg_data = self.mailbox.fetch(msg_id, '(RFC822)')
        raw_message = msg_data[0][1]
        email_msg = BytesParser().parsebytes(raw_message)
        
        category = self.determine_category(email_msg)
        self.move_to_folder(msg_id, category)
        
    def determine_category(self, email_msg):
        # Simple categorization based on sender domain
        sender_domain = email_msg['from'].split('@')[1]
        return self.categories.get(sender_domain, 'uncategorized')

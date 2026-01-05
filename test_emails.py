#!/usr/bin/env python3
"""Test script to verify email fetching works correctly."""
from gmail_client import get_unread_emails, get_service

if __name__ == "__main__":
    print("Fetching unread emails...")
    service = get_service()
    emails = get_unread_emails(service=service, max_results=5)
    
    print(f"\nFound {len(emails)} unread emails:\n")
    for i, email in enumerate(emails, 1):
        print(f"Email {i}:")
        print(f"  From: {email.get('from', 'N/A')}")
        print(f"  Subject: {email.get('subject', 'N/A')}")
        print(f"  Snippet: {email.get('snippet', 'N/A')[:100]}...")
        print(f"  Has body: {'Yes' if email.get('body') else 'No'}")
        print(f"  Body length: {len(email.get('body', ''))}")
        print()



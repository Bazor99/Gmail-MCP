import base64
from email.mime.text import MIMEText
from service import authenticate_gmail


def get_service():
    return authenticate_gmail()


def read_gmail_messages(service=None, max_results=5, unread_only=False):
    if service is None:
        service = get_service()

    query = "is:unread in:inbox" if unread_only else None

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = msg_data.get("payload", {}).get("headers", [])
        subject = sender = None

        for header in headers:
            if header.get("name") == "Subject":
                subject = header.get("value")
            elif header.get("name") == "From":
                sender = header.get("value")

        emails.append({
            "id": msg_data["id"],
            "threadId": msg_data["threadId"],
            "from": sender,
            "subject": subject,
            "snippet": msg_data.get("snippet")
        })

    return emails


def get_unread_emails(service=None, max_results=5):
    return read_gmail_messages(service=service, max_results=max_results, unread_only=True)


def create_draft_reply(service=None, original_message_id=None, reply_body=None):
    if service is None:
        service = get_service()

    msg_data = service.users().messages().get(
        userId="me",
        id=original_message_id,
        format="full"
    ).execute()

    headers = msg_data["payload"]["headers"]
    subject = sender = None

    for h in headers:
        if h["name"] == "Subject":
            subject = h["value"]
        elif h["name"] == "From":
            sender = h["value"]

    message = MIMEText(reply_body or "")
    message["to"] = sender
    message["subject"] = f"Re: {subject}"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().drafts().create(
        userId="me",
        body={"message": {"raw": raw, "threadId": msg_data["threadId"]}}
    ).execute()

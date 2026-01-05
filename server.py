from mcp.server.fastmcp import FastMCP
from gmail_client import get_service, get_unread_emails, create_draft_reply

mcp = FastMCP("gmail-mcp", json_response=True)

# Create a demo service instance 
SERVICE = get_service()

@mcp.tool()
def get_unread_emails_tool(max_results: int = 5):
    """
    MCP tool: returns unread emails with sender, subject, snippet/body, and ids.
    """
    emails = get_unread_emails(service=SERVICE, max_results=max_results)
    # keep only what you want the model to see
    return [
        {
            "message_id": e["id"],
            "thread_id": e["threadId"],
            "from": e["from"],
            "subject": e["subject"],
            "snippet": e["snippet"],
            # optional - sometimes you may want to return only snippet for privacy
            "body": e["body"],
        }
        for e in emails
    ]


@mcp.tool()
def create_draft_reply_tool(message_id: str, reply_body: str):
    """
    MCP tool: creates a threaded draft reply to an email.
    """
    return create_draft_reply(
        service=SERVICE,
        original_message_id=message_id,
        reply_body=reply_body
    )


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

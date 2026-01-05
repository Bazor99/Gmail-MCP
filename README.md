Project Summary

This project is a local MCP (Model Context Protocol) server that lets an AI assistant interact with a Gmail account in a safe and controlled way.

The server connects to Gmail using OAuth and exposes simple tools that allow the assistant to:

read unread emails, and

create draft replies to those emails.

When reading emails, the server returns the sender, subject, snippet, and plain-text body where available. When drafting replies, it creates a properly threaded Gmail draft without sending the email automatically, so the user stays in control.

The server runs locally and communicates with MCP-compatible clients (such as Claude Desktop) over standard input/output. It’s designed as a lightweight foundation for building AI email assistants and demonstrates how real-world APIs can be safely exposed to an AI through MCP tools.

## Running locally
Important: You will need Google Credentials, a json file from google console
```bash
uv venv
uv pip install -r requirements.txt or uv add mcp and other dependencies
uv run server.py or uv run python server.py

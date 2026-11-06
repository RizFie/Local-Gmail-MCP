import base64

from mcp.server.mcpserver import MCPServer
from auth_test import authenticate_gmail

mcp = MCPServer("Local Gmail")

def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""

def extract_body(payload):
    """Extract readable text from a Gmail message payload."""
    mime_type = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data")

    if mime_type == "text/plain" and body_data:
        return base64.urlsafe_b64decode(
            body_data + "=" * (-len(body_data) % 4)
        ).decode("utf-8", errors="replace")

    parts = payload.get("parts", [])

    for part in parts:
        result = extract_body(part)
        if result:
            return result

    if mime_type == "text/html" and body_data:
        return base64.urlsafe_b64decode(
            body_data + "=" * (-len(body_data) % 4)
        ).decode("utf-8", errors="replace")

    return ""

@mcp.tool()
def list_emails(max_results: int = 10) -> list:
    """List the latest emails in the Gmail inbox."""

    service = authenticate_gmail()

    max_results = max(1, min(max_results, 25))

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for message in messages:
        email = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = email.get("payload", {}).get("headers", [])

        emails.append({
            "id": email["id"],
            "from": get_header(headers, "From"),
            "subject": get_header(headers, "Subject"),
            "date": get_header(headers, "Date"),
            "snippet": email.get("snippet", "")
        })

    return emails


@mcp.tool()
def search_emails(query: str, max_results: int = 10) -> list:
    """
    Search Gmail using Gmail search syntax.

    Examples:
    from:someone@example.com
    is:unread
    subject:internship
    newer_than:7d
    """

    service = authenticate_gmail()

    max_results = max(1, min(max_results, 25))

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for message in messages:
        email = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = email.get("payload", {}).get("headers", [])

        emails.append({
            "id": email["id"],
            "from": get_header(headers, "From"),
            "subject": get_header(headers, "Subject"),
            "date": get_header(headers, "Date"),
            "snippet": email.get("snippet", "")
        })

    return emails


@mcp.tool()
def read_email(message_id: str) -> dict:
    """Read the full contents of an email by its Gmail message ID."""

    service = authenticate_gmail()

    email = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    headers = email.get("payload", {}).get("headers", [])

    return {
        "id": email["id"],
        "from": get_header(headers, "From"),
        "to": get_header(headers, "To"),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "body": extract_body(email.get("payload", {}))
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
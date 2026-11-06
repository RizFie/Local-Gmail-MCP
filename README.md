# Local Gmail MCP Connector

A locally hosted Gmail integration that allows **Unsloth Desktop** and a local LLM to interact with Gmail through the official Google Gmail API and the Model Context Protocol (MCP).

This project uses a custom Python MCP server instead of a third-party Gmail MCP server, giving you control over the integration, OAuth authentication, tool implementation, and local credential storage.

## Features

- **OAuth 2.0 Authentication:** Authenticate with your Google account.
- **Local Credential Storage:** Store OAuth tokens locally on your machine.
- **List Emails:** Retrieve recent emails from your Gmail inbox.
- **Search Emails:** Search emails using Gmail search syntax.
- **Read Emails:** Retrieve full email contents.
- **MCP Integration:** Expose Gmail functionality as tools through a local MCP server.
- **STDIO Transport:** Communicate with Unsloth Desktop without hosting a remote MCP server.

## Architecture

```text
             User
              |
              v
       Unsloth Desktop
              |
         Local LLM
              |
              v
        MCP Protocol
              |
         STDIO Transport
              |
              v
       Python MCP Server
           server.py
              |
              v
        Gmail API Client
              |
         OAuth 2.0
              |
              v
       Google Gmail API
              |
              v
         Gmail Account
```

### Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Backend implementation |
| Google Gmail API | Gmail integration |
| OAuth 2.0 | Authentication and authorization |
| Google API Python Client | Gmail API communication |
| FastMCP | MCP server implementation |
| Unsloth Desktop | AI application and MCP client |
| Ollama | Local LLM inference (optional) |

## Project Structure

```text
local-gmail-connector/
│
├── .venv/                  # Local Python environment
│
├── auth_test.py            # Gmail OAuth authentication
├── server.py               # Gmail MCP server
│
├── requirements.txt        # Python dependencies
├── .gitignore              # Excluded files
│
├── credentials.json        # Google OAuth credentials
├── token.json              # Generated OAuth token
│
└── README.md
```

**Important:** `credentials.json`, `token.json`, and `.venv/` are local-only files and should not be committed to GitHub.

## Prerequisites

- Python 3.12 or later
- Unsloth Desktop
- A Google account
- A Google Cloud project with Gmail API enabled
- Git (optional)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/RizFie/Local-Gmail-MCP.git

cd Local-Gmail-MCP
```

### 2. Create a virtual environment

Windows:

```powershell
py -3.12 -m venv .venv

.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Google Gmail API

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a Google Cloud project.
3. Navigate to APIs & Services → Library.
4. Search for Gmail API and enable it.
5. Configure the OAuth consent screen.
6. Add your Google account as a test user if your application is in Testing mode.
7. Create an OAuth Client ID.
8. Select Desktop App as the application type.
9. Download the OAuth credentials JSON.

Place the downloaded file inside the project directory and rename it:

```text
credentials.json
```

### 5. Authenticate with Gmail

Run:

```powershell
python auth_test.py
```

A browser window will open for Google OAuth authorization.

Select your Google account and grant the requested read-only Gmail permissions.

After successful authentication, `token.json` will be generated automatically.

Expected output:

```text
Gmail authentication successful!
Connected account: your-email@gmail.com
Total messages: 1234
```

The message count above is illustrative.

### 6. Connect to Unsloth Desktop

Open Unsloth Desktop and navigate to MCP Servers.

Ensure Remote Access is disabled when using local STDIO MCP servers.

Register a new MCP server with the following configuration:

| Setting | Value |
|---|---|
| Name | Local Gmail |
| Transport | STDIO |
| Executable | Path to `.venv\Scripts\python.exe` |
| Arguments | Path to `server.py` |

Example Windows configuration:

**Executable:**

```text
D:\local-gmail-connector\.venv\Scripts\python.exe
```

**Arguments:**

```text
D:\local-gmail-connector\server.py
```

Save and enable the server.

Unsloth Desktop will automatically launch the Python MCP server as a child process.

No separate server startup is required.

## Available MCP Tools

### 1. `list_emails`

Retrieves the latest emails from the Gmail inbox.

Parameters:

| Parameter | Type | Default |
|---|---|---|
| max_results | Integer | 10 |

Example:

```text
Show me my latest five inbox emails.
```

### 2. `search_emails`

Searches Gmail using Google's native search syntax.

Parameters:

| Parameter | Type | Default |
|---|---|---|
| query | String | Required |
| max_results | Integer | 10 |

Example queries:

```text
from:someone@example.com
```

```text
is:unread
```

```text
subject:internship
```

```text
newer_than:7d
```

### 3. `read_email`

Retrieves the full contents of an individual email.

Parameters:

| Parameter | Type |
|---|---|
| message_id | String |

The message ID can be obtained through `list_emails` or `search_emails`.

## Security and Privacy

This project avoids third-party Gmail MCP hosting by implementing its own local Python connector.

Security considerations:

- OAuth credentials are stored locally.
- OAuth tokens are stored locally.
- Gmail API requests are made directly from the Python connector to Google.
- MCP communication uses local STDIO.
- Gmail access initially uses the read-only OAuth scope.
- No third-party Gmail MCP server is required.

**Important privacy distinction:**

This is a locally hosted integration, not a completely offline Gmail system.

Gmail data is still retrieved from Google's infrastructure through the official Gmail API. Email contents are subsequently passed to the connected AI model.

For local AI processing, configure Unsloth Desktop to use a locally hosted model through Ollama rather than a cloud-based model provider.

### Git Ignore

Ensure `.gitignore` contains:

```gitignore
.venv/
__pycache__/
*.pyc

credentials.json
token.json

.env
```

Never commit OAuth credentials or authorization tokens to a public repository.

## Using the Project on Another Device

To reuse this connector on another computer:

1. Clone the GitHub repository.
2. Install the required Python dependencies.
3. Obtain the Google OAuth Desktop credentials and place `credentials.json` in the project directory.
4. Run `python auth_test.py` to authenticate the new device.
5. Configure the local MCP server in Unsloth Desktop using the new device's executable and project paths.

The OAuth token should be generated locally on each device. Do not transfer your existing `token.json` through GitHub.

## Current Limitations

This is an initial implementation.

| Feature | Status |
|---|---|
| Gmail OAuth authentication | Implemented |
| Local token storage | Implemented |
| MCP STDIO integration | Implemented |
| List inbox emails | Implemented |
| Search Gmail | Implemented |
| Read email contents | Implemented |
| Email thread retrieval | Planned |
| HTML email parsing | Planned |
| Attachment handling | Planned |
| Create email drafts | Planned |
| Send emails | Planned |

## Future Improvements

- Implement proper HTML-to-text conversion.
- Support email attachments.
- Add Gmail thread retrieval.
- Implement email draft creation.
- Add email sending with confirmation safeguards.
- Improve error handling and API request efficiency.
- Introduce additional Gmail management tools.

## References

- [Google Gmail API Documentation](https://developers.google.com/workspace/gmail/api)
- [Gmail API Python Quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Unsloth](https://unsloth.ai/)

---

**Project Goal:** Build a locally controlled AI agent ecosystem with direct integrations to external services, minimizing reliance on third-party MCP providers while keeping AI inference and application logic under local control.
### Google Calendar MCP Server Demo


# Run it like this 
```shell
    uv --directory [PROJ_DIRECTORY] run calendar_mcp.py
```
# example
```shell
    uv --directory /Users/emilakerman/Documents/calendar run calendar_mcp.py
```

# How it works?

1. You need a GCP Account with a project created as well as Google Calendar API Activated.
2. Create a service account with access to the google calendar api and that project.
3. Download the json key and rename it to service_account.json and place it in the root of this project.
4. In your google calendar, share the calendar with the gmail from the service account json file.
5. Update the values of the calendarId in the calendar_mcp.py with the calendar owner's gmail.


# Use the tools in Claude Desktop

Create a claude config file:
```shell
    code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Modify the config file and add this:

```json
{
  "mcpServers": {
    "calendar": {
      "command": "/Users/[USER]/.local/bin/uv",
      "args": [
        "--directory",
        "[PROJ_DIRECTORY]",
        "run",
        "calendar_mcp.py"
      ]
    }
  }
}
```# mcp-server-google-calendar

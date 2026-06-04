# Serena MCP Server

Exposes the Seavista workspace as a Serena MCP server for semantic code retrieval, symbol search, and IDE-like code analysis.

## Quick Start

Copy the example override, edit the mounts for your setup, then start:

```bash
cp docker-compose.projects.example.yml docker-compose.projects.yml
# Edit docker-compose.projects.yml — add/remove project mounts

docker compose -f docker-compose.yml -f docker-compose.projects.yml up -d

# Check status
docker compose -f docker-compose.yml -f docker-compose.projects.yml ps

# View logs
docker compose -f docker-compose.yml -f docker-compose.projects.yml logs -f

# Stop
docker compose -f docker-compose.yml -f docker-compose.projects.yml down
```

## Endpoints

| Service | URL |
|---------|-----|
| MCP (Streamable HTTP) | `http://localhost:9121/mcp` |
| Dashboard | `http://localhost:24282/dashboard` |

## Connect via MCP

The server exposes a Streamable HTTP MCP endpoint at `http://localhost:9121/mcp`. Add this URL as
an HTTP MCP server in your client.

### VS Code (Copilot)

1. Open the Command Palette → **MCP: Add Server**
2. Select **HTTP/SSE** (or **Remote**)
3. Enter `http://localhost:9121/mcp` as the URL
4. Name it `serena`
5. In chat, prompt: *"Activate the current project using Serena"* (pick the project from the list)

Alternatively, add to `.vscode/mcp.json` in the workspace:

```json
{
  "servers": {
    "serena": {
      "type": "http",
      "url": "http://localhost:9121/mcp"
    }
  }
}
```

### Claude Code

```bash
# Add as a remote MCP server (Claude Code >= v2 with HTTP support)
claude mcp add serena --url http://localhost:9121/mcp
```

Or in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "serena": {
      "url": "http://localhost:9121/mcp"
    }
  }
}
```

### Claude Desktop

Open **File → Settings → Developer → MCP Servers → Edit Config** and add:

```json
{
  "mcpServers": {
    "serena": {
      "url": "http://localhost:9121/mcp"
    }
  }
}
```

Restart Claude Desktop after saving.

### Codex (CLI / App)

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.serena]
url = "http://localhost:9121/mcp"
```

### Generic HTTP MCP Clients

Any MCP client that supports Streamable HTTP transport connects with:

```
http://localhost:9121/mcp
```

After connecting, ask the agent to *"Activate the project using Serena"* and
specify which workspace project (e.g. `seavista-core`, `seavista-ops-view`).

## Projects

Each mounted repo under `/workspace/` is an independent Serena project:

- `/workspace/seavista-core`
- `/workspace/seavista-simulator`
- `/workspace/seavista-triton`
- `/workspace/seavista-ops-view`
- `/workspace/seavista-ops-relay`
- `/workspace/seavista-ops-awareness`
- `/workspace/seavista-ray-orchestrator`
- `/workspace/seavista-tracklets`
- `/workspace/seavista-seq2seq`
- `/workspace/Seavista_Layers`

Add/remove projects in your local `docker-compose.projects.yml` (copied from `docker-compose.projects.example.yml`).

## Configuration

Serena config persists in the `serena-config` named volume (`/workspaces/serena/config` in container).

## Custom Ports

```bash
SERENA_PORT=9200 SERENA_DASHBOARD_PORT=25000 \
  docker compose -f docker-compose.yml -f docker-compose.projects.yml up -d
```

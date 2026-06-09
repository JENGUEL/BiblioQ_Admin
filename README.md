# BiblioQ Admin Dashboard

Separate Flet app for managing remote BiblioQ installations via Supabase.

## Quick start

```powershell
cd BiblioQ_Admin
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Default local login: `admin` / `changeme`

---

## Supabase setup (Dashboard)

### 1. Database schema

1. Open [Supabase Dashboard](https://supabase.com/dashboard) → your project
2. **SQL Editor** → New query
3. Paste and run [`scripts/supabase_migrations/001_initial.sql`](scripts/supabase_migrations/001_initial.sql)
4. Confirm tables under **Table Editor**: `installations`, `licenses`, `commands`, etc.

### 2. Edge function secrets

**Edge Functions → Secrets** — add only these two (do **not** add `SUPABASE_*` names; Supabase injects those automatically):

| Name | Value |
|---|---|
| `AGENT_API_KEY` | Random string (see below) |
| `ADMIN_API_TOKEN` | Random string (see below) |

Generate tokens locally:

```powershell
powershell -File scripts\generate_api_tokens.ps1
```

### 3. Deploy edge functions

Create/deploy **five** functions in the dashboard (or via CLI):

| Function | Source file |
|---|---|
| `agent_checkin` | `supabase/functions/agent_checkin/index.ts` |
| `agent_command_result` | `supabase/functions/agent_command_result/index.ts` |
| `agent_crash_report` | `supabase/functions/agent_crash_report/index.ts` |
| `admin_revoke_license` | `supabase/functions/admin_revoke_license/index.ts` |
| `admin_queue_command` | `supabase/functions/admin_queue_command/index.ts` |

CLI (after `supabase login` + `supabase link`):

```powershell
.\scripts\deploy_supabase.ps1 functions
```

**Important:** Edge function source must use `//` comments (not `#`). In the dashboard, disable **JWT verification** for agent/admin functions (they use `x-agent-key` / `x-admin-token` instead), or deploy with `--no-verify-jwt`.

### 4. API keys (Settings → API)

Copy from **Legacy** tab:

- **Project URL** → `https://YOUR_PROJECT.supabase.co`
- **service_role** JWT → admin app only (never on client PCs)

---

## Admin app Settings

Open **Settings** in the admin app:

| Field | Value |
|---|---|
| Supabase URL | `https://YOUR_PROJECT.supabase.co` (no `/rest/v1/`) |
| Service role key | Legacy `service_role` JWT |
| Admin API token | Same as `ADMIN_API_TOKEN` secret |
| Agent API key | Same as `AGENT_API_KEY` secret |

- Click **Test connection** — tests current fields and auto-saves on success
- Click **Create agent config on this PC** — writes agent `config.json` locally

---

## Client agent

### Option A: BiblioQ_Setup.exe (3.0.1+, recommended for school PCs)

The main BiblioQ installer bundles `BiblioQAgent.exe` and `BiblioQAgentSvc.exe`. On the **Remote Management** wizard page (or silent `/SUPABASEURL=` + `/AGENTKEY=`), IT enters the Supabase URL and Agent API key. The installer writes `%ProgramData%\BiblioQ\agent\config.json` (and mirrors to LocalAppData) and registers the **BiblioQ Remote Agent** Windows service.

Build the agent with `pywin32` installed (`pip install -r agent/requirements_agent.txt`); `build_agent.py` bundles pywin32 into `BiblioQAgentSvc.exe` and smoke-tests the service binary.

From 3.0.3+, setup also registers a **headless PowerShell logon task** (`BiblioQAgentLogon`) and HKCU Run key using `%ProgramData%\BiblioQ\agent\start_agent.ps1`. Agent check-in defaults to **30 seconds**.

### Repair agent startup (manual)

If the agent is not running after an update:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_agent_startup.ps1 -InstallDir "C:\Program Files\BiblioQ"
```

Manual agent setup on client PCs is only needed for dev/testing or pre-3.0.1 installs.

### Option B: From admin Settings (dev / single PC)

Click **Create agent config on this PC** after filling URL + Agent API key.

### Option C: Script

```powershell
python scripts/setup_agent_config.py
# Or with overrides:
python scripts/setup_agent_config.py --url https://YOUR_PROJECT.supabase.co --agent-key YOUR_KEY
```

Config is written to `%LOCALAPPDATA%\BiblioQ\agent\config.json` (no service role key on clients).

### Run agent (dev / debug)

```powershell
pip install -r agent/requirements_agent.txt
python agent/agent.py
```

Install as Windows service manually (Administrator, dev only — production uses BiblioQ_Setup.exe):

```powershell
.\agent\installer_agent.ps1
```

Build frozen agent exes for the main release:

```powershell
python scripts/build_agent.py --output-dir=../../dist/BiblioQ/agent
```

---

## Verify end-to-end

1. Run agent once → **Installations** page shows your PC (or check `installations` table)
2. Admin app → **Installations** → **Revoke** on a machine
3. Wait up to 5 minutes (or restart agent)
4. Launch BiblioQ → blocked with revoke message

---

## Architecture

- **Admin app**: Flet UI, bcrypt login, Supabase REST/RPC (service role)
- **Agent**: Outbound HTTPS to edge functions only (`x-agent-key`), 5-minute poll
- **BiblioQ client**: Writes `agent_state.json`, reads `license_revoked.json`

Tailscale remote access is Phase 5 (deferred). See [`agent/TAILSCALE.md`](agent/TAILSCALE.md).

---

## CLI install (optional)

If `supabase` is not on PATH:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_supabase_cli.ps1
```

Use full path if needed:

```powershell
& "$env:LOCALAPPDATA\Programs\supabase\supabase.exe" login
```

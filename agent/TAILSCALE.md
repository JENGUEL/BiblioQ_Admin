# Tailscale remote access (Phase 5)

Deferred until Phases 1-4 are stable.

Planned flow:
1. Admin generates Tailscale auth key in Settings.
2. Agent receives `install_tailscale` command (allowlisted installer only).
3. Agent reports `tailscale_ip` on check-in.
4. Admin UI shows copy SSH command: `tailscale ssh user@host`.

Do not open inbound SSH ports on school networks.

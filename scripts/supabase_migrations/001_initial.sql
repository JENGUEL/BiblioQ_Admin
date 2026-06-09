-- BiblioQ Admin: initial schema
-- Run in Supabase SQL Editor or via supabase db push

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS installations (
    machine_id      TEXT PRIMARY KEY,
    hostname        TEXT NOT NULL DEFAULT '',
    os_version      TEXT NOT NULL DEFAULT '',
    ip_last         TEXT NOT NULL DEFAULT '',
    biblioq_version TEXT NOT NULL DEFAULT '',
    license_key     TEXT,
    agent_version   TEXT NOT NULL DEFAULT '',
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'revoked', 'offline', 'suspended')),
    tailscale_ip    TEXT,
    biblioq_running BOOLEAN NOT NULL DEFAULT FALSE,
    last_seen_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS licenses (
    key             TEXT PRIMARY KEY,
    school          TEXT NOT NULL DEFAULT '',
    duration_days   INTEGER,
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'revoked', 'expired', 'suspended')),
    machine_id      TEXT REFERENCES installations(machine_id) ON DELETE SET NULL,
    revoked_at      TIMESTAMPTZ,
    revoke_message  TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS commands (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id      TEXT NOT NULL REFERENCES installations(machine_id) ON DELETE CASCADE,
    action          TEXT NOT NULL,
    params          JSONB NOT NULL DEFAULT '{}',
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'sent', 'acked', 'failed', 'cancelled')),
    created_by      TEXT NOT NULL DEFAULT 'admin',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sent_at         TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_commands_machine_status ON commands(machine_id, status);

CREATE TABLE IF NOT EXISTS command_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_id      UUID NOT NULL REFERENCES commands(id) ON DELETE CASCADE,
    machine_id      TEXT NOT NULL REFERENCES installations(machine_id) ON DELETE CASCADE,
    status          TEXT NOT NULL CHECK (status IN ('success', 'failed')),
    output          TEXT NOT NULL DEFAULT '',
    completed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crash_reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id      TEXT NOT NULL REFERENCES installations(machine_id) ON DELETE CASCADE,
    app_version     TEXT NOT NULL DEFAULT '',
    error_type      TEXT NOT NULL DEFAULT '',
    stack_trace     TEXT NOT NULL DEFAULT '',
    resolved        BOOLEAN NOT NULL DEFAULT FALSE,
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_crash_reports_machine ON crash_reports(machine_id);
CREATE INDEX IF NOT EXISTS idx_crash_reports_resolved ON crash_reports(resolved);

CREATE TABLE IF NOT EXISTS admin_users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username        TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor           TEXT NOT NULL DEFAULT 'admin',
    action          TEXT NOT NULL,
    target_type     TEXT NOT NULL DEFAULT '',
    target_id       TEXT NOT NULL DEFAULT '',
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_api_keys (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key_hash        TEXT NOT NULL UNIQUE,
    label           TEXT NOT NULL DEFAULT 'default',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS installations_updated_at ON installations;
CREATE TRIGGER installations_updated_at
    BEFORE UPDATE ON installations FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS licenses_updated_at ON licenses;
CREATE TRIGGER licenses_updated_at
    BEFORE UPDATE ON licenses FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION agent_checkin(payload JSONB)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    mid TEXT := payload->>'machine_id';
    pending JSONB;
    lic_status TEXT := 'active';
BEGIN
    IF mid IS NULL OR length(mid) < 8 THEN
        RAISE EXCEPTION 'invalid machine_id';
    END IF;

    INSERT INTO installations (
        machine_id, hostname, os_version, ip_last, biblioq_version,
        license_key, agent_version, status, biblioq_running, last_seen_at
    ) VALUES (
        mid,
        COALESCE(payload->>'hostname', ''),
        COALESCE(payload->>'os_version', ''),
        COALESCE(payload->>'ip', ''),
        COALESCE(payload->>'biblioq_version', ''),
        NULLIF(payload->>'license_key', ''),
        COALESCE(payload->>'agent_version', ''),
        'active',
        COALESCE((payload->>'biblioq_running')::boolean, false),
        NOW()
    )
    ON CONFLICT (machine_id) DO UPDATE SET
        hostname = EXCLUDED.hostname,
        os_version = EXCLUDED.os_version,
        ip_last = EXCLUDED.ip_last,
        biblioq_version = EXCLUDED.biblioq_version,
        license_key = COALESCE(EXCLUDED.license_key, installations.license_key),
        agent_version = EXCLUDED.agent_version,
        biblioq_running = EXCLUDED.biblioq_running,
        last_seen_at = NOW(),
        status = CASE
            WHEN installations.status = 'revoked' THEN 'revoked'
            ELSE 'active'
        END;

    IF payload->>'license_key' IS NOT NULL AND payload->>'license_key' <> '' THEN
        INSERT INTO licenses (key, school, status)
        VALUES (payload->>'license_key', '', 'active')
        ON CONFLICT (key) DO NOTHING;
    END IF;

    SELECT status INTO lic_status FROM installations WHERE machine_id = mid;

    UPDATE commands SET status = 'sent', sent_at = NOW()
    WHERE machine_id = mid AND status = 'pending';

    SELECT COALESCE(jsonb_agg(jsonb_build_object(
        'command_id', c.id,
        'action', c.action,
        'params', c.params
    )), '[]'::jsonb)
    INTO pending
    FROM commands c
    WHERE c.machine_id = mid AND c.status = 'sent';

    RETURN jsonb_build_object(
        'pending_commands', pending,
        'license_status', lic_status
    );
END;
$$;

CREATE OR REPLACE FUNCTION agent_command_result(payload JSONB)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    cid UUID := (payload->>'command_id')::uuid;
BEGIN
    INSERT INTO command_results (command_id, machine_id, status, output)
    VALUES (
        cid,
        payload->>'machine_id',
        payload->>'status',
        COALESCE(payload->>'output', '')
    );
    UPDATE commands SET
        status = CASE WHEN payload->>'status' = 'success' THEN 'acked' ELSE 'failed' END,
        completed_at = NOW()
    WHERE id = cid;
    RETURN jsonb_build_object('ok', true);
END;
$$;

CREATE OR REPLACE FUNCTION admin_revoke_license(
    p_license_key TEXT,
    p_machine_id TEXT,
    p_message TEXT,
    p_actor TEXT DEFAULT 'admin'
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    cmd_id UUID;
    mid TEXT := p_machine_id;
BEGIN
    UPDATE licenses SET
        status = 'revoked',
        revoked_at = NOW(),
        revoke_message = p_message
    WHERE key = p_license_key;

    IF mid IS NOT NULL THEN
        UPDATE installations SET status = 'revoked' WHERE machine_id = mid;
        INSERT INTO commands (machine_id, action, params, created_by)
        VALUES (mid, 'revoke_license', jsonb_build_object('message', p_message), p_actor)
        RETURNING id INTO cmd_id;
    END IF;

    INSERT INTO audit_log (actor, action, target_type, target_id, metadata)
    VALUES (p_actor, 'revoke_license', 'license', p_license_key,
            jsonb_build_object('machine_id', mid, 'message', p_message));

    RETURN jsonb_build_object('command_id', cmd_id, 'ok', true);
END;
$$;

ALTER TABLE installations ENABLE ROW LEVEL SECURITY;
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE commands ENABLE ROW LEVEL SECURITY;
ALTER TABLE command_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE crash_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_api_keys ENABLE ROW LEVEL SECURITY;

-- Default admin password: changeme (change immediately)
INSERT INTO admin_users (username, password_hash)
VALUES (
    'admin',
    '$2b$12$d8af0vh9fdFRAawDlJ23cu35djuZE2VQmOTL1baI.NmrsKhHXpNVu'
)
ON CONFLICT (username) DO NOTHING;

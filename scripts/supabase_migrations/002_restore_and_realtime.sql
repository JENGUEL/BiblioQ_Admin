-- License restore + Realtime publication (see supabase/migrations/20250608120000_restore_and_realtime.sql)

CREATE OR REPLACE FUNCTION admin_restore_license(
    p_license_key TEXT,
    p_machine_id TEXT,
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
        status = 'active',
        revoked_at = NULL,
        revoke_message = NULL,
        updated_at = NOW()
    WHERE key = p_license_key;

    IF mid IS NOT NULL THEN
        UPDATE installations SET status = 'active', updated_at = NOW() WHERE machine_id = mid;
        INSERT INTO commands (machine_id, action, params, created_by)
        VALUES (mid, 'clear_revoke', '{}'::jsonb, p_actor)
        RETURNING id INTO cmd_id;
    END IF;

    INSERT INTO audit_log (actor, action, target_type, target_id, metadata)
    VALUES (p_actor, 'restore_license', 'license', p_license_key,
            jsonb_build_object('machine_id', mid));

    RETURN jsonb_build_object('command_id', cmd_id, 'ok', true);
END;
$$;

DO $$
BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE commands;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE command_results;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE installations;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

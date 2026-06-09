// Supabase Edge Function: admin_queue_command

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const ADMIN_TOKEN = Deno.env.get("ADMIN_API_TOKEN") ?? "";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "authorization, x-admin-token, content-type",
      },
    });
  }

  const token = req.headers.get("x-admin-token") ?? "";
  if (ADMIN_TOKEN && token !== ADMIN_TOKEN) {
    return new Response(JSON.stringify({ error: "unauthorized" }), { status: 401 });
  }

  try {
    const body = await req.json();
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "",
    );

    const { data, error } = await supabase
      .from("commands")
      .insert({
        machine_id: body.machine_id,
        action: body.action,
        params: body.params ?? {},
        created_by: body.actor ?? "admin",
        status: "pending",
      })
      .select("id")
      .single();
    if (error) throw error;

    await supabase.from("audit_log").insert({
      actor: body.actor ?? "admin",
      action: "queue_command",
      target_type: "command",
      target_id: data.id,
      metadata: { machine_id: body.machine_id, action: body.action },
    });

    return new Response(JSON.stringify({ command_id: data.id, ok: true }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500 });
  }
});

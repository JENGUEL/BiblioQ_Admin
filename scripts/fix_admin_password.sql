-- Fix admin login when seed hash did not match password "changeme"
UPDATE admin_users
SET password_hash = '$2b$12$d8af0vh9fdFRAawDlJ23cu35djuZE2VQmOTL1baI.NmrsKhHXpNVu'
WHERE username = 'admin';

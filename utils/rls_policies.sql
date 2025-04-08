-- Function to check if RLS is enabled on a table
CREATE OR REPLACE FUNCTION check_rls_enabled(table_name text)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  rls_enabled boolean;
BEGIN
  SELECT relrowsecurity INTO rls_enabled
  FROM pg_class
  WHERE oid = (table_name::regclass);
  
  RETURN jsonb_build_object('rls_enabled', rls_enabled);
END;
$$;

-- Secure RLS policy for subscriptions table
ALTER TABLE IF EXISTS subscriptions ENABLE ROW LEVEL SECURITY;

-- Allow users to only see their own subscriptions
DROP POLICY IF EXISTS "Users can only view their own subscriptions" ON subscriptions;
CREATE POLICY "Users can only view their own subscriptions"
  ON subscriptions
  FOR SELECT
  USING (auth.uid() = user_id);

-- Allow users to only update their own subscriptions
DROP POLICY IF EXISTS "Users can only update their own subscriptions" ON subscriptions;
CREATE POLICY "Users can only update their own subscriptions"
  ON subscriptions
  FOR UPDATE
  USING (auth.uid() = user_id);

-- Secure RLS policy for security_logs table
ALTER TABLE IF EXISTS security_logs ENABLE ROW LEVEL SECURITY;

-- Allow users to only see their own security logs
DROP POLICY IF EXISTS "Users can only view their own security logs" ON security_logs;
CREATE POLICY "Users can only view their own security logs"
  ON security_logs
  FOR SELECT
  USING (auth.uid() = user_id);

-- Allow users to only insert their own security logs
DROP POLICY IF EXISTS "Users can only insert their own security logs" ON security_logs;
CREATE POLICY "Users can only insert their own security logs"
  ON security_logs
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Secure RLS policy for site_pages table
ALTER TABLE IF EXISTS site_pages ENABLE ROW LEVEL SECURITY;

-- Allow public read access to site_pages
DROP POLICY IF EXISTS "Allow public read access" ON site_pages;
CREATE POLICY "Allow public read access"
  ON site_pages
  FOR SELECT
  TO public;

-- Allow authenticated users to insert their own site pages
DROP POLICY IF EXISTS "Users can insert their own site pages" ON site_pages;
CREATE POLICY "Users can insert their own site pages"
  ON site_pages
  FOR INSERT
  WITH CHECK (auth.uid() = (metadata->>'user_id')::uuid);

-- Allow authenticated users to update their own site pages
DROP POLICY IF EXISTS "Users can update their own site pages" ON site_pages;
CREATE POLICY "Users can update their own site pages"
  ON site_pages
  FOR UPDATE
  USING (auth.uid() = (metadata->>'user_id')::uuid);

-- Allow authenticated users to delete their own site pages
DROP POLICY IF EXISTS "Users can delete their own site pages" ON site_pages;
CREATE POLICY "Users can delete their own site pages"
  ON site_pages
  FOR DELETE
  USING (auth.uid() = (metadata->>'user_id')::uuid);

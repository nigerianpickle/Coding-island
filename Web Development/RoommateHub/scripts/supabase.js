import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

// ⚠️ Replace with your actual Supabase project details:
const SUPABASE_URL = "https://lldolodllxfnkbcrsfzh.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxsZG9sb2RsbHhmbmtiY3JzZnpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3ODgwMzcsImV4cCI6MjA3NjM2NDAzN30.1BqyM8F2LfKqt0On9oN4FD9c5EJ-8GL2ZJn9h9czdIk";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

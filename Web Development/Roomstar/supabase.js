// import { createClient } from '@supabase/supabase-js'
// import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
const supabaseUrl = 'https://zigqiybygrsnorfhzdsq.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppZ3FpeWJ5Z3Jzbm9yZmh6ZHNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwNDcyMjUsImV4cCI6MjA3NjYyMzIyNX0.7ds492oG1dx-bt46vsO7vVYU95_CCXUFUEY6OyqAp_M'
// const supabase = createClient(supabaseUrl, supabaseKey)


// ✅ Export a named constant called "supabase"
export const supabase = createClient(supabaseUrl, supabaseKey);
from supabase import create_client

URL = "https://nvkfhlqvxugsqhgrasrk.supabase.co"

KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im52a2ZobHF2eHVnc3FoZ3Jhc3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI5MTE5ODIsImV4cCI6MjA4ODQ4Nzk4Mn0.fUkb85LGf3EAecJmv8Lru1XMt1uHdP3cuNxGZwTshuM"


supabase = create_client(URL, KEY)
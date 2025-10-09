from pathlib import Path
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Resolve project base and load env vars
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, 'app', '.env'))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment.")

# Singleton Supabase client for reuse across the project
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



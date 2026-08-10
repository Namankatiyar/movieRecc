from dotenv import load_dotenv
import os
import vecs

load_dotenv()
db_pass = os.getenv("DB_PASSWORD")

DB_CONNECTION = f"postgresql://postgres.yynkzwxttjasrwcjptmg:{db_pass}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

vx = vecs.create_client(DB_CONNECTION)
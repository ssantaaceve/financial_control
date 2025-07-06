
from supabase import create_client

# 👇 Reemplaza por tus datos reales
url = "https://hzkpfmguqfoleedqfatt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6a3BmbWd1cWZvbGVlZHFmYXR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzMDgyNDAsImV4cCI6MjA2Njg4NDI0MH0.x3WGCNgwuWr7JZiR_Quuh0JIw4o2hOuMo3bSGDcilYE"

supabase = create_client(url, key)

# Probar lectura
res = supabase.table("usuarios").select("*").limit(1).execute()
print(res.data)

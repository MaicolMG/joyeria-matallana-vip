import os
from dotenv import load_dotenv

load_dotenv()

# URL base de la API REST (Node.js/Express)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000/api")

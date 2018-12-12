from dotenv import load_dotenv
load_dotenv()
import os

db_name = os.getenv("DBNAME")
db_user = os.getenv("USERNAME")
db_pw = os.getenv("PW")
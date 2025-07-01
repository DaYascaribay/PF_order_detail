import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    ORDER_CREATION_URL = os.getenv("ORDER_CREATION_URL")
    ORDER_STATUS_URL = os.getenv("ORDER_STATUS_URL")

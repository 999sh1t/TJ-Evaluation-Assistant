import os
DATA_DIR   = os.path.join(os.getcwd(), ".tj_evaluation_system")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
os.makedirs(DATA_DIR, exist_ok=True)
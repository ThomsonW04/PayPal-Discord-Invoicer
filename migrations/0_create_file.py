import os

os.makedirs(f"{os.getcwd()}/data", exist_ok=True)
with open(f"{os.getcwd()}/data/db.sqlite", "w"):
    pass

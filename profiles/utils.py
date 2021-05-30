import uuid

def get_random_code():    # for slug in models.py
    code = str(uuid.uuid4())[:8].replace('-','').lower()
    return code

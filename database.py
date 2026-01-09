# Auto Approval Bot Database

from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

users = client['main']['users']
groups = client['main']['groups']
sessions = client['main']['sessions']  # For storing user login sessions

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        if not group:
            return False
        return True

def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def add_group(chat_id):
    in_db = already_dbg(chat_id)
    if in_db:
        return
    return groups.insert_one({"chat_id": str(chat_id)})

def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

# Session management functions
def save_session(user_id, session_string, phone_number):
    """Save user's Pyrogram session to database"""
    sessions.update_one(
        {"user_id": str(user_id)},
        {"$set": {
            "user_id": str(user_id),
            "session_string": session_string,
            "phone_number": phone_number
        }},
        upsert=True
    )

def get_session(user_id):
    """Get user's saved session from database"""
    session = sessions.find_one({"user_id": str(user_id)})
    return session

def delete_session(user_id):
    """Delete user's session from database"""
    return sessions.delete_one({"user_id": str(user_id)})

def is_logged_in(user_id):
    """Check if user has a saved session"""
    session = sessions.find_one({"user_id": str(user_id)})
    return session is not None

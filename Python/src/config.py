premium_users = {
    ".user1": "xyzsworld",
    "user2": "fuckyou456"
}

def is_premium_user(username, password):
    return username in premium_users and premium_users[username] == password
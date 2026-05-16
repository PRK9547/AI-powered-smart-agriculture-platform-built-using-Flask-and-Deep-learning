users = []

def register_user(username, password, role):
    # check if user already exists
    for user in users:
        if user["username"] == username:
            return False
    
    users.append({
        "username": username,
        "password": password,
        "role": role
    })
    return True


def login_user(username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None
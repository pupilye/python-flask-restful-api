from werkzeug.security import safe_str_cmp
from models.user import UserModel

# users = [
#     User(1, 'bob', 'asdf')
# ]

# username_mapping = {u.username: u for u in users} # set comprehension, assigning key-value pair
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = UserModel.find_by_username(username) # Another way to get item from dics
    if user and safe_str_cmp(user.password, password): 
        # not a good idea to compare string with == in python, especially with encoding/different environment
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
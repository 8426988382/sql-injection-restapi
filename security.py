from user import User


def authenticate(username, password):

    # TODO: CHECK FOR Login Bypass
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    _id = payload['identity']
    user = User.find_by_userid(_id)
    return user

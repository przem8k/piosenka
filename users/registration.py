import sha
import random


def generate_activation_key(username):
    salt = sha.new(str(random.random())).hexdigest()[:5]
    return sha.new(salt + username.encode('ascii', 'ignore')).hexdigest()

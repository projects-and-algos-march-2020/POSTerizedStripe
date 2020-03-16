import re
# from app import User
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def validate(post):
    errors = []

    if len(post['first_name']) < 2:
        errors.append("First name must be at least 2 characters")
        valid = False

    if len(post['last_name']) < 2:
        errors.append("Last name must be at least 2 characters")
        valid = False

    if not EMAIL_REGEX.match(post['email']):
        errors.append("Email must be valid")
        valid = False

    if len(post['password']) < 8:
        errors.append("Password must be at least 8 characters")
        valid = False

    # if User.query.filter_by(email=post["email"]):
    #     errors.append("Email is in use")
    
    if post['password'] != post['confirm']:
        errors.append("Passwords must match")
        valid = False

    return errors
import bcrypt
from db import cursor_obj, conn_obj

def signup_user(name,email,password):

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    query = """
    INSERT INTO users(name,email,password)
    VALUES(%s,%s,%s)
    """

    values = (
        name,
        email,
        hashed_password.decode()
    )

    cursor_obj.execute(query,values)

    conn_obj.commit()

def login_user(email,password):

    query = """
    SELECT * FROM users
    WHERE email=%s
    """

    values = (email,)

    cursor_obj.execute(query,values)

    user = cursor_obj.fetchone()

    if user:

        stored_password = user["password"]

        is_correct = bcrypt.checkpw(
            password.encode(),
            stored_password.encode()
        )

        if is_correct:
            return user

    return None
import bcrypt

password = 'yimnaiconrad123'
password_bytes = password.encode('utf-8')

salt = bcrypt.gensalt()
hashed_psswd = bcrypt.hashpw(password_bytes, salt)
print(hashed_psswd.decode("utf-8"))


bcrypt.checkpw()
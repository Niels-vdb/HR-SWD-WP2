from app import bcrypt, query_model

f_name = "John"
infix = ""
l_name = "Doe"
email = "admin@email.com"
password = bcrypt.generate_password_hash("werkplaats2").decode("utf-8")

query_model.set_new_user(f_name, infix, l_name, email, password, True)
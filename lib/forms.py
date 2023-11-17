from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, EmailField, StringField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = EmailField("Email:", validators=[Email(), Length(min=8, max=50)])
    password = PasswordField(
        "Password:", validators=[InputRequired(), Length(min=8, max=80)]
    )
    remember = BooleanField("Onthoud mij")


class SubmitForm(FlaskForm):
    first_name = StringField(
        "Voornaam", validators=[InputRequired(), Length(min=2, max=20)]
    )
    infix = StringField("Tussenvoegsel", validators=[Length(min=2, max=20)])
    last_name = StringField(
        "Achternaam", validators=[InputRequired(), Length(min=2, max=20)]
    )
    email = EmailField("Email", validators=[Email(), Length(min=8, max=50)])
    password = PasswordField(
        "Password:", validators=[InputRequired(), Length(min=8, max=80)]
    )
    herhaal_password = PasswordField(
        "Herhaal password:", validators=[InputRequired(), Length(min=8, max=80)]
    )
    admin = BooleanField("Admin")

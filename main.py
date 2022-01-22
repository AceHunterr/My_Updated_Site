
import smtplib
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email
import os


class LoginForm(FlaskForm):
    email = StringField(label='Email Address', validators=[DataRequired("This field is required"),
                                                           Email("Please enter an valid email address.")])
    name = StringField(label='Name', validators=[DataRequired("This field is required")])
    message = StringField(label='Message', validators=[DataRequired("This field is required")])


app = Flask(__name__)
my_email = "acehunter500@gmail.com"
password = os.environ["MAIL_PASSWORD"]
app.secret_key = os.environ["APP_SECRET_KEY"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact_page", methods=["GET", "POST"])
def contact_page():
    login_form = LoginForm()
    login_form.validate_on_submit()
    if login_form.validate_on_submit():
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        send_mail_to_me(name, email, phone, message)
        send_mail_to_the_person(name, email)
        return render_template("contact-page.html", msg_sent=True, form=login_form)
    return render_template("contact-page.html", msg_sent=False, form=login_form)
    # return render_template("login.html", form=login_form)


def send_mail_to_the_person(name, email):
    email_message = f"Subject:Hola Fellow\n\nThank You {name} for visiting my site your response has recorded.\n" \
                    f"This is my personal email: aggarwalmehul26@gmail.com. You can contact me directly through here.\n" \
                    f"If you find me interesting make sure to contact me ;)"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=email_message
        )


def send_mail_to_me(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=email_message
        )


@app.route('/about_page')
def about_page():
    return render_template("about-page.html")


@app.route('/education_page')
def education_page():
    return render_template("education-page.html")


@app.route('/skills_page')
def skills_page():
    return render_template("skills-page.html")


if __name__ == "__main__":
    app.run(debug=True)

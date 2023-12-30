from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


# create login form
class LoginForm(FlaskForm):
  email=StringField(label="Email", validators=[DataRequired(), Email()])
  password = PasswordField(label="Password", validators=[DataRequired()])
  submit = SubmitField(label="Login")

# create register form
class RegisterForm(FlaskForm):
  name = StringField(label="Full Name", validators=[DataRequired()])
  age = IntegerField(label="Age", validators=[DataRequired()])
  sex = StringField(label="Sex", validators=[DataRequired()]) 
  phone = IntegerField(label="Phone Number", validators=[DataRequired()])
  email = StringField(label="Email" , validators=[DataRequired(), Email()])
  title = StringField(label="Job Title", validators=[DataRequired()])
  location = StringField(label="Location", validators=[DataRequired()])
  experience = IntegerField(label="Years of Experience", validators=[DataRequired()])
  linkedIn = StringField(label="LinkedIn Profile", validators=[])
  resume = StringField(label="Upload Your Resume", validators=[])
  photo = StringField(label="Upload Your Photo", validators=[]) 
  reg_num = StringField(label="Registration Number", validators=[DataRequired()])
  password = PasswordField(label="Password", validators= [DataRequired()])
  con_password = PasswordField(label="Confirm Password", validators= [DataRequired()])
  submit = SubmitField(label="Register")
  
# create contact form 
class ContactForm(FlaskForm):
  name = StringField(label="Full Name", validators=[DataRequired()])
  email = StringField(label="Email", validators=[DataRequired(), Email()])
  message = TextAreaField(label="Message", validators=[DataRequired()])
  submit = SubmitField(label="Send")


# create job post form
class JobPostForm(FlaskForm):
  title = StringField(label="Job Title", validators=[DataRequired()])
  location = StringField(label="Location" , validators=[DataRequired()])
  facility = StringField(label="Facility", validators=[DataRequired()])
  time = StringField(label="Night Shift/ Day Shift", validators=[DataRequired()])
  duration = IntegerField(label="Duration in Hours", validators=[DataRequired()])
  description = TextAreaField(label="Job Description", validators=[DataRequired()])
  responsibilities = TextAreaField(label="Job Responsibilities", validators=[DataRequired()])
  requirements = TextAreaField(label="Job Requirements", validators=[DataRequired()])
  salary = IntegerField(label="Salary", validators=[DataRequired()])
  currency = StringField(label="Currency", validators=[DataRequired()])
  submit = SubmitField(label="Post Job")

# create FAQ form
class FAQForm(FlaskForm):
  question = StringField(label="Question", validators=[])
  answer = TextAreaField(label="Answer", validators=[])

# create profile form

# create aply  job form

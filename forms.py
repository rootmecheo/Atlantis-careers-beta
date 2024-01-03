from datetime import datetime
import pytz
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
  submit = SubmitField(label="Submit Job")

# create FAQ form
class FAQForm(FlaskForm):
  question = StringField(label="Question", validators=[])
  answer = TextAreaField(label="Answer", validators=[])

# create profile form

# create aply  job form

def format_time_difference(timestamp):
  # Convert the datetime object to Nairobi timezone
  nairobi_tz = pytz.timezone('Africa/Nairobi')
  timestamp = pytz.utc.localize(timestamp).astimezone(nairobi_tz)

  # Get the current time in Nairobi timezone
  current_time = datetime.now(nairobi_tz)

  # Calculate the time difference
  time_difference = current_time - timestamp

  # Extract time difference in days, hours, and minutes
  days = time_difference.days
  total_seconds = time_difference.total_seconds()
  hours = total_seconds // 3600
  minutes = (total_seconds % 3600) // 60

  if days >= 365:
      years = days // 365
      return f"{years} years ago"
  elif days >= 28:
      months = days // 30
      return f"{months} months ago"
  elif days >= 7:
      weeks = days // 7
      return f"{weeks} weeks ago"
  elif days >= 1:
      return f"{days} days ago"
  elif hours >= 1:
      return f"{int(hours)} hours ago"
  else:
      return f"{int(minutes)} minutes ago"

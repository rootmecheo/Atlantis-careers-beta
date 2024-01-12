import os 
from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash

#from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from database import (
  add_client,
  add_job_to_db,
  load_clients_from_db,
  load_jobs_from_db,
  remove_job_from_db,
  update_job_in_db,
 Base, engine, User, Post, Application, Review
)
from forms import (
  ContactForm,
  FAQForm,
  JobPostForm,
  LoginForm,
  RegisterForm,
  format_time_difference,
)

app = Flask(__name__)
app.secret_key = "atlantis@2023"
Bootstrap(app)

with app.app_context():
  Base.metadata.create_all(bind=engine)

current_year = datetime.now().year


@app.route('/')
def home():
  jobs = load_jobs_from_db()
  
  for job in jobs:
      timestamp = job['created_at']
      time_difference = format_time_difference(timestamp)
      job['time_difference'] = time_difference  

  return render_template('home.html', jobs=jobs, year=current_year)

@app.route('/clients')
def clients_list():
  clients = load_clients_from_db()

  for client in clients:
    timestamp = client['created_at']
    time_difference = format_time_difference(timestamp)
    client['time_difference'] = time_difference
  #return jsonify(clients)
  return render_template('clients.html', year=current_year, clients=clients)

@app.route("/login", methods=["POST", "GET"])
def login():
  form=LoginForm ()
  if form.validate_on_submit():
    return redirect(url_for("home"))
  return render_template('login.html', form=form, year=current_year)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()  # Initialize form here
    if request.method == "POST" and form.validate_on_submit():
        # data = request.form 
        data = request.form.to_dict(flat=True)  # Convert ImmutableMultiDict to a dictionary

        # Hash the password before adding the client to the database
        hashed_password = generate_password_hash(data["password"], method='pbkdf2:sha256', salt_length=8)
        data["password"] = hashed_password  # Replace the original password with the hashed one

        add_client(data)  # Add the client to the database
        return redirect(url_for("home"))
    return render_template("register.html", form=form, year=current_year)


@app.route("/job_post", methods=["POST", "GET"])
def job_post():
  form=JobPostForm()
  if request.method == "POST" and form.validate_on_submit():
    data = request.form
    add_job_to_db(data)
    return redirect(url_for("home"))
  return render_template('job_post.html', form=form, year=current_year)

@app.route("/job/<int:id>/delete")
def delete_job(id):
    # Assuming load_jobs_from_db returns the job with the given id
  job = load_jobs_from_db(id)[0]

  if job:
    remove_job_from_db(id)
    return redirect(url_for("home"))  
  else:
    return ' did not successfully delete you idiot'

@app.route("/job/<int:id>/update", methods=["POST", "GET"])
def update_job(id):
    form = JobPostForm()
    job = load_jobs_from_db(id)[0]  # Fetch the job details from the database
    # return jsonify(job)

    if request.method == "POST":
        new_data = request.form
        update_job_in_db(id, new_data)
        return redirect('/')  # Redirect to the home page 
    else:
        # Populate the form fields with the existing job data
        return render_template("update_job.html", job=job, form=form, year=current_year)


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)
 
@app.route("/contact_us", methods=["POST", "GET"])
def contact_us():  
  form = ContactForm()
  if form.validate_on_submit():
    # send email
    return redirect(url_for("home"))
  return render_template(
    'contact_us.html', form=form, year=current_year)

@app.route("/faq", methods=["POST", "GET"])
def faq():
  form = FAQForm()
  return render_template("faq.html", form=form, year=current_year)

@app.route("/search")
def search_results():
  jobs = load_jobs_from_db()
  
  for job in jobs:
    timestamp = job['created_at']
    time_difference = format_time_difference(timestamp)
    job['time_difference'] = time_difference  

  return render_template("search_results.html", jobs=jobs, year=current_year)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

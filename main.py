from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap5

from database import add_client, add_job_to_db, load_jobs_from_db, remove_job_from_db

from forms import ContactForm, FAQForm, JobPostForm, LoginForm, RegisterForm

app = Flask(__name__)
app.secret_key = "atlantis@2023"
Bootstrap5(app)

current_year = datetime.now().year

@app.route('/')
def home():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs, year=current_year)

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
    data = request.form
    add_client(data)
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
def delete_job(jobID):
    # Assuming load_jobs_from_db returns the job with the given id
  job = load_jobs_from_db(jobID)[0]

  if job:
    remove_job_from_db(id)
    return jsonify(job)
    # return redirect(url_for("home"))  
  else:
    return ' did not successfully delete you idiot'

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
  return render_template("search_results.html", jobs=jobs, year=current_year)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)


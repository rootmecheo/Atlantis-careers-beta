import os

from sqlalchemy import create_engine, text

# retrieve environment variable
db_connection_string = os.environ["DB_CONNECTION_STRING"]


engine = create_engine(
  db_connection_string,
  connect_args= {
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem",
        }
    } ) 

# insert client to db
def add_client(data):
  with engine.connect() as conn:
    query = text("insert into clients(name, age, sex, phone, email, title, location, experience, linkedin, resume, photo, reg_num, password) values(:name, :age, :sex, :phone, :email, :title, :location, :experience, :linkedin, :resume, :photo, :reg_num, :password)")
    conn.execute(query, {
      "name": data["name"],
      "age": data["age"],
      "sex": data["sex"],
      "phone": data["phone"],
      "email": data["email"],
      "title": data["title"],
      "location": data["location"],
      "experience": data["experience"],
      "linkedin": data["linkedIn"],
      "resume": data["resume"],
      "photo": data["photo"],
      "reg_num": data["reg_num"],
      "password": data["password"]
    })

# post job to db
def add_job_to_db(data):
    try:
        with engine.connect() as conn:
            query = text("INSERT INTO JobPosts (title, location, facility, time, duration, description, responsibilities, requirements, salary, currency) VALUES (:title, :location, :facility, :time, :duration, :description, :responsibilities, :requirements, :salary, :currency)")
            conn.execute(query, {
                "title": data["title"],
                "location": data["location"],
                "facility": data["facility"],
                "time": data["time"],
                "duration": data["duration"],
                "description": data["description"],
                "responsibilities": data["responsibilities"],
                "requirements": data["requirements"],
                "salary": data["salary"],
                "currency": data["currency"]
            })
        return True  # Return True to indicate successful insertion
    except Exception as e:
        print(f"Error occurred while adding job to database: {e}")
        return False  # Return False to indicate insertion failure


# read jobs from the database
def load_jobs_from_db(id=None):
  if id:
      with engine.connect() as conn:
          result = conn.execute(text("SELECT * FROM JobPosts WHERE id = :val"), {"val": id})
          jobs = [r._asdict() for r in result.all()]
          return jobs
  else:
      # If no id is provided, fetch all jobs
      with engine.connect() as conn:
          result = conn.execute(text("SELECT * FROM JobPosts"))
          jobs = [r._asdict() for r in result.all()]
          return jobs


# remove job from the database
def remove_job_from_db(job_id):
  with engine.connect() as conn:
    query = text("DELETE FROM JobPosts where id = :id")
    conn.execute(query, {"id": job_id})
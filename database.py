import os
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# retrieve environment variable
db_connection_string = os.environ["DB_CONNECTION_STRING"]


engine = create_engine(
  db_connection_string, connect_args= {
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem",
        }} 
  ) 

# use sqlalchemy orm to create a connection to the database
class Base(DeclarativeBase):
  pass

# create db models
class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  name = Column(String(100), unique=True)
  age = Column(Integer)
  sex = Column(String(10))
  email = Column(String(100), unique=True)
  phone = Column(String(20), unique=True)
  experience = Column(Integer)
  title = Column(String(100))
  linkedIn = Column(String(1000))
  resume = Column(String(1000))
  photo = Column(String(1000))
  reg_num = Column(String(50))
  location = Column(String(100))
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  password = Column(String(500))
  # ... other user columns ...
  posts = relationship("Post", primaryjoin='User.id == Post.user_id')

class Post(Base):
  __tablename__ = "job_posts"

  id = Column(Integer, primary_key=True)
  title = Column(String(30))
  location = Column(String(30))
  facility = Column(String(30))
  time = Column(String(30))
  duration = Column(Integer)
  description = Column(String(1000))
  responsibilities = Column(String(1000))
  requirements = Column(String(1000))
  salary = Column(Integer)
  currency = Column(String(30))
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  user_id = Column(Integer)
  user = relationship("User", primaryjoin='User.id == Post.user_id')

class Application(Base):
  __tablename__ = "job_applications"
  id = Column(Integer, primary_key=True)  
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer)
  user = relationship("User", primaryjoin='User.id == Application.user_id')
  post_id = Column(Integer)
  post = relationship("Post", primaryjoin='Post.id == Application.post_id')


class Review(Base):
  __tablename__ = "job_reviews"
  id = Column(Integer, primary_key=True)
  rating = Column(Integer)
  comment = Column(String(1000))
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer)  
  user = relationship("User", primaryjoin='User.id == Review.user_id')
  post_id = Column(Integer)
  post = relationship("Post", primaryjoin='Post.id == Review.post_id')


# insert client to db
def add_client(data):
  data["created_at"] = datetime.utcnow()
  data["updated_at"] = datetime.utcnow()
  with engine.connect() as conn:
      query = text("insert into users(name, age, sex, phone, email, title, location, experience, linkedin, resume, photo, reg_num, password, created_at, updated_at) values(:name, :age, :sex, :phone, :email, :title, :location, :experience, :linkedin, :resume, :photo, :reg_num, :password, :created_at, :updated_at)")
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
        "password": data["password"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"]
      })
def add_job_to_db(data):
  data = data.to_dict(flat=True)
  data["created_at"] = datetime.utcnow()
  data["updated_at"] = datetime.utcnow()
  try:
      with engine.connect() as conn:
          query = text("INSERT INTO job_posts (title, location, facility, time, duration, description, responsibilities, requirements, salary, currency, created_at, updated_at) VALUES (:title, :location, :facility, :time, :duration, :description, :responsibilities, :requirements, :salary, :currency, :created_at, :updated_at)")
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
              "currency": data["currency"],
              "created_at": data["created_at"],
              "updated_at": data["updated_at"]
          })
      return True  # Return True to indicate successful insertion
  except Exception as e:
      print(f"Error occurred while adding job to database: {e}")
      return False  # Return False to indicate insertion failure
# read clients from database
def load_clients_from_db():
  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM users"))
      clients = [r._asdict() for r in result.all()]
      return clients

# read jobs from the database
def load_jobs_from_db(id=None):
  if id:
      with engine.connect() as conn:
          result = conn.execute(text("SELECT * FROM job_posts WHERE id = :val"), {"val": id})
          jobs = [r._asdict() for r in result.all()]
          return jobs
  else:
      # If no id is provided, fetch all jobs
      with engine.connect() as conn:
          result = conn.execute(text("SELECT * FROM job_posts"))
          jobs = [r._asdict() for r in result.all()]
          return jobs


# remove job from the database
def remove_job_from_db(job_id):
  with engine.connect() as conn:
    query = text("DELETE FROM job_posts where id = :id")
    conn.execute(query, {"id": job_id})

# update job in the database
def update_job_in_db(job_id, new_data):
  data["updated_at"] = datetime.utcnow()
  try:
      with engine.connect() as conn:
          query = text("""
              UPDATE job_posts
              SET title = :title,
                  location = :location,
                  facility = :facility,
                  time = :time,
                  duration = :duration,
                  description = :description,
                  responsibilities = :responsibilities,
                  requirements = :requirements,
                  salary = :salary,
                  currency = :currency,
                  updated_at = :updated_at
              WHERE id = :id
          """)
          conn.execute(query, {**new_data, "id": job_id})
  except Exception as e:
      print(f"Error occurred while updating job: {e}")
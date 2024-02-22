from fastapi import FastAPI,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models
from .database import engine,get_db
from .routers import post,user



models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='deekshith',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected successfully")
        break
    except Exception as ex:
        print("database connection failed")
        print("error", ex)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"data": "This is for posts"}

@app.get("/test")
def Test(db:Session=Depends(get_db)):
    return {"status":"success"}
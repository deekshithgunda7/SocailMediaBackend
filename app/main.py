from turtle import title
from typing import Optional,List
from fastapi import FastAPI, Response, status, HTTPException,Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models,schemas
from .database import engine,get_db


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


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    print(posts)
    return posts


@app.get("/")
def root():
    return {"data": "This is for posts"}

@app.get("/test")
def Test(db:Session=Depends(get_db)):
    return {"status":"success"}

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db)):

    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no post found")
      
    return  post


@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db)):
    
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
   
    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate,db:Session=Depends(get_db)):

    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()

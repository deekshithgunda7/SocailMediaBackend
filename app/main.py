from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"data": "This is for posts"}

# @app.get("/test")
# def Test(db:Session=Depends(get_db)):
#     return {"status":"success"}
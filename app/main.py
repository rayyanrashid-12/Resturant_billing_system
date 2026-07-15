from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Restaurant Billing System API"}

@app.get ("/health")
def root():
    
    return {
    "STATUS":"RUNNING"}


    
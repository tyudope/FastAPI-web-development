from fastapi import FastAPI, Depends


app = FastAPI()

def user_dep(name : str, password:str):
    return {"name": name , "valid" : True}

@app.get("/user")
def get_user(user:dict = Depends(user_dep)) -> dict:
    return user



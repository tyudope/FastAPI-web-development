from fastapi import FastAPI
from fastapi import Body
from fastapi import Header


app = FastAPI()

@app.get("/hi")
def greet():
    return f"Hello? world?"


# url path
@app.get("/hi/{who}")
def greet(who):
    return f"Hello? {who}"

# Query Parameters



@app.post("/hi")
def greet(who:str = Body(embed = True)):
    return f"Hello {who}"

##

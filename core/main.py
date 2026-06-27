from fastapi import FastAPI

app = FastAPI()

Name_List = [
    {"id":1, "name":"Mehdi"},
    {"id":2, "name":"Maria"},
    {"id":3, "name":"Mazi"},
    {"id":4, "name":"Ela"},
    {"id":5, "name":"Eli"},
    {"id":6, "name":"Fate"},
    {"id":7, "name":"Raihan"},
    {"id":8, "name":"Monica"},
    {"id":9, "name":"Zin"}
]


@app.get("/")
def root():
    return {"message":"Hello World:)"}

@app.get("/names")
def Retvieve_Name_List():
    return Name_List
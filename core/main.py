from fastapi import FastAPI, Query, status, HTTPException
from typing import Annotated

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
    {"id":9, "name":"Zin"},
    {"id":10, "name":"Mehdi"},
    {"id":11, "name":"Maria"}
]

@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_a_new_name (name:str):
    new_id = Name_List[-1]["id"] + 1
    name_obj = {"id":  new_id, "name": name}
    Name_List.append(name_obj)
    return name_obj

@app.get("/names/{name_id}")
def retrieve_name_detail (name_id:int):
    for name in Name_List:
        if name["id"] == name_id:
            return name
    return {"detail":"name_id is not in our server"}

@app.put("/names/{name_id}",status_code=status.HTTP_200_OK)
def retrieve_name_detail (name_id:int, name:str):
    for item in Name_List:
        if item["id"] ==name_id:
            item["name"] = name
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")

@app.delete("/names/{name_id}", status_code=status.HTTP_200_OK)
def retrieve_name_detail (name_id:int):
    for item in Name_List:
        if item["id"] ==name_id:
            Name_List.remove(item)
            return {"detail":"object removed successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")

@app.get("/")
def root():
    return {"message":"Hello World:)"}

@app.get("/names")
def Retvieve_Name_List(q:Annotated[str|None,Query(max_length=50)]=None):
    if q:
        return [item for item in Name_List if item["name"] == q]
    return Name_List
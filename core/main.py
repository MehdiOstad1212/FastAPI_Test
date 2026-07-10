from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated, List
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Start Up")
    yield
    print("Application Shut Down")

app = FastAPI(lifespan = lifespan)

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

@app.get("/")
def root():
    Content = {"message":"Hello World:)"}
    return JSONResponse(content = Content, status_code= status.HTTP_202_ACCEPTED)

@app.get("/names")
def Retvieve_Name_List(q:Annotated[str|None,
                                   Query(title="search", alias="search", 
                                         description="Searching the provided title", 
                                         example="Mehdi" , deprecated= True, 
                                         max_length=50)]=None):
    if q:
        Content = [item for item in Name_List if item["name"] == q]
        if Content == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")
        return JSONResponse(content = Content, status_code= status.HTTP_200_OK)
    Content = Name_List
    return JSONResponse(content = Content, status_code= status.HTTP_200_OK)


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_a_new_name (name:str = Body (...,
                                        title="Adding a name",
                                        description="Write the name that you want to" \
                                        "add to the list", example="Mehdi",
                                        embed=True)):
    new_id = Name_List[-1]["id"] + 1
    name_obj = {"id":  new_id, "name": name}
    Name_List.append(name_obj)
    Content = name_obj
    return JSONResponse(content = Content, status_code= status.HTTP_201_CREATED)

@app.get("/names/{name_id}")
def retrieve_name_detail (name_id:int = Path(title= "Object id",
                                             description="The id related to " \
                                             "a name in the Name List")):
    for name in Name_List:
        if name["id"] == name_id:
            Content = name
            return JSONResponse(content = Content, status_code= status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "name_id is not in our server")

@app.put("/names/{name_id}",status_code=status.HTTP_200_OK)
def retrieve_name_detail (name_id:int = Path(), name:str = Form()):
    for item in Name_List:
        if item["id"] ==name_id:
            item["name"] = name
            Content = item
            return JSONResponse(content = Content, status_code= status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")

@app.delete("/names/{name_id}")
def retrieve_name_detail (name_id:int):
    for item in Name_List:
        if item["id"] ==name_id:
            Name_List.remove(item)
            Content = {"detail":"object removed successfully"}
            return JSONResponse(content = Content, status_code = status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}

'''
@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    return [
        {"filename": file.filename, "content_type": file.content_type}
        for file in files
    ]

@app.post("/upload-multiple/")
async def upload_multiple(
    files: Annotated[List[UploadFile], File(description="Multiple files to upload")]
):
    return [
        {"filename": file.filename, "content_type": file.content_type} 
        for file in files
    ]
'''

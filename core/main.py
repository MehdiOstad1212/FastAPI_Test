from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile
from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Annotated, List
from contextlib import asynccontextmanager
from dataclasses import dataclass
from database_main import Base, engine, get_db, Person
from sqlalchemy.orm import Session
from Schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Start Up")
    Base.metadata.create_all(engine)
    yield
    print("Application Shut Down")

app = FastAPI(lifespan = lifespan)

@app.get("/")
def root():
    Content = {"message":"Hello World:)"}
    return JSONResponse(content = Content, status_code= status.HTTP_202_ACCEPTED)

@app.get("/names")
def Retvieve_Name_List(q:Annotated[str|None,
                                   Query(title="search", alias="search", 
                                         description="Searching the provided title", 
                                         example="Mehdi" , deprecated= True, 
                                         max_length=50)]=None,db:Session = Depends(get_db)):
    query = db.query(Person)
    
    if q:
        query = query.filter_by(username = q).all()
        if query == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")
        return query
    query = query.all()
    return query


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_a_new_name (request: PersonCreateSchema,db:Session = Depends(get_db)):
    new_person = Person(username = request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@app.get("/names/{name_id}")
def retrieve_name_detail (name_id:int = Path(title= "Object id",
                                             description="The id related to " \
                                             "a name in the Name List"), 
                                             db:Session = Depends(get_db)):
    person = db.query(Person).filter_by(id = name_id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "name_id is not in our server")

@app.put("/names/{name_id}",status_code = status.HTTP_200_OK)
def retrieve_name_detail (request: PersonUpdateSchema, name_id:int = Path(),
                          db:Session = Depends(get_db)):
    person = db.query(Person).filter_by(id = name_id).one_or_none()
    if person:
        person.username = request.name
        db.commit()
        db.refresh(person)
        return person
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "object not found")

@app.delete("/names/{name_id}")
def retrieve_name_detail (name_id:int, db:Session = Depends(get_db)):
    person = db.query(Person).filter_by(id = name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
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



from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import asyncio
from datetime import datetime
from typing import Optional


# STEP 1. Create the Note Class
class Note(BaseModel):

    id:int
    title: str = Field(..., min_length = 2, max_length=10)
    content: str= Field(..., min_length = 2, max_length=148)
    tags : list[str] = Field(min_length = 1, max_length=5)
    created_at : datetime
    updated_at : datetime = Field(default_factory=datetime.now)





note_1 = Note(id = 1, title="ML note", content = "To perform ridge/lasso regression you have to normalize the data first.", tags = ["ML","REG"], created_at=datetime.now())
note_2 = Note(id = 2 , title="Math" , content = "Study calculus for 2 hours ", tags = ["Math","Uni"], created_at=datetime.now())
note_3 = Note(id = 3, title= "AI" , content = "Study AI Engineering from Chip Huyen for 2 hours" , tags = ["ML","AI","BOOK"] , created_at=datetime.now())

notes = [
    note_1,
    note_2,
    note_3
]


# STEP 2.
# Create the FastAPI application
app = FastAPI()



# STEP 3.
# Create
# CRUD (CREATE (POST) , Read (GET), UPDATE (PUT) , DELETE (DELETE))

# Read notes by given user_id and given tags.
# You CANNOT have two endpoints with the same path.
@app.get("/notes/{user_id}")
def read_jokes_tag(user_id :int, tag: Optional[str] = None):

    read_notes = []
    for note in notes:
        if note.id == user_id:

            # If tag is provided, filter by tag
            if tag:
                if tag in note.tags:
                    read_notes.append(note)
            else:
                # No tag given -> include all notes for that user.
                read_notes.append(note)

    if not read_notes:
        raise HTTPException(status_code=404, detail = "No notes found.")


    return read_notes



from fastapi import FastAPI
from C3_FastAPITour.model.tag import TagIn, Tag, TagOut
from datetime import datetime
import C3_FastAPITour.service.tag as service
app = FastAPI()

@app.post("/")
def create(tag_in: TagIn) -> TagIn:

    tag : Tag = Tag(tag = tag_in.tag, created = datetime.utcnow(), secret = 'ssshhhh')
    service.create(tag)

    return tag_in


@app.get("/{tag_str}", response_model = TagOut)
def get_one(tag_str : str) -> TagOut:

    tag : Tag = service.get(tag_str)
    return tag
    # Even though we returned a Tag, response_model will convert it to a TagOut


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("tag:app" , reload = True)
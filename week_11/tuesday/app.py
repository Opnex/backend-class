from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

app = FastAPI(title="Simple Fast App", version="1.0.0")

data=[{"name": "Sam Larry", "age": 20, "track": "AI Developer"},
    {"name": "Steve More", "age": 30, "track": "AI Engineer"},
    {"name": "Dan Mike", "age": 25, "track": "AI Developer"}]


class Item(BaseModel):
    name: str = Field(..., example="Perpetual")
    age: int = Field(..., example=25)
    name: str = Field(..., example="Fullstack Developer")

@app.get("/", description="This endpoint just return a message")
def root():
    return {"Message": "Welccome to Opnex FastAPI Application"}

@app.get("/get_data")
def get_data():
    return data


@app.post("/create_data")
def create_data(req:Item):
    data.append(req.dict())
    return{"Message": "Data Receive", "Data": data}


@app.put("/update_data{id}/")
def create_data(id, int, req: Item):
    data[id] = req.dict()
    print(data)
    return{"Message": "Data Updated", "Data": data}

if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))


# Write an endpoint to patch and delete entries from the data var
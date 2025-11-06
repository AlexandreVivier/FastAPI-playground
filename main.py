from fastapi import FastAPI, HTTPException

app = FastAPI()


items = []

@app.get("/")
def root():
    return {"Foo": "Bar"}

@app.post("/items/")
def create_item(item: str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    try:
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")
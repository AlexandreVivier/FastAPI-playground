from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    text: str
    is_done: bool = False


items = []

@app.get("/")
def root():
    return {"Foo": "Bar"}

@app.post("/items/")
def create_item(item: Item):
    items.append(item)
    return items
# Avant l'arrivée de BaseModel et la création de la classe Item:
#  Invoke-WebRequest -Uri "http://127.0.0.1:8000/items/?item=apple" -Method POST -Headers @{"Content-Type"="application/json"}
#  maintenant, avec BaseModel et JSON:
#  Invoke-WebRequest -Uri "http://127.0.0.1:8000/items/" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"text": "apple", "is_done": false}'

@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

#  Invoke-WebRequest -Uri "http://127.0.0.1:8000/items" -Method GET -Headers @{"Content-Type"="application/json"}
#  Ou bien avec limite:
#  Invoke-WebRequest -Uri "http://127.0.0.1:8000/items?limit=3" -Method GET -Headers @{"Content-Type"="application/json"}

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    
    # Invoke-WebRequest -Uri "http://127.0.0.1:8000/items/3" -Method GET -Headers @{"Content-Type"="application/json"}

# DOCS:
    # Pour lancer le serveur:
    # uvicorn main:app --reload
    # Puis aller à l'adresse:
    # http://127.0.0.1:8000
    # Pour avoir le modèle de réponse dans la documentation interactive:
    # http://127.0.0.1:8000/docs
    # Ou en mode texte:
    # http://127.0.0.1:8000/redoc
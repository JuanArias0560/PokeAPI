from typing import Optional
from fastapi import FastAPI
import httpx

app=FastAPI()


@app.get("/")
async def read_root():
    name_ability=[]
    url_ability=[]
    data_url=[]
    descrip_data=[]
    
    poke_name="ditto"
    url=f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
    
    
    async with httpx.AsyncClient() as client:
        resp= await client.get(url)
        resp = resp.json()
        resp=resp["abilities"]              
        length=len(resp)

    for ability in range(0,length):
        name_ability.append(resp[ability]["ability"]["name"])
        url_ability.append(resp[ability]["ability"]["url"])
    
    async with httpx.AsyncClient() as name:
        for urls in url_ability:
            descrip= await name.get(urls)
            descrip=descrip.json()
            descrip=descrip["flavor_text_entries"]
            descrip_data.append(descrip)

    length_descrip_data=len(descrip_data)
    
            
    
    for description in range(0,length_descrip_data):
        length_internal=len(descrip_data[description])
        for count in range(0,length_internal):
            if descrip_data[description][count]["language"]["name"]=="en" and descrip_data[description][count]["version_group"]["name"]=="sword-shield":
                data_url.append(descrip_data[description][count]["flavor_text"]) 
                       
        
    
    return data_url


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return{"item_id": item_id ,"q" : q}
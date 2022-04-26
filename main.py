from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app=FastAPI()


@app.get("/home/" , response_class=HTMLResponse)
async def home(request:Request):    

    return templates.TemplateResponse("index.html",{
    "request":request,
    "message":"Lista de pokemones",
    "output1":"Escoje tu pokemon:"
})

@app.post("/home/",response_class=HTMLResponse)
async def index(request:Request):
    pokemon=await request.form()
    for name in pokemon:
        names=name
    return templates.TemplateResponse("index.html",{
    "request":request,
    "names":names,
    "message":f"Habilidades de {names}",
    "output" : await ability(names)})

@app.get("/ability")
async def ability(pokemon):
    name_ability=[]
    url_ability=[]
    data_url=[]
    descrip_data=[]    

    url=f"https://pokeapi.co/api/v2/pokemon/{pokemon}"    
    
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
    
    returned={name_ability[0]:data_url[0],name_ability[1]:data_url[1]}
    return returned

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
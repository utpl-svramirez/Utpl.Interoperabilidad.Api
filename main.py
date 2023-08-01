from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

from fastapi_versioning import VersionedFastAPI, version

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth import authenticate

#seccion mongo importar libreria
import pymongo

import spotipy

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='c8519595485648c3949369793de3e366',
    client_secret='d266e54ea24346a7b278445be87cd400'
))
description = """
Utpl tnteroperabilidad API ayuda a describir las capacidades de un directorio. 🚀

## Estudiantes
Tu puedes crear un estudiante
Tu puedes listar estudiantes.

## Artistas
You will be able to:

* **Crear artista** (_not implemented_).
"""

tags_metadata = [
    {
        "name":"estudiantes",
        "description": "Permite realizar un crud completo de una persona (listar)"
    },
    {
        "name":"artistas",
        "description": "Permite realizar un crud completo de un artista"
    },
]

app = FastAPI(
    title="Utpl Interoperabilidad APP 2",
    description= description,
    version="0.0.1",
    terms_of_service="http://utpl.edu.ec/",
    contact={
        "name": "Silvia Ramírez",
        "url": "https://utpl-interoperabilidad-svramirez.onrender.com",
        "email": "svramirez@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata
)

#para agregar seguridad a nuestro api
security = HTTPBasic()

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://svramirez:<Sydney.786>@cluster0.is5ixhq.mongodb.net/?retryWrites=true&w=majority")
database = cliente["informacion"]
coleccion = database["estudiante"]

class EstudianteRepositorio (BaseModel):
    id: str
    nombre: str
    edad: int
    identificacion: Optional[str] = None
    ciudad: Optional[str] = None

class EstudianteEntrada (BaseModel):
    nombre:str
    edad:int
    ciudad: Optional[str] = None

class EstudianteEntradaV2 (BaseModel):
    nombre:str
    edad:int
    identificacion:str
    ciudad: Optional[str] = None


EstudiantesList = []

@app.post("/estudiantes", response_model=EstudianteRepositorio, tags = ["estudiantes"])
@version(1, 0)
async def crear_Estudiante(estudianteE: EstudianteEntrada):
    itemEstudiante = EstudianteRepositorio (id= str(uuid.uuid4()), nombre = estudianteE.nombre, edad = estudianteE.edad, ciudad = estudianteE.ciudad)
    resultadoDB =  coleccion.insert_one(itemEstudiante.dict())
    return itemEstudiante

@app.post("/estudiantes", response_model=EstudianteRepositorio, tags = ["estudiantes"])
@version(2, 0)
async def crear_estudiantev2(estudianteE: EstudianteEntradaV2):
    itemEstudiante = EstudianteRepositorio (id= str(uuid.uuid4()), nombre = estudianteE.nombre, edad = estudianteE.edad, ciudad = estudianteE.ciudad, identificacion = estudianteE.identificacion)
    resultadoDB =  coleccion.insert_one(itemEstudiante.dict())
    return itemEstudiante

@app.get("/Estudiantes", response_model=List[EstudianteRepositorio], tags=["estudiantes"])
@version(1, 0)
def get_estudiantes():
    print ("llego a consultar todas los estudiantes")
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/estudiantes/{estudiante_id}", response_model=EstudianteRepositorio , tags=["estudiantes"])
@version(1, 0)
def obtener_Estudiante (estudiante_id: str):
    item = coleccion.find_one({"id": estudiante_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

@app.delete("/estudiantes/{estudiante_id}", tags=["estudiantes"])
@version(1, 0)
def eliminar_Estudiante (estudiante_id: str):
    result = coleccion.delete_one({"id": estudiante_id})
    if result.deleted_count == 1:
        return {"mensaje": "Estudiante eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Estudiante no encontrada")

@app.get("/pista/{pista_id}", tags = ["artistas"])
@version(1, 0)
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track
    
@app.get("/artistas/{artista_id}", tags = ["artistas"])
@version(1, 0)
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista

@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad - SVRAMIREZ"}

app = VersionedFastAPI(app)
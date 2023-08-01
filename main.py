from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import spotipy

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='b0092ad56acf4c1baec55ddda550e9a3',
    client_secret='9b42ffeca6d641a9b3ab1631da824fc6'
))

app = FastAPI()


description = """
Utpl tnteroperabilidad API ayuda a describir las capacidades de un directorio. 🚀

## Items

You can **read items **.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""
tags_metadata = [
    {
        "name": "estudiantes",
        "description": "Permite realizar un crud completo de un estudiante (listar)"
    }
]

app = FastAPI(
    title="Utpl Interoperabilidad APP",
    description= description,
    version="0.0.1",
    terms_of_service="http:utpl.edu.ec",
    contact={
        "name": "Silvia Ramírez",
        "url": "https://utpl-interoperabilidad-svramirez.onrender.com",
        "email": "svramirez@utpl.edu.ec",
    },
    license_info= {
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


class Estudiante (BaseModel):
    dni: int
    nombre: str
    edad: int
    carrera: str
    ciudad: Optional[str] = None

EstudianteList = []

@app.post("/Estudiantes", response_model=Estudiante)
def crear_Estudiante(estudiante: Estudiante):
    EstudianteList.append(estudiante)
    return estudiante

@app.get("/Estudiantes ", response_model=List[Estudiante])
def get_Estudiante():
    return EstudianteListList

@app.get("/Estudiantes/{Estudiante_id}", response_model= Estudiante)
def obtener_Estudiante (Estudiante_id: int):
    for Estudiante in EstudianteList:
        if Estudiante.dni == Estudiante_dni:
            return Estudiante
    raise HTTPException(status_code=404, detail=" Estudiante no encontrado")

@app.delete("/Estudiantes/{Estudiante_id}")
def eliminar_estudiante(Estudiante_id: int):
    estudiante = next ((p for p in EstudianteList if p.Estudiante_id == estudiante_id), None)
    if estudiante:
        EstudianteList.remove(estudiante)
        return {"mensaje": "Estudiante eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail=" Estudiante eliminado")

@app.get("/pista/{pista_id}")

async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track
    
@app.get("/")
def read_root():
    return {"Interoperabilidad": "deber_final_svramirez"}


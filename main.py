from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Estudiante (BaseModel):
    dni: int
    nombre: str
    edad: int
    carrera: str
    ciudad: Optional[str] = None

EstudianteList = []

@app.post("/Estudiantes", response_model=Estudiante)
def crear_Estudiante(person: Estudiante):
    EstudianteList.append(person)
    return Estudiante

@app.get("/Estudiantes ", response_model=List[Estudiante])
def get_personas():
    return personaList

@app.get("/Estudiantes/{persona_id}", response_model= Estudiante)
def obtener_Estudiante (Estudiante_id: int):
    for Estudiante in EstudianteList:
        if Estudiante.dni == Estudiante_dni:
            return Estudiante
    raise HTTPException(status_code=404, detail=" Estudiante no encontrado")

@app.delete("/Estudiantes/{persona_id}")
def eliminar_estudiante(persona_id: int):
    estudiante = next ((p for p in EstudianteList if p.Estudiante_id == persona_id, None))
    if estudiante:
        EstudianteList.remove(estudiante)
        return {"mensaje": "Estudiante eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail=" Estudiante eliminado")

@app.get("/")
def read_root():
    return {"Interoperabilidad": "caso01_svramirez"}


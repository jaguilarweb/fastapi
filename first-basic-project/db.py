from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine

'''
# Si deseas usar una base de datos diferente a SQLite, puedes descomentar el siguiente bloque de código y configurar la URL de conexión en un archivo .env.

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Obtener la URL de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definido en el archivo .env")

# Crear el motor de la base de datos usando directamente la cadena de conexión
engine = create_engine(DATABASE_URL)
'''

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

# Creamos la función que crea las tablas.
def create_all_tables(app: FastAPI):    
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
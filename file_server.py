import os
from date_time_dir import DateTimeDir
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

SERVED_FOLDER = os.environ.get("SERVED_FOLDER", "/tmp/date_time_dir")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                                   allow_methods=["*"], allow_headers=["*"])
app.mount("/get_file", StaticFiles(directory=SERVED_FOLDER), name="get_file")

# Récupération sans filtre :        curl 127.0.0.1:8080 | jq
# Récupération d'un jour donné :    curl 127.0.0.1:8080?filter=20201231 | jq
# Récupération d'une heure donnée : curl 127.0.0.1:8080?filter=2020123118 | jq
@app.get("/")
async def root(filter: str = ""):
    dir = DateTimeDir(SERVED_FOLDER)
    return {"served_folder": SERVED_FOLDER} | dir.get_list(filter)

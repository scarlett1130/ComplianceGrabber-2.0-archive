from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Scrapper import Scrapper



scrapper = Scrapper()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Part Number Scrapper": "Welcome!"}


@app.get("/maxim/{part_number}")
def read_item(part_number):
    return scrapper.scrap_Maxim(part_number)

@app.get("/omron/{part_number}")
def read_item(part_number):
    return scrapper.scrap_omron(part_number)

@app.get("/arrow/{part_number}")
def read_item(part_number):
    return scrapper.scrap_Arrow(part_number)


@app.get("/molex/{part_number}")
def read_item(part_number):

    return scrapper.scrap_Molex(part_number)


@app.get("/phoenix/{part_number}")
def read_item(part_number):
    return scrapper.scrap_Phoenix(part_number)


@app.get("/rscomponents/{part_number}")
def read_item(part_number):
    return scrapper.scrap_Rscomponents(part_number)

@app.get("/onsemi/{part_number}")
def read_item(part_number):
    return scrapper.scrap_onsemi(part_number)


@app.get("/mouser/{part_number}")
def read_item(part_number):
    return scrapper.scrap_mouser(part_number)




@app.get("/te/{part_number}")
def read_item(part_number):
    return scrapper.scrap_Te(part_number)


@app.get("/wago/{part_number}")
def read_item(part_number):
    return scrapper.scrap_Wago(part_number)

@app.get("/findsupplier/{part_number}")
def read_item(part_number):
    return scrapper.find_Supplier(part_number)



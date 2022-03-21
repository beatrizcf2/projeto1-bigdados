from email.mime import message
from typing import Optional, Dict, List, Set
from urllib import response
from fastapi import FastAPI, Path, Query, status, HTTPException
from pydantic import BaseModel, Field, HttpUrl # for request body interactions
#from fastapi.encoders import jsonable_encoder
#import json
from funcoes import *


# TAREFAS ###########################################

# - Add mais exemplos: https://fastapi.tiangolo.com/tutorial/schema-extra-example/
# descobrir pra q q serve cookie
# add response status code: https://fastapi.tiangolo.com/tutorial/response-status-code/
# add handler errors - se der tempo, adicinei no de criar carrinho so
#####################################################


'''
Models ................................................
Usado para declarar o request body
'''
class Image(BaseModel):
    url: HttpUrl
    name: str

class Product(BaseModel):
    product_id: int = Field(example=1)                           
    name: str = Field(None, title="The name of the product", max_length=100, example="iogurte")                              
    description: Optional[str] = Field(None, title="The description of the product", max_length=300, example="iogurte desnatado 200g")   
    brand: Optional[str] = Field(None, title="The brand of the item", max_length=80, example="nestle")   
    price: float = Field(..., gt=0, description="The price must be greater than zero", example=2.7)
    discount: Optional[float] = Field(..., ge=0, lt=1, description="The discount must be greater than 0 and less than 1", example=0.05)     
    quantity: float = Field(..., gt=0, description="The quantity must be greater than zero", example=1)
    image: Optional[Image] = Field(example={
                "url": "https://static.paodeacucar.com/img/uploads/1/912/668912.jpg",
                "name": "iogurte desnatado nestle"
                })

    
class Cart(BaseModel):
    cart_id: int
    user_id: int                                                    
    #products: Dict[Product,int] = dict() #chave:produto, valor:qtde
    products: Set[str] = set() # lista de produtos unicos



'''
Path operations .....................................................
'''

app = FastAPI()

# root - OK
@app.get("/")
async def root():
    return {"Message": "Welcome to The Shop Cart"}

# criar carrinho de compras - OK
@app.post("/cart/", response_model=Cart, status_code=status.HTTP_201_CREATED) 
async def create_cart(cart: Cart):
    append_json(cart, "carts.json", "carts")
    return cart

# deletar carrinho de compras - OK
@app.delete("/cart/{cart_id}", response_model=Cart)
async def delete_cart(*, cart_id: int = Path(..., title="The ID of the cart to get", ge=0)):
    remove_from_json(cart_id,"carts.json", "carts")
    return 

# ADICIONAL - ler carrinho de compras
@app.get("/cart/{cart_id}")
async def read_cart(*, cart_id: int):
    carts = read_json("carts.json", "carts")

    for cart in carts:
        if cart["cart_id"] == cart_id:
            return cart
    
    return {"message": "Not Found"}
    

# # ADICIONAL - ler carrinhos de compras existentes
# @app.get("/carts/", response_model=Cart)
# async def read_carts(cart: Cart):
#    return cart

# adicionar item ao carrinho de compras
# envia dados pelo request body
@app.patch("/cart/{cart_id}/product", response_model=Product)
async def add_to_cart(cart_id:int, product: Product):
    cart = carts[cart_id]
    (cart.products).append(product)
    carts[cart_id] = cart
    return product

# remover item carrinho de compras 
# como defino a quantidade de itens que vou remover?
@app.delete("/cart/{cart_id}/product/{product_id}", response_model=Product)
async def remove_from_cart(cart_id:int, product_id: int, product: Product):
    remove_from_json(product_id,"carts.json", "carts")
    return product

# criar produto
# envia dados pelo request body - OK
@app.post("/inventory/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    append_json(product, "inventory.json", "inventory")
    return product

# consultar inventario de produtos
@app.get("/inventory/")
async def read_all_inventory():
    all_products = read_json("inventory.json", "inventory")

    return all_products

# consultar produto em inventario de produtos
@app.get("/inventory/{product_id}")
async def read_inventory(*, product_id: int):
    all_products = read_json("inventory.json", "inventory")
    for p in all_products:
        if p["product_id"] == product_id:
            return p
    
    return {"message": "Not Found"}

# alterar produto do inventario
# envia o que quer alterar pelo request body
@app.patch("/inventory/{product_id}")
async def update_product(product_id: int, product: Product):
    update_json(product_id, product,"inventory.json","inventory")
    return 

# remover produto do inventario - OK
@app.delete("/inventory/{product_id}", response_model=List[Product])
async def delete_product(product_id: int):
    remove_from_json(product_id, "inventory.json", "inventory", id_type=1)
    return 



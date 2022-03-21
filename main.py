from typing import Optional, Dict, List, Set
from urllib import response
from fastapi import FastAPI, Path, Query, status, HTTPException
from pydantic import BaseModel, Field, HttpUrl # for request body interactions
from fastapi.encoders import jsonable_encoder

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
    products: Dict[Product,int] = dict() #chave:produto, valor:qtde
    #products: Set[Product] = set() # lista de produtos unicos

'''
Variaveis para aplicacao ..................................................
'''
inventory = {
    1 : {"product_id": 1,
        "name": "iogurte",
        "description": "iogurte desnatado 200g",
        "brand": "nestle",
        "price": 2.7,
        "discount": 0.05,
        "quantity": 359,
        "image": {
            "url": "https://static.paodeacucar.com/img/uploads/1/912/668912.jpg",
            "name": "iogurte desnatado nestle"
        }
        },
    2 : {"product_id": 2,
        "name": "macarrao",
        "description": "macarrao barilla grano duro 500g",
        "brand": "barilla",
        "price": 10.20,
        "discount": 0.0,
        "quantity": 123,
        }
}

carts = {}

'''
Path operations .....................................................
'''

app = FastAPI()

# root
@app.get("/")
async def root():
    return {"Message": "Welcome to The Shop Cart"}

# criar carrinho de compras
@app.post("/cart/", response_model=Cart, status_code=status.HTTP_201_CREATED) 
async def create_cart(cart: Cart):
    carts[cart.cart_id] = cart
    print(carts)
    return cart

# deletar carrinho de compras 
@app.delete("/cart/{cart_id}", response_model=Cart)
async def delete_cart(*, cart_id: int = Path(..., title="The ID of the cart to get", ge=1)):
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    del carts[cart_id]
    print(carts)
    return carts

# ADICIONAL - ler carrinho de compras
@app.get("/cart/{cart_id}", response_model=Cart)
async def read_cart(cart_id: int):
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart = carts
    return {f"cart {cart_id}": cart.products}
    

# ADICIONAL - ler carrinhos de compras existentes
@app.get("/carts/", response_model=Cart)
async def read_cart(cart: Cart):
   return cart

# adicionar item ao carrinho de compras
# envia dados pelo request body
@app.patch("/cart/product", response_model=Product)
async def add_to_cart(product: Product):
    return product

# remover item carrinho de compras 
# como defino a quantidade de itens que vou remover?
@app.delete("/cart/product/{product_id}", response_model=Product)
async def remove_from_cart(product_id: int, product: Product):
    return product

# criar produto
# envia dados pelo request body
@app.post("/inventory/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    return product

# consultar inventario de produtos
@app.get("/inventory/")
async def read_inventory():
    return 

# alterar produto do inventario
# envia o que quer alterar pelo request body
@app.patch("/inventory/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    return product

# remover produto do inventario 
@app.delete("/inventory/{product_id}", response_model=List[Product])
async def delete_product(product_id: int, product: Product):
    return inventory



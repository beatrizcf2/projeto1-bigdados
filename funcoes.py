import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

def raise_exception(status_code):
    raise HTTPException(status_code=status_code, detail="Item not found")

def find_id(id, file, tag, id_type):
    '''
        Funcao que retorna objeto do tipo definido por id_type e o index em que ele se
        id_type = 0 - cart
        id_type = 1 - inventory 
    '''
    with open(file, 'r', encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
        dado = find_data(id,dados[tag],id_type)
        return dado
        

def find_data(id, data, id_type):
    for item in data:
        if item[id_type+'_id']==id:
            return item
    return False

def format_to_json(file, data):
    '''
     convert dict in json format
    '''
    file.truncate(0)
    file.seek(0)
    json.dump(data,file, indent=4)
    return

def read_json(file, key):
    '''
        le um arquivo em json e retorna seu conteudo
    '''
    file = "data/"+file
    with open(file, "r+", encoding='utf-8') as file_data:
        file_data = json.loads(file_data.read())
        return file_data[key]



def append_json(new_data, file, tag, id_type):
    '''
        add dados ao arquivo json
    '''
    new_data = jsonable_encoder(new_data) 
    file = "data/"+file
    with open(file, 'r+') as f:
        file_data = json.load(f)  
        index = max([id[id_type+"_id"] for id in file_data[tag]]) + 1
        final_data = {**new_data, **{id_type+"_id":index}}
        file_data[tag].append(final_data)
        format_to_json(f, file_data)
        return


def remove_from_json(id, file, tag, id_type, update_type, id_extra=0):
    '''
        atualiza dados ao arquivo json
        update_type: 0 - cart
                     1 - cart+product
    '''

    file = "data/"+file
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
        try: 
            if update_type == 1:
                cart = find_id(id, file, tag, id_type="cart")
                cart_index = file_data[tag].index(cart)
                product = find_data(id_extra, cart["products"], id_type="product")
                file_data[tag][cart_index]["products"].remove(product)
            elif update_type == 0:
                product = find_id(id, file, tag, id_type)
                file_data[tag].remove(product)
        except:
            raise_exception(404)
        format_to_json(f, file_data)
        return

def update_json(id, new_data,file,tag, update_type, id_extra = 0):
    '''
        atualiza dados ao arquivo json
        update_type: 0 - edit
                     1 - add
    '''
    new_data = jsonable_encoder(new_data) 
    file = "data/"+file
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
        try:
            if update_type == 1:
                #preciso achar o cart id
                cart = find_id(id, file, tag, id_type="cart")
                cart_index = file_data[tag].index(cart)
                lista = cart["products"]
                product = find_data(id_extra, cart["products"], id_type="product")
                if product:
                    product_index = cart["products"].index(product)
                    lista[product_index]["quantity"] += new_data["quantity"]
                else:
                    lista.append(new_data)
                file_data[tag][cart_index]["products"] = lista
                
            elif update_type == 0:
                product = find_id(id, file, tag, id_type="product")
                lista = file_data[tag]
                if product:
                    product_index = file_data[tag].index(product)
                    lista[product_index] = new_data
                else:
                    raise
                    lista.append(new_data)
                file_data[tag] = lista
        except:
            raise_exception(404)
        format_to_json(f, file_data)
        return


    







    
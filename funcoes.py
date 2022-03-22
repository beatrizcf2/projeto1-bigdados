import json
from fastapi.encoders import jsonable_encoder


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
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return


def remove_from_json(id, file, tag, id_type):
    file = "data/"+file
    print(file)
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
        item = find_id(id, file, tag, id_type)
        file_data[tag].remove(item)
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return
    
def remove_from_json_cart(id, file, tag, id_type=0):
    file = "data/"+file
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
        item = find_id(id, file, tag, id_type)
        print(item)
        print(file_data[tag].index(item))
        index = file_data[tag].index(item)
        print(index)
        
        file_data[tag][index]["products"].remove(item)
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return


def update_json(id,new_data,file,tag):
     index = 0
     '''
         atualiza dados ao arquivo json
     '''
     new_data = jsonable_encoder(new_data) 
     file = "data/"+file
     with open(file, 'r+') as f:
         file_data = json.load(f)
         item = file_data[tag]
         # para cada produto no inventario
         for dado in item: 
             # se o id o produto esta na lista
             if dado["product_id"] == id:
                 print(id)
                 index = item.index(dado)
                 # para cada chave e valor no produto do inventario 
                 for k,v in dado.items():
                     if dado[k] != new_data[k]:
                         dado[k] = new_data[k] # atualiza o valor do produto
                 dado_novo = dado
                 break
         item[index] = dado_novo
         file_data[tag] = item
         print(item)
         f.truncate(0)
         f.seek(0)
         json.dump(file_data,f, indent=4)
         return



def update_json_cart(id, new_data,file,tag, update_type, id_extra = 0):
    '''
        atualiza dados ao arquivo json
        update_type: 0 - edit
                     1 - add
    '''
    new_data = jsonable_encoder(new_data) 
    file = "data/"+file
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
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
                lista[product_index]["quantity"] += new_data["quantity"]
            else:
                lista.append(new_data)
            file_data[tag] = lista
        
        print(file_data)
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return


# criar funcao para dar raise error caso nao exista o id
'''
ESCOPO
if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    del carts[cart_id]
    print(carts)
    return carts
'''








    
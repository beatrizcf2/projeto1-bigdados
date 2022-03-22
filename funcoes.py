import json
from fastapi.encoders import jsonable_encoder

def find_id(id, file, tag, id_type=0):
    '''
        Funcao que retorna objeto do tipo definido por id_type 
        id_type = 0 - cart
        id_type = 1 - inventory 
    '''
    with open(file, 'r', encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
        for dado in dados[tag]:
            if id_type == 0:
                if dado['cart_id']==id:
                    print(f"\n{dado}\n")
                    return dado
            if id_type == 1:
                if dado['product_id']==id:
                    print(f"\n{dado}\n")
                    return dado
        return False



def find_product(id, dado):
    print(dado)
    for product in dado:
        if product['product_id']==id:
            print(f"achei o besta")
            return product
        return False

def read_json(file, key):
    '''
        le um arquivo em json e retorna seu conteudo
    '''
    file = "data/"+file
    with open(file, "r+", encoding='utf-8') as file_data:
        file_data = json.loads(file_data.read())
        return file_data[key]

def append_json(new_data, file, tag):
    '''
        add dados ao arquivo json
    '''
    new_data = jsonable_encoder(new_data) 
    file = "data/"+file
    with open(file, 'r+') as f:
        file_data = json.load(f)
        if tag == "carts":
            index = max([id[tag[:-1]+"_id"] for id in file_data[tag]]) + 1
            final_data = {**new_data, **{tag[:-1]+"_id":index}}
        else:
            index = max([id["product_id"] for id in file_data[tag]]) + 1
            final_data = {**new_data, **{"product_id":index}}
        file_data[tag].append(final_data)
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return



def remove_from_json(id, file, tag, id_type=0):
    # verifica se existe o id 
    # se existir, remove
    file = "data/"+file
    print(file)
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
        item = find_id(id, file, tag, id_type)
        print(item)
        file_data[tag].remove(item)
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return
    


def update_json(id,new_data,file,tag):
    index = 0
    '''
        atualiza dados ao arquivo json
    '''
    #new_data = json.dumps(jsonable_encoder(new_data)) #json.dumps(new_data) # converte dici para json
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
                pass #saio do for pq ja encontrei um id
                print(dado)
                dado_novo = dado
                print(index)
        print(dado_novo)
        item[index] = dado_novo
        file_data[tag] = item
        print(item)
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

# def find_id(cart_id, path,tag):
#     lista_confere = []
#     with open(path, encoding='utf-8') as meu_json:
#         dados = json.load(meu_json)
#         for dado in dados[tag]:
#             if dado['cart_id']==cart_id not in lista_confere:
#                 lista_confere.append(dado['cart_id'])
#                 index = dados.index(dado['cart_id'])
#                 return True
    
#         return False







    
import json
from fastapi.encoders import jsonable_encoder

def find_id(id, file, tag):
    #path = "data/"+file
    with open(file, 'r', encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
        for dado in dados[tag]:
            if dado['cart_id']==id:
                print(f"\n{dado}\n")
                return dado
        return False
        
def read_json(file):
    '''
        le um arquivo em json e retorna seu conteudo
    '''
    file = "data/"+file
    with open(file, "r", encoding='utf-8') as file_data:
        file_data = json.loads(file_data)
        return file_data

def append_json(new_data, file, tag):
    '''
        add dados ao arquivo json
    '''
    #new_data = json.dumps(jsonable_encoder(new_data)) #json.dumps(new_data) # converte dici para json
    new_data = jsonable_encoder(new_data) 
    file = "data/"+file
    with open(file, 'r+') as f:
        file_data = json.load(f)
        file_data[tag].append(new_data)
        f.truncate(0)
        f.seek(0)
        json.dump(file_data,f, indent=4)
        return

def remove_from_json(id, file, tag):
    # verifica se existe o id 
    # se existir, remove
    file = "data/"+file
    print(file)
    
    with open(file, 'r+') as f:
        file_data = json.load(f)
        item = find_id(id, file, tag)
        print(item)
        file_data[tag].remove(item)
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







    
import requests 
import pandas as pd 

def get_data(cep):
    endpoint = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(endpoint)

    if response.status_code == 200:
        cep_info = response.json()
        return cep_info
    else: 
        return None

def get_cep():
    users_path = 'data/01-bronze_raw/users.csv'
    users_df = pd.read_csv(users_path)

    cep_list = users_df['cep'].tolist()
    return cep_list

def search_cep():
    cep_info_list = []

    cep_list = get_cep()
    for cep in cep_list:
        cep_clean = cep.replace('-', '')
        cep_info = get_data(cep_clean)
        print(cep_info)
        if cep_info is None or 'erro' in cep_info:
            continue 
        cep_info_list.append(cep_info)

    return cep_info_list

def cep_info_to_csv():
    cep_info_list = search_cep()
    cep_info_df = pd.DataFrame(cep_info_list)
    cep_info_df.to_csv('data/01-bronze_raw/cep_info.csv', index=False) 

if __name__ == '__main__':
    cep_info_to_csv()
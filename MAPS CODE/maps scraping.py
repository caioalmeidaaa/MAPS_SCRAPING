import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

zipcodes = input(['edson queiroz', 'guararapes', 'varjota', 'aldeota'])  # Substitua 'bairro1', 'bairro2', 'bairro3' e 'bairro4' pelos bairros desejados
tipo_local = input('Informe o tipo de estabelecimento: ')
cidade = input('Informe a cidade de busca: ')

s = Service(r'D:\download\chromedriver')
driver = webdriver.Chrome(service=s)

driver.maximize_window()

for bairro in zipcodes:
    driver.get(f'https://www.google.com/search?q={tipo_local}+em+{bairro}+{cidade}')
    time.sleep(6)
    driver.find_element(By.XPATH, '//*[@id="wp-tabs-container"]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/g-more-link/a/div').click()

    data_set = set()  # Conjunto para armazenar as entradas únicas

    # Hora de fazer a raspagem!!
    while True:
        time.sleep(6)
        main_page = driver.find_elements(By.XPATH, '//div[@class="rllt__details"]')

        for entry in main_page:
            entry.click()

            # Aguardando o javascript abrir
            time.sleep(7)

            # Início da raspagem
            title = driver.find_element(By.XPATH, '//h2/span/span').text

            # Tentar obter a avaliação do estabelecimento
            try:
                rating = driver.find_element(By.CLASS_NAME, 'Aq14fc').text
            except Exception:
                rating = 'sem avaliação'

            location = driver.find_element(By.CLASS_NAME, 'LrzXr').text

            # Verificar se a entrada já existe no conjunto (duplicada)
            if (title, location) in data_set:
                continue

            # Armazenar a entrada única no conjunto
            data_set.add((title, location))

            # Testar o resultado
            print(f'{title}, avaliação = {rating}, localização: {location}')

        # Clicar no botão próxima página
        try:
            next_button = driver.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]')
            next_button.click()
        except Exception:
            break


# Converter o conjunto de dados únicos em uma lista de dicionários
data = [{'Nome': entry[0], 'Avaliação': 'sem avaliação', 'Localização': entry[1]} for entry in data_set]

df = pd.DataFrame(data)

# Salvar o arquivo CSV
filename = f'resultado de {tipo_local} em {cidade} nos bairros {zipcodes}.csv'
df.to_csv(filename, index=False)

# Fechar o navegador
driver.close()

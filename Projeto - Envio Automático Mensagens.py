
### Projeto Envio de mensagens automatizadas ###

#Carregando os pacotes necessarios
import time
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


chromedriver_path = "./chromedriver//chromedriver.exe"
chrome_service = Service(chromedriver_path)
navegador = webdriver.Chrome(service= chrome_service)
navegador.get("https://web.whatsapp.com")
navegador.maximize_window()

#enquanto a lista  de elementos nao for localizado nao passa proxima etapa
while len(navegador.find_elements(By.ID, 'side')) < 1:
    time.sleep(1)
#um tempo maior para carregar a aplicacao do whatsapp Web
time.sleep(5) 

#Carregar o arquivo excel
tabela = pd.read_excel('agenda.xlsx', sheet_name= 'Clientes') 

#Faz um loop por toda a tabela
for linha in tabela.index:
    cliente = tabela.loc[linha,"Cliente"]
    mensagem = tabela.loc[linha,"Mensagem"]
    telefone = tabela.loc[linha,"Telefone"]
    Status = tabela.loc[linha, "Status"]
    
    texto = urllib.parse.quote(f"Oi {cliente},tudo bem? {mensagem}")

    link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"
    navegador.get(link)
    
    #enquanto a lista  de elementos nao for localizado nao passa proxima etapa
    while len(navegador.find_elements(By.ID, 'side')) < 1:
        time.sleep(1)
    time.sleep(2)

    #Verificar se o numero do cliente é válido
    if len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1: 
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()  
        tabela.loc[linha, "Status"] = "Mensagem enviada com Sucesso"
    else:    
        tabela.loc[linha, "Status"] = "Erro: Mensagem não enviada"

    # Aguardar o intervalo de 60s para envio da proxima mensagem    
    time.sleep(20)
    
data_atual = datetime.now().strftime("%Y-%m-%d")
nome_arquivo = f'Retorno_{data_atual}.xlsx'
tabela.to_excel(nome_arquivo, index=False)
print(f'Arquivo {nome_arquivo} gerado em excel com sucesso.')
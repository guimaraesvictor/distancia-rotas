import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from lxml import html
from tqdm import tqdm

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "resultado_rotas.json")

if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)
else:
    resultados = []

destinos = pd.read_excel("calculo_distancia.xlsx")
destinos['LAT-O'] = destinos['LAT-O'].round(5)
destinos['LOG-O'] = destinos['LOG-O'].round(5)
destinos['LAT-D'] = destinos['LAT-D'].round(5)
destinos['LOG-D'] = destinos['LOG-D'].round(5)

for _, des in tqdm(destinos.iterrows(), total=len(destinos), desc="Processando destinos", unit="destino"):    
    origem = f"{des['LAT-O']},{des['LOG-O']}"
    destino = f"{des['LAT-D']},{des['LOG-D']}"
    params = {
        "from": origem,
        "to": destino,
        "v": "",
        "sm": "90",
        "so": "90",
        "fc": "8.00",
        "fp": "6.12"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Referer": "https://www.melhoresrotas.com/"}
    try:
        response = requests.get("https://www.melhoresrotas.com/distancia/", params=params, headers=headers)
        tree = html.fromstring(response.content)

        distancia = tree.xpath("/html/body/div[1]/div[3]/div[1]/table/tbody/tr[2]/td[2]/text()")[0].strip()
        tempo = tree.xpath("/html/body/div[1]/div[3]/div[1]/table/tbody/tr[3]/td[2]/text()")[0].strip()
    except Exception as e:
        distancia = None
        tempo = None
    resultado = {
        "origem": des["CIDADE/UF NORMALIZADO-O"],
        "destino": des["CIDADE/UF NORMALIZADO-D"],
        "distancia": distancia,
        "tempo": tempo}
    resultados.append(resultado)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    time.sleep(0.5)

with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

df = pd.DataFrame(dados)
excel_path = os.path.join(base_dir, "resultado_rotas.xlsx")
df.to_excel(excel_path, index=False)
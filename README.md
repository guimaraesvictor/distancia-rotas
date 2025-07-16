# distancia-rotas
Script de webscraping para consultar a distância e tempo em rota entre 2 pontos (Latitude, Longitude).

## 🔎 Visão Geral
- Consome os pontos de origem e destino no arquivo Excel
- Faz uma request no endpoint do site
- Trata a resposta HTML com BeuatiulSoup
- Preenche um arquivo Json a cada iteração para não perder o histórico
- Consolida o Json em um arquivo Excel

## 📑 Requisitos
- Python 3.12+
- Bibliotecas Python:
  - Pandas
  - os
  - json
  - requests
  - BeautifulSoup
  - time
  - lxml
  - tqdm
  - openpyxl

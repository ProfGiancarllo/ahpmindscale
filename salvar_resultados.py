import csv
import os

def salvar_resultados_csv(dados_dict, nome_arquivo="respostas.csv"):
    arquivo_existe = os.path.exists(nome_arquivo)
    with open(nome_arquivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dados_dict.keys())
        if not arquivo_existe:
            writer.writeheader()
        writer.writerow(dados_dict)

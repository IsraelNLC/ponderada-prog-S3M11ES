from supabase import create_client, Client
import csv
import os
from dotenv import load_dotenv
import time

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("As variáveis de ambiente SUPABASE_URL e SUPABASE_KEY devem estar definidas.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def ingest_data(csv_file_path: str, table_name: str):
    """
    Lê um arquivo CSV e insere os dados na tabela especificada no Supabase.
    
    :param csv_file_path: Caminho do arquivo CSV.
    :param table_name: Nome da tabela no Supabase.
    """
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {"payload": {"dados": row}}
                response = supabase.table(table_name).insert(data).execute()
                print("Dado inserido com sucesso!", response)
                time.sleep(0.1)  # Aguarda 0.1 segundos antes de enviar o próximo dado
    
    except FileNotFoundError:
        print(f"Erro: Arquivo {csv_file_path} não encontrado.")
    except Exception as e:
        print(f"Erro durante a ingestão de dados: {e}")

if __name__ == "__main__":
    ingest_data("../../data/data.csv", "dados")

#!/usr/bin/env python3
# enviar_para_sheets.py — Publicar métricas de GPU no Google Sheets API
# Dependências: pip install google-auth google-api-python-client

import csv
import os
import sys

def main():
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "gpu_log.csv"
    spreadsheet_id = os.environ.get("SHEETS_ID", "")
    cred_file = os.environ.get("GOOGLE_CREDS", "service_account.json")

    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' não existe.")
        return

    if not spreadsheet_id:
        print("Aviso: Variável de ambiente SHEETS_ID não definida. Executando em modo simulação.")
        print(f"Simulando envio dos dados contidos em '{csv_file}'...")
        with open(csv_file, "r", encoding="utf-8") as f:
            total_linhas = sum(1 for _ in f) - 1
        print(f"Modo Simulação: {total_linhas} linhas seriam enviadas para o Google Sheets.")
        return

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            cred_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        linhas = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Pular cabeçalho
            for row in reader:
                linhas.append(row)

        if linhas:
            body = {"values": linhas}
            resultado = sheet.values().append(
                spreadsheetId=spreadsheet_id,
                range="GPU_Logs!A:M",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            print(f"Sucesso! Enviadas {resultado.get('updates', {}).get('updatedRows', len(linhas))} linhas ao Google Sheets.")
        else:
            print("Nenhum dado encontrado para envio.")
    except Exception as e:
        print(f"Erro ao conectar na Google Sheets API: {e}")

if __name__ == "__main__":
    main()

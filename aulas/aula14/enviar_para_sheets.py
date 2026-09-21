#!/usr/bin/env python3
# ============================================================================
# enviar_para_sheets.py — publica o CSV de métricas de GPU no Google Sheets
# ----------------------------------------------------------------------------
# Instalação:
#   pip install google-auth google-api-python-client
#
# Variáveis de ambiente:
#   SHEETS_ID      = ID da planilha (trecho entre /d/ e /edit na URL)
#   GOOGLE_CREDS   = caminho do JSON da service account (padrão: service_account.json)
# ============================================================================
import csv
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.environ["SHEETS_ID"]          # ID da planilha
RANGE_NAME     = "GPU_Logs!A:M"                   # aba + colunas
CRED_FILE      = os.environ.get("GOOGLE_CREDS", "service_account.json")
CSV_ARQUIVO    = os.environ.get("GPU_CSV", "gpu_log.csv")

# ── Autenticar com a service account ────────────────────────────────────────
creds = service_account.Credentials.from_service_account_file(
    CRED_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# ── Ler o CSV local (pulando o cabeçalho) ───────────────────────────────────
linhas = []
with open(CSV_ARQUIVO, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # pula o cabeçalho
    for row in reader:
        linhas.append(row)

# ── Anexar as linhas à planilha ─────────────────────────────────────────────
if linhas:
    body = {"values": linhas}
    resultado = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()
    print(f"Enviadas {resultado['updates']['updatedRows']} linhas ao Google Sheets.")
else:
    print("Nenhum dado para enviar.")

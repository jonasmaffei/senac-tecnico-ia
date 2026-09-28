#!/usr/bin/env python3
# ============================================================================
# enviar_para_sheets.py — publica o CSV de métricas de GPU no Google Sheets
# ----------------------------------------------------------------------------
# Instalação (opcional, só para enviar de verdade):
#   pip install google-auth google-api-python-client
#
# Variáveis de ambiente:
#   SHEETS_ID      = ID da planilha (trecho entre /d/ e /edit na URL)
#   GOOGLE_CREDS   = caminho do JSON da service account (padrão: service_account.json)
#   GPU_CSV        = caminho do CSV de entrada (padrão: gpu_log.csv)
#
# Sem credenciais, o script NÃO falha: apenas avisa e encerra (útil no Colab).
# ============================================================================
import csv
import os
import sys

SPREADSHEET_ID = os.environ.get("SHEETS_ID", "")          # ID da planilha
RANGE_NAME     = "GPU_Logs!A:M"                           # aba + colunas
CRED_FILE      = os.environ.get("GOOGLE_CREDS", "service_account.json")
CSV_ARQUIVO    = os.environ.get("GPU_CSV", "gpu_log.csv")

# ── Verificação amigável: sem credenciais não há o que enviar ───────────────
if not SPREADSHEET_ID or not os.path.exists(CRED_FILE):
    print("Sem credenciais do Google Sheets — nada a enviar.")
    print("Defina SHEETS_ID e GOOGLE_CREDS (JSON da service account) para publicar.")
    print("No Colab: envie o service_account.json e exporte as variáveis.")
    sys.exit(0)

# As importações do Google ficam aqui (só são necessárias com credenciais)
from google.oauth2 import service_account
from googleapiclient.discovery import build

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

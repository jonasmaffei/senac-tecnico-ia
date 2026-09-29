import csv
import os
import sys

def main():
    csv_file = os.path.join("reports", "gpu_log.csv")
    spreadsheet_id = os.environ.get("SHEETS_ID", "")
    cred_file = os.environ.get("GOOGLE_CREDS", "service_account.json")

    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' nao encontrado. Execute o monitoramento primeiro.")
        return

    if not spreadsheet_id:
        print("Modo de Simulacao: Variavel 'SHEETS_ID' nao configurada no ambiente.")
        with open(csv_file, "r", encoding="utf-8") as f:
            total = sum(1 for _ in f) - 1
        print(f"[Simulacao] {total} linhas de telemetria prontas para envio a Google Sheets API.")
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
            next(reader, None)
            for row in reader:
                linhas.append(row)

        if linhas:
            body = {"values": linhas}
            res = sheet.values().append(
                spreadsheetId=spreadsheet_id,
                range="GPU_Logs!A:M",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            print(f"Sucesso! {res.get('updates', {}).get('updatedRows', len(linhas))} linhas publicadas no Google Sheets.")
    except Exception as e:
        print(f"Erro na conexao com Google Sheets: {e}")

if __name__ == "__main__":
    main()

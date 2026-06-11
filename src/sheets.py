import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def register_test_locally(test_name, partner, period, winner, roi, profit, decision, description):
    """
    Registra o resultado do teste no arquivo CSV local em output/historico_testes.csv
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "historico_testes.csv")
    
    headers = [
        "Teste", 
        "Parceiro", 
        "Data da Analise", 
        "Periodo do Teste", 
        "Vencedor", 
        "ROI do Vencedor", 
        "Lucro Total do Vencedor", 
        "Decisao", 
        "Descricao"
    ]
    
    file_exists = os.path.exists(csv_path)
    
    # Formata as métricas para gravação
    roi_str = f"{roi * 100:.1f}%" if roi is not None else "N/A"
    profit_str = f"R$ {profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if profit is not None else "N/A"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    row = [
        test_name,
        partner,
        date_str,
        period,
        winner if winner else "Nenhum",
        roi_str,
        profit_str,
        decision,
        description
    ]
    
    try:
        with open(csv_path, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';') # Usa ponto e vírgula para melhor abertura no Excel/Sheets
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)
        print(f"Teste registrado localmente em {csv_path}")
        return True
    except Exception as e:
        print(f"Erro ao registrar o teste localmente: {str(e)}")
        return False

def register_test_in_google_sheets(test_name, partner, period, winner, roi, profit, decision, description):
    """
    Registra o resultado do teste no Google Sheets.
    Suporta dois métodos de integração:
    1. Através de um Google Apps Script Web App (sem necessidade de credenciais do Google Cloud).
    2. Através de uma Conta de Serviço do Google Cloud (gspread + service_account.json).
    """
    web_app_url = os.getenv("GOOGLE_WEB_APP_URL")
    
    # Método 1: Integração direta via Google Apps Script Web App (Zero-GCP, Recomendado por facilidade)
    if web_app_url and web_app_url != "sua_url_do_web_app_aqui":
        try:
            import requests
            
            roi_str = f"{roi * 100:.1f}%" if roi is not None else "N/A"
            profit_str = f"R$ {profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if profit is not None else "N/A"
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            payload = {
                "test_name": test_name,
                "partner": partner,
                "date_str": date_str,
                "period": period,
                "winner": winner if winner else "Nenhum",
                "roi_str": roi_str,
                "profit_str": profit_str,
                "decision": decision,
                "description": description
            }
            
            response = requests.post(web_app_url, json=payload, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("status") == "success":
                    print("Teste registrado com sucesso no Google Sheets (via Web App API)")
                    return True
                else:
                    print(f"Erro do Web App: {res_json.get('message')}")
            else:
                print(f"Erro HTTP do Web App: {response.status_code}")
        except Exception as e:
            print(f"Falha na integração direta via Web App: {str(e)}. Tentando fallback para Conta de Serviço...")
            
    # Método 2: Conta de Serviço do Google Cloud (gspread)
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    
    if not sheet_id:
        print("Aviso: GOOGLE_SHEET_ID ausente no ambiente. Integração com o Google Sheets pulada.")
        return False
        
    if not os.path.exists(creds_file):
        print(f"Aviso: Arquivo de credenciais do Google '{creds_file}' não encontrado. Integração com o Google Sheets pulada.")
        print("Por favor, cole suas credenciais ou utilize a URL de integração direta Google Apps Script.")
        return False
        
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("Aviso: A biblioteca 'gspread' ou 'google-auth' não está instalada. Execute 'pip install -r requirements.txt'")
        return False
        
    try:
        # Define os escopos
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(creds_file, scopes=scopes)
        gc = gspread.authorize(credentials)
        
        # Abre pelo ID
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.get_worksheet(0) # Seleciona a primeira página
        
        # Formata as métricas
        roi_str = f"{roi * 100:.1f}%" if roi is not None else "N/A"
        profit_str = f"R$ {profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if profit is not None else "N/A"
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verifica se os cabeçalhos precisam ser gravados (se a planilha estiver vazia)
        existing_values = worksheet.get_all_values()
        if not existing_values:
            headers = [
                "Teste", 
                "Parceiro", 
                "Data da Análise", 
                "Período do Teste", 
                "Vencedor", 
                "ROI do Vencedor", 
                "Lucro Total do Vencedor", 
                "Decisão", 
                "Descrição"
            ]
            worksheet.append_row(headers)
            
        row = [
            test_name,
            partner,
            date_str,
            period,
            winner if winner else "Nenhum",
            roi_str,
            profit_str,
            decision,
            description
        ]
        
        worksheet.append_row(row)
        print(f"Teste registrado com sucesso no Google Sheets: {sh.url}")
        return True
        
    except Exception as e:
        print(f"Erro ao registrar o teste no Google Sheets: {str(e)}")
        print("Verifique o ID da planilha, as credenciais e garanta que o e-mail da conta de serviço está compartilhado na planilha.")
        return False

def register_test_result(test_name, partner, period, winner, roi, profit, decision, description):
    """
    Orquestrador principal para registrar os resultados do teste localmente e no Google Sheets.
    """
    # Sempre registra localmente primeiro
    local_success = register_test_locally(
        test_name, partner, period, winner, roi, profit, decision, description
    )
    
    # Tenta a sincronização com o Google Sheets
    sheets_success = register_test_in_google_sheets(
        test_name, partner, period, winner, roi, profit, decision, description
    )
    
    return local_success, sheets_success

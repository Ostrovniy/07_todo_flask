import requests

def get_ngrok_url():
    """Получить текущий ЮРЛ домена"""
    try:
        # URL для доступа к локальному API ngrok
        api_url = "http://127.0.0.1:4040/api/tunnels"
        response = requests.get(api_url)
        response.raise_for_status()  # Проверяем на ошибки

        # Получаем список туннелей
        tunnels = response.json().get("tunnels", [])
        if not tunnels:
            raise Exception("No active ngrok tunnels found.")
        
        # Возвращаем первый публичный URL
        public_url = tunnels[0].get("public_url")
        if not public_url:
            raise Exception("No public URL found for the tunnel.")
        
        return public_url
    except Exception as e:
        print(f"Error: {e}")
        return None
    


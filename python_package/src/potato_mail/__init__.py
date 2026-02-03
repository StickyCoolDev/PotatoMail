import requests
from typing import Optional, Dict, Any

class PotatoMailError(Exception):
    """Exception raised for errors in the PotatoMail API."""
    pass

class Client:
    def __init__(self, api_key: str, base_url: str = "http://localhost:2000") -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def send_email(
        self, 
        subject: str, 
        receiver_email: str, 
        body: str, 
        html_body: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends an email via the PotatoMail API.
        
        :param subject: The subject line of the email.
        :param receiver_email: The recipient's email address.
        :param body: Plain text version of the email.
        :param html_body: Optional HTML content for rich formatting.
        :return: JSON response from the server.
        """
        endpoint = f"{self.base_url}/send_email"
        
        payload = {
            "Subject": subject,
            "Body": body,
            "Receiver mail": receiver_email
        }
        
        if html_body:
            payload["Html Body"] = html_body

        try:
            response = self.session.post(endpoint, json=payload)
            
            if response.status_code == 401:
                raise PotatoMailError("Unauthorized: Invalid API Key.")
            elif response.status_code == 400:
                raise PotatoMailError(f"Bad Request: {response.text}")
            elif response.status_code >= 500:
                raise PotatoMailError(f"Server Error: {response.status_code}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise PotatoMailError(f"Connection failed: {str(e)}")


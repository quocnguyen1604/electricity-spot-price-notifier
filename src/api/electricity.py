import requests

class ElectricityAPI:
    def __init__ (self, base_url, tulos):
        self.base_url = base_url
        self.tulos = tulos

    def getSpotPrice(self, date):
        params = {
            "aikaraja": date,
            "tulos": self.tulos,
        }
    
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
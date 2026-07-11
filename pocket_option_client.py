from pocket_option import PocketOption
from config import POCKET_OPTION_EMAIL, POCKET_OPTION_PASSWORD
import time

class PocketOptionClient:
    
    def __init__(self):
        self.client = PocketOption(
            email=POCKET_OPTION_EMAIL,
            password=POCKET_OPTION_PASSWORD
        )
        self.is_connected = False
    
    def connect(self):
        """Conecta con Pocket Option"""
        try:
            print("🔗 Conectando a Pocket Option...")
            self.client.connect()
            self.is_connected = True
            print("✅ Conectado a Pocket Option")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_candles(self, asset, timeframe=15, count=50):
        """Obtiene velas históricas"""
        try:
            candles = self.client.get_candles(
                asset=asset,
                period=timeframe,
                count=count
            )
            return candles
        except Exception as e:
            print(f"❌ Error al obtener velas: {e}")
            return None
    
    def subscribe_to_live(self, asset, callback):
        """Suscribe a datos en vivo"""
        try:
            self.client.subscribe_to_candle_data(
                asset=asset,
                period=15,
                callback=callback
            )
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def disconnect(self):
        """Desconecta"""
        try:
            self.client.disconnect()
            self.is_connected = False
        except:
            pass
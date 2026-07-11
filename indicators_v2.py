import asyncio
import numpy as np
import pandas as pd
from datetime import datetime
import pytz
from typing import Dict, List, Tuple
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Indicators:
    """Calcula Williams Alligator, DeMarker y Momentum"""
    
    @staticmethod
    def williams_alligator(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Dict:
        """
        Williams Alligator:
        - Mandíbula (Azul): SMA(13, shift 8)
        - Dientes (Rojo): SMA(8, shift 5)
        - Labios (Verde): SMA(5, shift 3)
        """
        hl2 = (high + low) / 2
        
        jaw = pd.Series(hl2).rolling(window=13).mean().shift(8).values
        teeth = pd.Series(hl2).rolling(window=8).mean().shift(5).values
        lips = pd.Series(hl2).rolling(window=5).mean().shift(3).values
        
        return {
            'jaw': jaw,
            'teeth': teeth,
            'lips': lips
        }
    
    @staticmethod
    def demarker(high: np.ndarray, low: np.ndarray, period: int = 15) -> np.ndarray:
        """DeMarker período 15: 0-100 (30=sobreventa, 70=sobrecompra)"""
        dmax = np.where(high > np.roll(high, 1), high - np.roll(high, 1), 0)
        dmin = np.where(low < np.roll(low, 1), np.roll(low, 1) - low, 0)
        
        dmax_sum = pd.Series(dmax).rolling(window=period).sum()
        dmin_sum = pd.Series(dmin).rolling(window=period).sum()
        
        demarker = 100 * dmax_sum / (dmax_sum + dmin_sum)
        return demarker.values
    
    @staticmethod
    def momentum(close: np.ndarray, period: int = 15) -> np.ndarray:
        """Momentum: close - close[período atrás]"""
        momentum = np.array(close) - np.roll(np.array(close), period)
        return momentum
    
    @staticmethod
    def calculate_all(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Dict:
        """Calcula todos los indicadores"""
        return {
            'alligator': Indicators.williams_alligator(high, low, close),
            'demarker': Indicators.demarker(high, low, 15),
            'momentum': Indicators.momentum(close, 15)
        }


class SignalDetector:
    """Detecta señales BAJA (PUT) o ALZA (CALL)"""
    
    def __init__(self):
        self.last_signal = None
        self.last_signal_time = None
    
    def detect_signal(self, alligator: Dict, demarker: np.ndarray, 
                     momentum: np.ndarray) -> Tuple[str, str]:
        """
        Detecta señales de entrada completa
        
        SEÑAL BAJA (PUT):
        - Alligator: Mandíbula > Dientes > Labios (comprimida)
        - DeMarker: Baja hacia 30 (sobreventa)
        - Momentum: Negativo y acelerando hacia abajo
        
        SEÑAL ALZA (CALL):
        - Alligator: Labios > Dientes > Mandíbula (comprimida)
        - DeMarker: Sube hacia 70 (sobrecompra)
        - Momentum: Positivo y acelerando hacia arriba
        """
        
        jaw = alligator['jaw'][-1]
        teeth = alligator['teeth'][-1]
        lips = alligator['lips'][-1]
        
        demarker_val = demarker[-1]
        momentum_val = momentum[-1]
        momentum_prev = momentum[-2] if len(momentum) > 1 else momentum[-1]
        
        # Evitar señales duplicadas en corto tiempo
        if self.last_signal_time:
            time_diff = (datetime.now() - self.last_signal_time).total_seconds()
            if time_diff < 60:  # 60 segundos de espera entre señales
                return "WAIT", "Esperando 60 segundos entre señales"
        
        # SEÑAL BAJA (PUT)
        if (jaw > teeth > lips and 
            abs(jaw - lips) > 0.0001 and
            demarker_val < 35 and
            momentum_val < 0 and
            momentum_val < momentum_prev):
            
            self.last_signal = "PUT"
            self.last_signal_time = datetime.now()
            return "ENTRY", "PUT"
        
        # SEÑAL ALZA (CALL)
        elif (lips > teeth > jaw and
              abs(lips - jaw) > 0.0001 and
              demarker_val > 65 and
              momentum_val > 0 and
              momentum_val > momentum_prev):
            
            self.last_signal = "CALL"
            self.last_signal_time = datetime.now()
            return "ENTRY", "CALL"
        
        return "NO_SIGNAL", "Sin señal en este momento"


class TelegramAlert:
    """Envía alertas a Telegram"""
    
    @staticmethod
    def send_alert(asset: str, signal_type: str, indicators_data: Dict = None):
        """Envía alerta de entrada a Telegram"""
        
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not token or not chat_id:
            print("❌ Error: TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configurados")
            return False
        
        timestamp = datetime.now(pytz.timezone('America/Bogota')).strftime("%H:%M:%S")
        
        if signal_type == "PUT":
            message = f"""
🚨 SEÑAL BAJA (PUT) 🚨

🎯 Activo: {asset} OTC
📊 Tipo: VENTA (PUT)
⏱️ Expiración: 1 minuto
🕐 Hora: {timestamp}

✅ Confirmación:
✓ Alligator separado
✓ DeMarker < 35
✓ Momentum negativo

💡 ENTRA AHORA EN VENTA
            """
        else:  # CALL
            message = f"""
🚨 SEÑAL ALZA (CALL) 🚨

🎯 Activo: {asset} OTC
📊 Tipo: COMPRA (CALL)
⏱️ Expiración: 1 minuto
🕐 Hora: {timestamp}

✅ Confirmación:
✓ Alligator separado
✓ DeMarker > 65
✓ Momentum positivo

💡 ENTRA AHORA EN COMPRA
            """
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Alerta enviada a Telegram: {signal_type}")
                return True
            else:
                print(f"❌ Error en Telegram: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error de conexión a Telegram: {e}")
            return False
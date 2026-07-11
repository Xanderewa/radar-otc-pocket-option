import time
from pocket_option_client import PocketOptionClient
from indicators import Indicators, SignalDetector
from telegram_alerts import TelegramAlert
from config import ASSETS_TO_MONITOR
import numpy as np
from datetime import datetime

class RadarOTCBot:
    
    def __init__(self):
        self.client = PocketOptionClient()
        self.detector = SignalDetector()
        self.indicators_calc = Indicators()
        self.candle_buffers = {}
        
        for asset in ASSETS_TO_MONITOR:
            self.candle_buffers[asset] = {
                'high': [],
                'low': [],
                'close': [],
                'timestamp': []
            }
    
    def on_candle_update(self, asset, candle):
        """Callback cuando llega una vela"""
        print(f"🕐 Vela {asset}: {candle}")
        
        self.candle_buffers[asset]['high'].append(candle.get('high', 0))
        self.candle_buffers[asset]['low'].append(candle.get('low', 0))
        self.candle_buffers[asset]['close'].append(candle.get('close', 0))
        self.candle_buffers[asset]['timestamp'].append(datetime.now())
        
        if len(self.candle_buffers[asset]['high']) > 50:
            for key in self.candle_buffers[asset]:
                self.candle_buffers[asset][key] = self.candle_buffers[asset][key][-50:]
        
        self.analyze_asset(asset)
    
    def analyze_asset(self, asset):
        """Analiza con indicadores"""
        
        buffer = self.candle_buffers[asset]
        
        if len(buffer['close']) < 15:
            return
        
        high = np.array(buffer['high'])
        low = np.array(buffer['low'])
        close = np.array(buffer['close'])
        
        alligator = self.indicators_calc.williams_alligator(high, low, close)
        demarker = self.indicators_calc.demarker(high, low, period=15)
        momentum = self.indicators_calc.momentum(close, period=15)
        
        # Fase 1
        pre_alert = self.detector.phase1_pre_alert(alligator, demarker, momentum, asset)
        if pre_alert:
            print(f"📢 PRE-ALERTA en {asset}: {pre_alert}")
            TelegramAlert.send_pre_alert(asset, pre_alert)
        
        # Fase 2
        entry = self.detector.phase2_entry(alligator, demarker, momentum, asset)
        if entry:
            print(f"🚨 ENTRADA en {asset}: {entry}")
            TelegramAlert.send_entry_alert(asset, entry)
    
    def run(self):
        """Ejecuta el bot"""
        
        print("🤖 Iniciando Radar OTC...")
        
        if not self.client.connect():
            print("❌ No se pudo conectar")
            return
        
        for asset in ASSETS_TO_MONITOR:
            print(f"📊 Monitoreando {asset}...")
            self.client.subscribe_to_live(asset, self.on_candle_update)
        
        print("✅ Bot en ejecución...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ Bot detenido")
            self.client.disconnect()

if __name__ == "__main__":
    bot = RadarOTCBot()
    bot.run()
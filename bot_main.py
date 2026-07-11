import asyncio
import numpy as np
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os
import sys
from indicators_v2 import Indicators, SignalDetector, TelegramAlert

load_dotenv()

# Intenta importar la librería de Pocket Option
try:
    from pocketoptionapi_async import AsyncPocketOptionClient
    print("✅ Librería pocketoptionapi-async importada correctamente")
except ImportError:
    print("❌ Error: No se encontró pocketoptionapi-async")
    print("Instala con: pip install pocketoptionapi-async")
    sys.exit(1)


class RadarOTCBot:
    """Bot de Trading OTC con estrategia Williams Alligator"""
    
    def __init__(self):
        self.client = None
        self.signal_detector = SignalDetector()
        self.indicators = Indicators()
        self.assets_to_monitor = ["EURUSD"]  # Puedes agregar más activos
        self.candle_buffers = {}
        self.is_running = False
        
        # Configurar buffers para cada activo
        for asset in self.assets_to_monitor:
            self.candle_buffers[asset] = {
                'time': [],
                'open': [],
                'high': [],
                'low': [],
                'close': [],
                'volume': []
            }
    
    async def initialize_connection(self):
        """Inicializa la conexión con Pocket Option"""
        
        # Obtener SSID del archivo .env
        ssid = os.getenv("POCKET_OPTION_SSID")
        
        if not ssid:
            print("❌ Error: POCKET_OPTION_SSID no encontrado en .env")
            print("📋 Instrucciones:")
            print("1. Abre PocketOption en tu navegador")
            print("2. Presiona F12 para abrir DevTools")
            print("3. Ve a Network > Filter 'WS'")
            print("4. Busca mensaje que comience con: 42[\"auth\",")
            print("5. Copia TODO el mensaje")
            print("6. Agrégalo a .env como: POCKET_OPTION_SSID=tu_mensaje_aqui")
            return False
        
        try:
            print("🔗 Conectando a Pocket Option...")
            
            # Crear cliente asincrónico
            self.client = AsyncPocketOptionClient(
                ssid=ssid,
                is_demo=True,  # Cambiar a False para trading real
                persistent_connection=True,
                auto_reconnect=True
            )
            
            # Conectar
            connected = await self.client.connect()
            
            if connected:
                print("✅ Conectado a Pocket Option exitosamente")
                
                # Obtener balance
                try:
                    balance = await self.client.get_balance()
                    print(f"💰 Balance: {balance.balance} {balance.currency}")
                except Exception as e:
                    print(f"⚠️ No se pudo obtener balance: {e}")
                
                return True
            else:
                print("❌ Fallo la conexión a Pocket Option")
                return False
                
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            return False
    
    async def get_historical_candles(self, asset: str, count: int = 50) -> bool:
        """Obtiene velas históricas para inicializar los buffers"""
        
        try:
            print(f"📊 Obteniendo {count} velas de {asset}...")
            
            # Obtener velas del último período (15 minutos)
            candles = await self.client.get_candles(
                asset=asset,
                period=15,  # 15 minutos
                count=count
            )
            
            if candles and len(candles) > 0:
                print(f"✅ Obtenidas {len(candles)} velas de {asset}")
                
                # Llenar el buffer
                for candle in candles:
                    self.candle_buffers[asset]['time'].append(candle.time)
                    self.candle_buffers[asset]['open'].append(candle.open)
                    self.candle_buffers[asset]['high'].append(candle.high)
                    self.candle_buffers[asset]['low'].append(candle.low)
                    self.candle_buffers[asset]['close'].append(candle.close)
                    self.candle_buffers[asset]['volume'].append(candle.volume or 0)
                
                return True
            else:
                print(f"⚠️ No se obtuvieron velas para {asset}")
                return False
                
        except Exception as e:
            print(f"❌ Error al obtener velas: {e}")
            return False
    
    async def on_candle_received(self, asset: str, candle):
        """Callback cuando llega una nueva vela"""
        
        print(f"\n📈 Nueva vela {asset}:")
        print(f"   Hora: {datetime.fromtimestamp(candle.time)}")
        print(f"   Open: {candle.open} | High: {candle.high} | Low: {candle.low} | Close: {candle.close}")
        
        # Agregar a buffer
        self.candle_buffers[asset]['time'].append(candle.time)
        self.candle_buffers[asset]['open'].append(candle.open)
        self.candle_buffers[asset]['high'].append(candle.high)
        self.candle_buffers[asset]['low'].append(candle.low)
        self.candle_buffers[asset]['close'].append(candle.close)
        self.candle_buffers[asset]['volume'].append(candle.volume or 0)
        
        # Mantener solo las últimas 50 velas
        max_candles = 50
        for key in self.candle_buffers[asset]:
            if len(self.candle_buffers[asset][key]) > max_candles:
                self.candle_buffers[asset][key] = self.candle_buffers[asset][key][-max_candles:]
        
        # Analizar
        await self.analyze_asset(asset)
    
    async def analyze_asset(self, asset: str):
        """Analiza el activo con los indicadores"""
        
        buffer = self.candle_buffers[asset]
        
        # Necesitamos al menos 20 velas para análisis
        if len(buffer['close']) < 20:
            print(f"⏳ Esperando más datos... ({len(buffer['close'])}/20 velas)")
            return
        
        # Convertir a numpy arrays
        high = np.array(buffer['high'], dtype=np.float64)
        low = np.array(buffer['low'], dtype=np.float64)
        close = np.array(buffer['close'], dtype=np.float64)
        
        try:
            # Calcular indicadores
            print("🔍 Calculando indicadores...")
            indicators_data = self.indicators.calculate_all(high, low, close)
            
            alligator = indicators_data['alligator']
            demarker = indicators_data['demarker']
            momentum = indicators_data['momentum']
            
            # Mostrar valores actuales
            print(f"   Alligator - Jaw: {alligator['jaw'][-1]:.5f} | Teeth: {alligator['teeth'][-1]:.5f} | Lips: {alligator['lips'][-1]:.5f}")
            print(f"   DeMarker: {demarker[-1]:.2f}")
            print(f"   Momentum: {momentum[-1]:.6f}")
            
            # Detectar señal
            signal_type, signal_value = self.signal_detector.detect_signal(
                alligator, demarker, momentum
            )
            
            if signal_type == "ENTRY":
                print(f"\n🚨🚨🚨 ¡SEÑAL GENERADA! 🚨🚨🚨")
                print(f"Tipo: {signal_value}")
                
                # Enviar alerta a Telegram
                TelegramAlert.send_alert(asset, signal_value, indicators_data)
            
            elif signal_type == "WAIT":
                print(f"⏳ {signal_value}")
            
            else:
                print("⏸️  Sin señal en este momento")
                
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            import traceback
            traceback.print_exc()
    
    async def subscribe_to_candles(self):
        """Se suscribe a las velas en tiempo real"""
        
        try:
            print("\n📡 Suscribiéndose a velas en tiempo real...")
            
            for asset in self.assets_to_monitor:
                # Obtener velas históricas primero
                await self.get_historical_candles(asset)
                
                # Suscribirse a velas en vivo
                await self.client.subscribe_to_candle_data(
                    asset=asset,
                    period=15,  # 15 minutos
                    callback=lambda candle, a=asset: self.on_candle_received(a, candle)
                )
                
                print(f"✅ Suscrito a {asset}")
            
        except Exception as e:
            print(f"❌ Error en suscripción: {e}")
    
    async def run(self):
        """Ejecuta el bot"""
        
        print("\n" + "="*60)
        print("🤖 RADAR OTC - BOT DE TRADING")
        print("="*60)
        print(f"⏰ Inicio: {datetime.now(pytz.timezone('America/Bogota')).strftime('%H:%M:%S')}")
        print("="*60 + "\n")
        
        self.is_running = True
        
        try:
            # Conectar a Pocket Option
            if not await self.initialize_connection():
                print("❌ No se pudo conectar a Pocket Option")
                return
            
            # Suscribirse a velas
            await self.subscribe_to_candles()
            
            print("\n✅ Bot en ejecución...")
            print("💡 Esperando señales de trading...\n")
            
            # Mantener el bot corriendo
            while self.is_running:
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n⛔ Bot detenido por el usuario")
        
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Desconectar
            if self.client:
                print("\n🔌 Desconectando...")
                await self.client.disconnect()
                print("✅ Desconectado")


async def main():
    """Función principal"""
    bot = RadarOTCBot()
    await bot.run()


if __name__ == "__main__":
    # Ejecutar bot
    asyncio.run(main())
import numpy as np
import pandas as pd

class Indicators:
    """Calcula Williams Alligator, DeMarker y Momentum"""
    
    @staticmethod
    def williams_alligator(high, low, close):
        """
        Williams Alligator:
        - Mandíbula (Rosa): SMA(15, offset 5)
        - Dientes (Naranja): SMA(10, offset 3)
        - Labios (Turquesa): SMA(5, offset 1)
        """
        hl2 = (high + low) / 2
        
        jaw = pd.Series(hl2).rolling(window=15).mean().shift(5).values
        teeth = pd.Series(hl2).rolling(window=10).mean().shift(3).values
        lips = pd.Series(hl2).rolling(window=5).mean().shift(1).values
        
        return {
            'jaw': jaw,
            'teeth': teeth,
            'lips': lips
        }
    
    @staticmethod
    def demarker(high, low, period=15):
        """DeMarker período 15: 0-100 (30=sobreventa, 70=sobrecompra)"""
        dmax = np.where(high > np.roll(high, 1), high - np.roll(high, 1), 0)
        dmin = np.where(low < np.roll(low, 1), np.roll(low, 1) - low, 0)
        
        dmax_sum = pd.Series(dmax).rolling(window=period).sum()
        dmin_sum = pd.Series(dmin).rolling(window=period).sum()
        
        demarker = 100 * dmax_sum / (dmax_sum + dmin_sum)
        return demarker.values
    
    @staticmethod
    def momentum(close, period=15):
        """Momentum: close - close[período atrás]"""
        momentum = np.array(close) - np.roll(np.array(close), period)
        return momentum

class SignalDetector:
    """Detecta señales de entrada en 2 fases"""
    
    def __init__(self):
        self.pre_alert_sent = {}
    
    def phase1_pre_alert(self, alligator, demarker, momentum, asset):
        """Fase 1: Preparación del movimiento"""
        jaw, teeth, lips = alligator['jaw'][-1], alligator['teeth'][-1], alligator['lips'][-1]
        demarker_val = demarker[-1]
        momentum_val = momentum[-1]
        momentum_prev = momentum[-2] if len(momentum) > 1 else momentum[-1]
        
        # Condiciones para BAJA
        baja_condition = (
            jaw > teeth > lips and
            abs(jaw - lips) > 0.001 and
            demarker_val > 40 and demarker_val < 50 and
            momentum_val < 0 < momentum_prev
        )
        
        # Condiciones para ALZA
        alza_condition = (
            lips > teeth > jaw and
            abs(lips - jaw) > 0.001 and
            demarker_val > 50 and demarker_val < 60 and
            momentum_val > 0 > momentum_prev
        )
        
        if baja_condition:
            return "PRE_ALERT_BAJA"
        elif alza_condition:
            return "PRE_ALERT_ALZA"
        
        return None
    
    def phase2_entry(self, alligator, demarker, momentum, asset):
        """Fase 2: Confirmación para entrada"""
        jaw, teeth, lips = alligator['jaw'][-1], alligator['teeth'][-1], alligator['lips'][-1]
        demarker_val = demarker[-1]
        momentum_val = momentum[-1]
        momentum_prev = momentum[-2] if len(momentum) > 1 else momentum[-1]
        
        # VENTA
        venta_condition = (
            jaw > teeth > lips and
            abs(jaw - lips) > 0.002 and
            demarker_val < 30 and
            momentum_val < momentum_prev and
            momentum_val < 0
        )
        
        # COMPRA
        compra_condition = (
            lips > teeth > jaw and
            abs(lips - jaw) > 0.002 and
            demarker_val > 70 and
            momentum_val > momentum_prev and
            momentum_val > 0
        )
        
        if venta_condition:
            return "ENTRY_VENTA"
        elif compra_condition:
            return "ENTRY_COMPRA"
        
        return None
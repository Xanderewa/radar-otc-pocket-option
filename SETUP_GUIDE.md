# 🤖 GUÍA DE CONFIGURACIÓN - RADAR OTC BOT

## 📋 REQUISITOS PREVIOS

- Python 3.8+
- Cuenta en Pocket Option
- Acceso a Telegram
- Tu SSID de Pocket Option

---

## 🔧 PASO 1: OBTENER TU SSID DE POCKET OPTION

### En tu navegador (PC o Celular):

1. **Abre Pocket Option:**
   - Ve a https://pocketoption.com
   - Inicia sesión con tus credenciales

2. **Abre DevTools:**
   - Presiona **F12** (o Click derecho → Inspeccionar)
   - Ve a la pestaña **"Network"**

3. **Filtra WebSocket:**
   - En el filtro, escribe: `WS`
   - O busca los mensajes con "ws"

4. **Busca el mensaje de autenticación:**
   - Busca un mensaje que comience con: `42["auth",`
   - Verá algo como:
   ```
   42["auth",{"session":"tu_sesion_aqui","isDemo":1,"uid":12345,"platform":1}]
   ```

5. **Copia TODO el mensaje:**
   - Copia desde el primer `4` hasta el último `]`

---

## 🔑 PASO 2: ACTUALIZAR EL ARCHIVO .env

En tu repositorio, abre el archivo `.env` y agrega:

```env
# Telegram
TELEGRAM_BOT_TOKEN=8822818498:AAFmuBxNyRogaXYgT3MnOTVCTj8dwKfqgmw
TELEGRAM_CHAT_ID=-1003915863677

# Pocket Option
POCKET_OPTION_SSID=42["auth",{"session":"tu_sesion_aqui","isDemo":1,"uid":12345,"platform":1}]
```

⚠️ **IMPORTANTE:** 
- El `SSID` debe ser el mensaje COMPLETO que copiaste
- No olvides la estructura: `42["auth",{...}]`

---

## 💻 PASO 3: INSTALAR DEPENDENCIAS

En tu terminal (o Termux si es celular):

```bash
# Navega a la carpeta del proyecto
cd radar-otc-pocket-option

# Instala las dependencias
pip install -r requirements.txt
```

**Si tienes problemas con `pocketoptionapi-async`:**

```bash
pip install pocketoptionapi-async --upgrade
```

---

## 🚀 PASO 4: EJECUTAR EL BOT

```bash
python bot_main.py
```

**Verás algo como:**

```
============================================================
🤖 RADAR OTC - BOT DE TRADING
============================================================
⏰ Inicio: 14:30:45
============================================================

✅ Librería pocketoptionapi-async importada correctamente
🔗 Conectando a Pocket Option...
✅ Conectado a Pocket Option exitosamente
💰 Balance: 1000.00 USD
📊 Obteniendo 50 velas de EURUSD...
✅ Obtenidas 50 velas de EURUSD
📡 Suscribiéndose a velas en tiempo real...
✅ Suscrito a EURUSD

✅ Bot en ejecución...
💡 Esperando señales de trading...
```

---

## 📱 PASO 5: RECIBIR ALERTAS EN TELEGRAM

Cuando se genere una señal, recibirás un mensaje en tu canal:

```
🚨 SEÑAL BAJA (PUT) 🚨

🎯 Activo: EURUSD OTC
📊 Tipo: VENTA (PUT)
⏱️ Expiración: 1 minuto
🕐 Hora: 14:35:22

✅ Confirmación:
✓ Alligator separado
✓ DeMarker < 35
✓ Momentum negativo

💡 ENTRA AHORA EN VENTA
```

---

## 🔄 CAMBIAR ACTIVOS A MONITOREAR

Si quieres monitorear otros activos además de EURUSD:

**En `bot_main.py`, línea ~30:**

```python
self.assets_to_monitor = ["EURUSD", "GBPUSD", "XAUUSD"]  # Agrega más aquí
```

---

## 🎚️ CAMBIAR A TRADING REAL

**En `bot_main.py`, línea ~133:**

```python
# DEMO MODE (por defecto)
self.client = AsyncPocketOptionClient(
    ssid=ssid,
    is_demo=True,  # ← CAMBIAR A False para REAL
    persistent_connection=True,
    auto_reconnect=True
)
```

⚠️ **ADVERTENCIA:** Solo cambia a `False` si estás seguro de lo que haces.

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### ❌ "POCKET_OPTION_SSID no encontrado"

- Verifica que el `.env` existe en la carpeta del proyecto
- Asegúrate de haber agregado el SSID correctamente
- Reinicia la terminal

### ❌ "Connection failed"

- Tu SSID podría estar expirado
- Obtén un SSID fresco desde tu navegador
- Reinicia el bot

### ❌ "No se reciben alertas en Telegram"

- Verifica que el `TELEGRAM_BOT_TOKEN` sea correcto
- Verifica que el `TELEGRAM_CHAT_ID` sea correcto
- Asegúrate de que el bot esté en el canal

### ❌ "ModuleNotFoundError: pocketoptionapi_async"

```bash
pip install pocketoptionapi-async --force-reinstall
```

---

## 📊 ESTRATEGIA IMPLEMENTADA

### SEÑAL BAJA (PUT):
```
✓ Alligator: Mandíbula > Dientes > Labios (comprimida)
✓ DeMarker: < 35 (sobreventa)
✓ Momentum: Negativo y acelerando hacia abajo
```

### SEÑAL ALZA (CALL):
```
✓ Alligator: Labios > Dientes > Mandíbula (comprimida)
✓ DeMarker: > 65 (sobrecompra)
✓ Momentum: Positivo y acelerando hacia arriba
```

---

## ⏱️ CARACTERÍSTICAS

- ✅ Monitoreo 24/7 en tiempo real
- ✅ Análisis de múltiples activos simultáneamente
- ✅ Alertas instantáneas en Telegram
- ✅ Evita señales duplicadas (60 segundos de espera)
- ✅ Reconexión automática
- ✅ Soporta tanto modo Demo como Real

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Configura tu `.env` con SSID, Token y Chat ID
2. ✅ Instala dependencias: `pip install -r requirements.txt`
3. ✅ Ejecuta: `python bot_main.py`
4. ✅ Recibe alertas en Telegram cuando hay señales

---

## 📞 SOPORTE

Si tienes problemas:

1. Revisa que el `.env` esté bien configurado
2. Asegúrate de tener python 3.8+
3. Reinstala las dependencias
4. Obtén un SSID nuevo si pasó mucho tiempo

---

**¡Listo para tradear! 🚀**
# 🤖 RADAR OTC - Bot de Trading Automatizado

Bot asincrónico para trading OTC en Pocket Option con estrategia **Williams Alligator + DeMarker + Momentum**. Genera señales automáticas y envía alertas a Telegram en tiempo real.

---

## ✨ Características

✅ **Análisis en Tiempo Real**
- Williams Alligator (Mandíbula, Dientes, Labios)
- DeMarker (Período 15)
- Momentum (Período 15)

✅ **Automatización Completa**
- Monitoreo 24/7 de múltiples activos
- Generación automática de señales
- Alertas instantáneas en Telegram

✅ **Conexión Pocket Option**
- WebSocket asincrónico
- Reconexión automática
- Soporte para modo Demo y Real

✅ **Gestión Inteligente**
- Evita señales duplicadas (60s de espera)
- Buffers de velas optimizados
- Manejo robusto de errores

---

## 📋 Requisitos

- **Python 3.8+**
- **Pip** (gestor de paquetes Python)
- **Cuenta Pocket Option** (activa)
- **Bot de Telegram** (token y chat ID)
- **Conexión a Internet** (estable)

---

## 🚀 Instalación Rápida

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/Xanderewa/radar-otc-pocket-option.git
cd radar-otc-pocket-option
```

### 2️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar Variables de Entorno

```bash
cp .env.example .env
# Edita .env con tus datos
```

### 4️⃣ Ejecutar el Bot

```bash
python bot_main.py
```

---

## 🔑 Obtener Credenciales

### 📱 TELEGRAM BOT TOKEN
- Busca **@BotFather** en Telegram
- Envía `/newbot` y sigue instrucciones
- Copia el token generado

### 💬 TELEGRAM CHAT ID
- Crea un canal privado en Telegram
- Obtén el ID (con formato: -1003915863677)

### 🔐 POCKET OPTION SSID
1. Abre https://pocketoption.com
2. Inicia sesión
3. Presiona F12 → Network → Filtra WS
4. Busca mensaje: `42["auth",`
5. Copia TODO el mensaje

📖 **Instrucciones detalladas en `SETUP_GUIDE.md`**

---

## 📊 Estrategia

### SEÑAL ALZA (CALL)
- Alligator: Labios > Dientes > Mandíbula
- DeMarker > 65 (sobrecompra)
- Momentum positivo

### SEÑAL BAJA (PUT)
- Alligator: Mandíbula > Dientes > Labios
- DeMarker < 35 (sobreventa)
- Momentum negativo

---

## 🎮 Uso

```bash
python bot_main.py
```

El bot se conectará a Pocket Option y comenzará a monitorear. Recibirás alertas en Telegram cuando se generen señales.

---

## 🛠️ Solución de Problemas

### POCKET_OPTION_SSID no encontrado
- Verifica que `.env` existe
- Obtén un SSID nuevo desde tu navegador

### Connection failed
- Tu SSID podría estar expirado
- Obtén uno nuevo

### No se reciben alertas
- Verifica TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID
- Asegúrate que el bot esté en el canal

---

## 📁 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `bot_main.py` | Bot principal asincrónico |
| `indicators_v2.py` | Cálculo de indicadores |
| `requirements.txt` | Dependencias de Python |
| `.env` | Variables de configuración |
| `SETUP_GUIDE.md` | Guía de configuración detallada |

---

## 📱 Uso en Celular (Termux - Android)

```bash
# Instala Python
pkg install python3 git

# Clona el repo
git clone https://github.com/Xanderewa/radar-otc-pocket-option.git
cd radar-otc-pocket-option

# Instala dependencias
pip install -r requirements.txt

# Configura .env y ejecuta
python bot_main.py
```

---

## 🚀 Roadmap

- [ ] Interfaz web
- [ ] Histórico de señales
- [ ] Análisis de rentabilidad
- [ ] Notificaciones Discord
- [ ] Trading automático

---

## 🔐 Seguridad

⚠️ **Nunca** compartas tu `.env` públicamente  
⚠️ **Nunca** subas `.env` a GitHub  
⚠️ **Siempre** usa `.gitignore`

---

## 📝 Licencia

MIT License

---

## 🤝 Contribuciones

¿Mejoras o bugs? ¡Abre un Pull Request!

---

**¡Listo para tradear! 🚀**

**Última actualización:** 11/07/2026 | **Versión:** 1.0.0
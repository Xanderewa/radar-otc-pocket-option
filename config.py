import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Pocket Option
POCKET_OPTION_EMAIL = os.getenv("POCKET_OPTION_EMAIL")
POCKET_OPTION_PASSWORD = os.getenv("POCKET_OPTION_PASSWORD")

# Activos a monitorear
ASSETS_TO_MONITOR = [
    "AUDUSD",  # AUD/USD
    "USDTHB",  # USD/THB
    "SOLANA",  # Solana
    "AAPL",    # Apple
    "BABA",    # Alibaba
]

# Timeframe
TIMEFRAME = 15  # 15 segundos

# Timezone
TIMEZONE = "America/Bogota"
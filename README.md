# Fiyat Takip Botu

Telegram üzerinden Bitcoin fiyatını takip eden basit bir bot.

## Özellikler
- `/start` ile kullanım bilgisi gösterir
- `/fiyat` ile güncel Bitcoin fiyatını getirir
- `/setalarm` ile düzenli kontrol başlatır
- `/stopalarm` ile alarmı kapatır
- CoinGecko API kullanır

## Kullanılan Teknolojiler
- Python
- python-telegram-bot
- requests

## Kurulum
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ortam değişkeni
`.env.example` dosyasını örnek alarak token bilgisini ortam değişkeni olarak tanımlayın.

Windows PowerShell için geçici kullanım:
```powershell
$env:TELEGRAM_BOT_TOKEN="BURAYA_TOKEN"
python bot.py
```

## Komutlar
- `/start`
- `/fiyat`
- `/setalarm`
- `/stopalarm`

## Not
Gerçek bot tokenını kodun içine yazmayın. GitHub'a yüklemeden önce BotFather üzerinden tokenı yenileyin.

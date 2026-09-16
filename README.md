# Atrangii Telegram Bot + Mini App — Railway

This version is designed for ONE Railway service running both the Telegram bot and Mini App web server, with one persistent SQLite volume.

## Railway deployment

1. Put this project in a GitHub repository, or deploy with Railway CLI.
2. Railway -> New Project -> Deploy from GitHub Repo.
3. Select the repository. Railway detects the Dockerfile and builds it.
4. In the service Variables tab, add:
   - BOT_TOKEN = 8656736053:AAET1pZpa9lbfNGe_SFFbiSAw-L1riUUZ54
   - APP_URL = the HTTPS Railway domain you will generate
   - MAIN_CHANNEL_ID = 1563070778
   - BACKUP_CHANNEL_URL = https://t.me/Atrangii_re_new
   - ADMIN_IDS = your Telegram numeric ID (optional)
   - DATABASE_PATH = /app/data/bot.db
5. In Settings -> Networking, generate a public domain.
6. Put that generated https://... URL into APP_URL and redeploy.
7. Add @Atrangii_re_bot as an administrator in the main channel.
8. In @BotFather, configure the bot's Main Mini App / Web App URL as the same Railway HTTPS URL.
9. In Railway Volumes, add a volume mounted at /app/data.
10. Open https://YOUR-RAILWAY-DOMAIN/ to check the Mini App.

## Important

- Never publish your BotFather token.
- The bot must be an administrator in the main channel to receive channel-post updates.
- The private invite link is not enough for the bot to read channel posts.
- This project captures posts arriving after the bot is installed; it does not import arbitrary old channel history.
- For high traffic, consider Postgres + object storage/CDN and server-side Telegram Mini App initData validation.

## Local run

```bash
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

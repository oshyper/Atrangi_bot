# Atrangii Telegram Bot + Mini App

## Railway setup
Set these Variables in Railway (do not commit secrets):

- `BOT_TOKEN` = your BotFather token
- `APP_URL` = your Railway public HTTPS URL
- `MAIN_CHANNEL_ID` = your Telegram main channel ID
- `BACKUP_CHANNEL_URL` = `https://t.me/Atrangii_re_new`
- `ADMIN_IDS` = optional comma-separated Telegram user IDs
- `DATABASE_PATH` = `/data/bot.db`

Attach a Railway Volume mounted at `/data` if you want SQLite data to persist across redeploys.

## Important
The previous repository exposed a BotFather token and incorrectly used the token/channel values as environment-variable names. This version fixes the configuration. Revoke/regenerate any token that was previously exposed publicly.

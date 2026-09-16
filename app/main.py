import asyncio
import uvicorn
from app.bot import main as bot_main

async def web_main():
    config = uvicorn.Config("app.web:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(bot_main(), web_main())

if __name__ == "__main__":
    asyncio.run(main())

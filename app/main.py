import asyncio, os
import uvicorn
from app.bot import main as bot_main
async def web_main():
    config=uvicorn.Config('app.web:app',host='0.0.0.0',port=int(os.getenv('PORT','8000')),log_level='info')
    await uvicorn.Server(config).serve()
async def main(): await asyncio.gather(bot_main(),web_main())
if __name__=='__main__': asyncio.run(main())

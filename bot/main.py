import asyncio
import logging
from typing import List

from discord.ext import commands

from bot.settings import DISCORD_TOKEN, RMQ_USER, RMQ_PASS

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
log = logging.getLogger(__name__)

#############

from fastapi import FastAPI
from uvicorn import Config, Server

from bot.routers import info, account, do

app = FastAPI()

app.include_router(
    info.router,
    prefix='/info',
    tags=['info']
)
app.include_router(
    account.router,
    prefix='/account',
    tags=['account']
)
app.include_router(
    do.router,
    prefix='/do',
    tags=['do']
)



config = Config(
    app,
    host='127.0.0.1',
    port=5000
)

server = Server(config)

#############


class Symbot(commands.Bot):
    def __init__(self, cogs: List[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if cogs is None:
            cogs = []
        self.load_cogs = cogs

    async def start(self):
        for cog in self.load_cogs:
            self.load_extension(cog)

        self.loop.create_task(server.serve())

        await super().start(DISCORD_TOKEN)

    async def on_ready(self):
        log.info(f'We have logged in as {self.user}')


bot = Symbot(cogs=[], command_prefix='`')

app.state.bot = bot


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(bot.start())

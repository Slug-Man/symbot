import discord
from discord.ext import commands
from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request


def get_bot(request: Request):
    return request.app.state.bot


def get_guild(guild_id: int, bot: commands.Bot = Depends(get_bot)):
    return bot.get_guild(guild_id)


def get_channel(channel_id: int, bot: commands.Bot = Depends(get_bot)):
    return bot.get_channel(channel_id)


def get_text_channel(text_channel: discord.TextChannel = Depends(get_channel)):
    if text_channel is None:
        raise HTTPException(status_code=404, detail='Text channel not found')
    if not isinstance(text_channel, discord.TextChannel):
        raise HTTPException(status_code=422, detail='Channel is not a Text channel')

    return text_channel


async def fetch_message(message_id: int,
                        channel: discord.TextChannel = Depends(get_text_channel),
                        bot: commands.Bot = Depends(get_bot)):
    message = discord.utils.get(bot.cached_messages, id=message_id)

    if message is None:
        message = await channel.fetch_message(message_id)
        print('dang nigga had to fetch')

    return message



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/account/login')


def get_login(token: str = Depends(oauth2_scheme)):
    return token


def is_user_in_guild(guild: discord.Guild = Depends(get_guild), user: str = Depends(get_login)):
    if guild is None:
        raise HTTPException(status_code=404, detail='Guild not found')
    if guild.get_member(int(user)) is None:
        raise HTTPException(status_code=404, detail='User not found in guild')

import discord
from discord.ext import commands
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import Response
from pydantic import BaseModel

from .utils import get_bot, get_guild, get_login, is_user_in_guild, get_text_channel, fetch_message


from pydantic import BaseModel


class Message(BaseModel):
    content: str


router = APIRouter()


@router.put('/say')
async def say(channel: discord.TextChannel = Depends(get_text_channel)):
    await channel.send('test')


@router.put('/edit')
async def edit(new_message: Message, message: discord.Message = Depends(fetch_message)):
    try:
        await message.edit(content=new_message.content)
    except discord.errors.Forbidden as e:
        raise HTTPException(status_code=403, detail=e.text)

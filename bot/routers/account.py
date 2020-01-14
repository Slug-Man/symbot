import discord
from discord.ext import commands
from fastapi import APIRouter, Cookie, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import Response

from .utils import get_bot, get_guild, get_login, is_user_in_guild

router = APIRouter()


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username, 'token_type': 'bearer'}


@router.get('/me')
async def me(user: str = Depends(get_login)):
    return user


@router.get('/inguildcheck', dependencies=[Depends(is_user_in_guild)])
async def in_guild_check(guild: discord.Guild = Depends(get_guild)):
    return True

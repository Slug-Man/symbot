import discord
from discord.ext import commands
from fastapi import APIRouter, Depends

from .utils import get_bot, get_guild

router = APIRouter()


@router.get('/guilds')
async def get_guilds(bot: commands.Bot = Depends(get_bot)):
    guilds = {}
    for guild in bot.guilds:  # type: discord.Guild
        guilds[guild.id] = {'name': guild.name, 'owner': guild.owner_id, 'channel count': len(guild.channels)}

    return guilds

@router.get('/guilds/{guild_id}/channels')
async def get_guild_channels(guild: discord.Guild = Depends(get_guild)):
    channels = {'text channels': {}, 'category channels': {}, 'voice channels': {}}
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            channels['text channels'][channel.id] = {'name': channel.name,
                                                     'position': channel.position,
                                                     'nsfw': channel.is_nsfw(),
                                                     'category': channel.category_id}

        elif isinstance(channel, discord.CategoryChannel):
            channels['category channels'][channel.id] = {'name':channel.name,
                                                         'position': channel.position}

        elif isinstance(channel, discord.VoiceChannel):
            channels['voice channels'][channel.id] = {'name': channel.name,
                                                      'position': channel.position,
                                                      'user limit': channel.user_limit,
                                                      'category': channel.category_id}

    return channels

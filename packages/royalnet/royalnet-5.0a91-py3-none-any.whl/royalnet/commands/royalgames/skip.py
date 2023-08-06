import typing
import pickle
import discord
from ..command import Command
from ..commandinterface import CommandInterface
from ..commandargs import CommandArgs
from ..commanddata import CommandData
from ...utils import NetworkHandler, asyncify
from ...network import Request, ResponseSuccess
from ...error import *
from ...audio import YtdlDiscord
if typing.TYPE_CHECKING:
    from ...bots import DiscordBot


class SkipNH(NetworkHandler):
    message_type = "music_skip"

    @classmethod
    async def discord(cls, bot: "DiscordBot", data: dict):
        # Find the matching guild
        if data["guild_name"]:
            guild = bot.client.find_guild_by_name(data["guild_name"])
        else:
            if len(bot.music_data) == 0:
                raise NoneFoundError("No voice clients active")
            if len(bot.music_data) > 1:
                raise TooManyFoundError("Multiple guilds found")
            guild = list(bot.music_data)[0]
        # Set the currently playing source as ended
        voice_client: discord.VoiceClient = bot.client.find_voice_client_by_guild(guild)
        if not (voice_client.is_playing() or voice_client.is_paused()):
            raise NoneFoundError("Nothing to skip")
        # noinspection PyProtectedMember
        voice_client._player.stop()
        return ResponseSuccess()


class SkipCommand(Command):
    name: str = "skip"

    description: str = "Salta la canzone attualmente in riproduzione in chat vocale."

    syntax: str = "[ [guild] ]"

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        interface.register_net_handler(SkipNH.message_type, SkipNH)

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        guild, = args.match(r"(?:\[(.+)])?")
        await self.interface.net_request(Request(SkipNH.message_type, {"guild_name": guild}), "discord")
        await data.reply(f"⏩ Richiesto lo skip della canzone attuale.")

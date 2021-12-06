import json
import typing
from itertools import cycle
from dotenv import dotenv_values

import discord
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.errors import NotFound
from discord.ext import commands

from ui import TagDropdown, TagView, ButtonAcceptView, BasicInterfaceView, ExtraInterfaceView, RulesAcceptView
from tags import TAGS_DEGREE, TAGS_SPECIAL, TAGS_YEAR

# Possibili stati divertenti del bot
STATUSES = cycle([
    'Risolvendo le dipendenze circolari della segreteria 🔁',
    'Facendo colazione con caffè e brioche al bar 💞',
    'Costruendo sedie per i tavoli nei corridoi',
    'Mostrando il Green-Pass alle guardie 👮',
    'Pranzando nel tetto di CV3 mentre il Giaco spiega',
    'Cercando le macchinette del caffè nei sotterranei',
    'Facendo l\'esame di Fondamenti dell\'Informatica',
    'Simulando una FSM di Mealy con SIS',
    'Discutendo di matrici e di ponti con Gregorio',
    'Protestando per la mensa di Borgo Roma',
    'Chiudendo i cancelli a quelli di medicina',
    'Annaffiando le piante della serra mentre fuori piove 🪴 ',
    'Contattando Algida per riavere la macchinetta dei gelati 🍦',
    'Attendendo in coda per riempire la borraccia a CV1',
    'Organizzando uno spritz 🍸 alla Bottega  ',
    'Imprecando contro la sbarra del parcheggio',
    'Indagando sulla roulotte nel parcheggio esterno',
    'Aspettando il 21 in stazione alle 7.15 🧊🚌 ',
    'Ammassando un esercito per conquistare gli uffici del CLA ⚔️',
    'Rubando sedie dal laboratorio Delta',
    'Rincorrendo la 🐑 fuori da CV2.'
])

#
# GuildChannel = Union[TextChannel, NewsChannel, VoiceChannel, CategoryChannel, StoreChannel, StageChannel, ThreadChannel]
#

CHANNEL_TYPE = {
    "GUILD_TEXT": 0,
    "DM": 1,
    "GUILD_VOICE": 2,
    "GROUP_DM": 3,
    "GUILD_CATEGORY": 4,
    "GUILD_NEWS": 5,
    "GUILD_STORE": 6,
    "GUILD_NEWS_THREAD": 7,
    "GUILD_PUBLIC_THREAD": 8,
    "GUILD_PRIVATE_THREAD": 9,
    "GUILD_STAGE_VOICE": 10,
}

CHANNEL_PERMISSION = {
    "CREATE_INSTANT_INVITE": 0x0000000001,
    "KICK_MEMBERS": 0x0000000002,
    "BAN_MEMBERS": 0x0000000004,
    "ADMINISTRATOR": 0x0000000008,
    "MANAGE_CHANNELS": 0x0000000010,
    "MANAGE_GUILD": 0x0000000020,
    "ADD_REACTIONS": 0x0000000040,
    "VIEW_AUDIT_LOG": 0x0000000080,
    "PRIORITY_SPEAKER": 0x0000000100,
    "STREAM": 0x0000000200,
    "VIEW_CHANNEL": 0x0000000400,
    "SEND_MESSAGES": 0x0000000800,
    "SEND_TTS_MESSAGES": 0x0000001000,
    "MANAGE_MESSAGES": 0x0000002000,
    "EMBED_LINKS": 0x0000004000,
    "ATTACH_FILES": 0x0000008000,
    "READ_MESSAGE_HISTORY": 0x0000010000,
    "MENTION_EVERYONE": 0x0000020000,
    "USE_EXTERNAL_EMOJIS": 0x0000040000,
    "VIEW_GUILD_INSIGHTS": 0x0000080000,
    "CONNECT": 0x0000100000,
    "SPEAK": 0x0000200000,
    "MUTE_MEMBERS": 0x0000400000,
    "DEAFEN_MEMBERS": 0x0000800000,
    "MOVE_MEMBERS": 0x0001000000,
    "USE_VAD": 0x0002000000,
    "CHANGE_NICKNAME": 0x0004000000,
    "MANAGE_NICKNAMES": 0x0008000000,
    "MANAGE_ROLES": 0x0010000000,
    "MANAGE_WEBHOOKS": 0x0020000000,
    "MANAGE_EMOJIS_AND_STICKERS": 0x0040000000,
    "USE_APPLICATION_COMMANDS": 0x0080000000,
    "REQUEST_TO_SPEAK": 0x0100000000,
    "MANAGE_EVENTS": 0x0200000000,
    "MANAGE_THREADS": 0x0400000000,
    "CREATE_PUBLIC_THREADS": 0x0800000000,
    "CREATE_PRIVATE_THREADS": 0x1000000000,
    "USE_EXTERNAL_STICKERS": 0x2000000000,
    "SEND_MESSAGES_IN_THREADS": 0x4000000000,
    "START_EMBEDDED_ACTIVITIES": 0x8000000000
}


class BotUniVR(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        self.persistent_views_added = False

    async def on_ready(self):
        print('Motori a curvatura: ingaggio!')

        # Carica views persistente
        if not self.persistent_views_added:
            self.add_view(BasicInterfaceView())
            self.add_view(ExtraInterfaceView())
            self.persistent_views_added = True

        # Cambia stato del bot ogni 10 minuti
        self.update_status.start()

    @tasks.loop(minutes=10)
    async def update_status(self):
        new_status = str(next(STATUSES))
        print(f'Cambio stato bot a "{new_status}"')
        await self.change_presence(activity=discord.Game(new_status))


class MyBot:

    def __init__(self):
        self.config = {}
        self.bot = BotUniVR()

    def load_configuration(self):
        with open('configuration.json', 'r') as f:
            print('Caricamento configurazione...')
            self.config = json.load(f)
        return self.config

    def save_configuration(self, json_data=None):
        if json_data is None: json_data = self.config
        with open('configuration.json', 'w') as f:
            print('Salvataggio nuova configurazione...')
            json.dump(json_data, f, indent=4)

    async def send_embed(self, ctx, view, title, description, url):
        embed_degrees = Embed(title=title, description=description)
        embed_degrees.set_thumbnail(url=url)
        await ctx.send(view=view, embed=embed_degrees)

    async def send(self, ctx, msg):
        await ctx.send(content=msg)

    async def get_roles(self, ctx):
        roles = await ctx.guild.roles()
        return roles

    def hex2int(self,hex_color):
        hex_vals = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                "8": 8, "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
        length = len(hex_color) - 1
        hex_color = hex_color.upper()
        int_color = 0

        for digit in hex_color:
            int_color += hex_vals[digit] * 16 ** length
            length -= 1
        return int_color

    async def create_role(self, ctx, role_name, role_color=None) -> discord.Role:
        try:
            # Crea nuovo ruolo associato alla categoria
            print(f'Creazione nuovo ruolo per la categoria "{role_name}"...')
            color = self.hex2int(role_color)
            color_obj = discord.Color(color)

            role = await ctx.guild.create_role(name=role_name, color=color_obj)
            return role

        except discord.HTTPException as e:
            print('Errore creazione nuovo ruolo: ' + e.text)
        return None

    async def fetch_role(self, ctx, role_id) -> discord.Role:
        roles = list(filter(lambda r: r.id == role_id, ctx.guild.roles))
        if len(roles) > 0: return roles[0]
        return None

    async def find_role(self, ctx, name) -> discord.Role:
        roles = list(filter(lambda r: r.name == name, ctx.guild.roles))
        if len(roles) > 0: return roles[0]
        return None

    async def fetch_channel(self, ctx, channel_id) -> discord.abc.GuildChannel:
        try:
            channel = await ctx.guild.fetch_channel(channel_id)
            return channel
        except discord.HTTPException as e:
            print('fetch_channel: ' + e.text)
            return None

    async def find_channel(self, ctx, name, kind=None) -> discord.abc.GuildChannel:
        channels = ctx.guild.channels # List[discord.GuildChannel]
        if kind is not None: channels = list(filter(lambda c: c.type.value == CHANNEL_TYPE[kind], channels))
        channels = list(filter(lambda c: c.name == name, channels))
        if len(channels) > 0: return channels[0]
        return None

    async def create_category(self, ctx, category_name, overwrites=None):
        if overwrites is None: overwrites = {}
        # Permetti al solo nuovo ruolo di visualizzare la categoria
        print(f'Creazione nuova categoria "{category_name}"...')
        try:
            category = await ctx.guild.create_category_channel(category_name, overwrites=overwrites)
            return category
        except discord.HTTPException as e:
            print('Errore creazione nuova categoria:' + e.text)
            return None

    async def create_channel(self, ctx, channel_name, category=None):
        try:
            print(f'Creazione nuovo canale testuale "{channel_name}" per la categoria {channel_name}...')
            base = ctx.guild if category is None else category
            channel = await base.create_text_channel(name=channel_name)
            return channel

        except discord.HTTPException as e:
            print('Errore creazione nuovo canale testuale:' + e.text)
            return None

    async def assign_channel(self, ctx, channel_id, category_id):
        try:
            channel = ctx.guild.fetch_channel(channel_id)
            category = ctx.guild.fetch_channel(category_id)
            print(f'Sposto il canale "{channel.name}" nella la categoria {category.name}...')
            await channel.edit(category=category)
            return True

        except discord.HTTPException as e:
            print('Errore spostamento  nuovo canale testuale:' + e.text)
            return False

    async def reset_channel_permissions(self, ctx, channel):
        await channel.edit(overwrites={})

    async def permission_channel(self, ctx, channel, role, permission_name, permission_value) -> bool:
        # TODO:
        try:
            perms = {permission_name: permission_value}
            perms_overwrite = discord.PermissionOverwrite(**perms)
            overwrites = channel.overwrites
            overwrites[role] = perms_overwrite
            await channel.edit(overwrites=overwrites)
            return True
        except discord.HTTPException as e:
            print('Errore nella configurazione dei permessi' + e.text)
            return False

    async def private_channel(self, ctx, channel, role, reset=False) -> bool:
        try:
            role_everyone = await self.find_role(ctx, "@everyone")
            view_yes = discord.PermissionOverwrite(view_channel=True)
            view_no = discord.PermissionOverwrite(view_channel=False)
            overwrites = {} if reset else channel.overwrites
            overwrites[role] = view_yes
            overwrites[role_everyone] = view_no
            await channel.edit(overwrites=overwrites)
            return True
        except discord.HTTPException as e:
            print('Errore nella configurazione dei permessi' + e.text)
            return False

    async def delete_category(self, ctx, category_id: int, force: bool = False):
        """
        Elimina categoria e tutti i canali contenuti
        """
        try:
            print(f'Ottenimento categoria con ID {category_id}...')
            category = await ctx.guild.fetch_channel(category_id)
            for channel in category.text_channels:
                if not force and channel.last_message_id is not None: continue
                try:
                    print(f'Rimozione canale testuale {str(channel)}...')
                    await channel.delete()

                except discord.HTTPException as e:
                    print('Errore rimozione canale testuale: ' + e.text)
                    continue
            try:
                print('Rimozione categoria...')
                await category.delete()

            except discord.HTTPException as e:
                print('Errore rimozione categoria: ' + e.text)


        except discord.HTTPException as e:
            print('Errore ottenimento  categoria: ' + e.text)

        except discord.NotFound as e:
            print('Categoria non trovata: ' + e.text)

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import PCMVolumeTransformer

class MusicButton(discord.ui.Button):
    def __init__(self, text, buttonStyle):
        super().__init__(label=text, style=buttonStyle)

    async def callback(self, interaction: discord.Interaction):
        voice_state = interaction.user.voice
        if self.label == "Connect":
            if voice_state:
                voice_channel = voice_state.channel
                if not interaction.guild.voice_client:  # Überprüfung, ob bereits verbunden
                    voice_client = await voice_channel.connect()
                    print(f"Bot connected to {voice_channel}")
            else:
                await interaction.response.send_message("Du befindest dich in keinem Sprachkanal.", ephemeral=True)
        elif self.label == "Disconnect":
            voice_channel = interaction.guild.voice_client.channel if interaction.guild.voice_client else None
            if voice_channel:
                await interaction.guild.voice_client.disconnect()
                print(f"Bot disconnected from Channel {voice_channel}")
            else:
                await interaction.response.send_message("Der Bot ist nicht mit einem Sprachkanal verbunden.", ephemeral=True)
        elif self.label == "IloveRadio":
            if voice_state:
                voice_channel = voice_state.channel
                if not interaction.guild.voice_client:  # Überprüfung, ob bereits verbunden
                    voice_client = await voice_channel.connect()
                    await play_internet_radio(voice_client, "IloveRadio")  # iloveradio abspielen
                else:
                    await interaction.response.send_message("Der Bot ist bereits mit einem Sprachkanal verbunden.", ephemeral=True)
            else:
                await interaction.response.send_message("Du befindest dich in keinem Sprachkanal.", ephemeral=True)
        elif self.label == "Skyrock":
            if voice_state:
                voice_channel = voice_state.channel
                if not interaction.guild.voice_client:  # Überprüfung, ob bereits verbunden
                    voice_client = await voice_channel.connect()
                    await play_internet_radio(voice_client, "Skyrock")  # skyrock abspielen
                else:
                    await interaction.response.send_message("Der Bot ist bereits mit einem Sprachkanal verbunden.", ephemeral=True)
            else:
                await interaction.response.send_message("Du befindest dich in keinem Sprachkanal.", ephemeral=True)

async def play_internet_radio(voice_client, radio_station):
    if radio_station == "IloveRadio":
        radio_url = "https://ilm-stream13.radiohost.de/ilm_iloveradio_mp3-192?"
    elif radio_station == "Skyrock":
        radio_url = "http://icecast.skyrock.net/s/natio_mp3_128k?type=.mp3"
    else:
        return  # Unerkannte Radiostation

    # Stream vom Internetradio abspielen
    voice_client.play(FFmpegPCMAudio(radio_url))
    voice_client.source = PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = 0.5  # Lautstärke einstellen

class MusicView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MusicButton("Connect", discord.ButtonStyle.green))
        self.add_item(MusicButton("IloveRadio", discord.ButtonStyle.blurple))
        self.add_item(MusicButton("Skyrock", discord.ButtonStyle.blurple))
        self.add_item(MusicButton("Disconnect", discord.ButtonStyle.red))

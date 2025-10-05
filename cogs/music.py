import discord
import pytubefix

if not discord.opus.is_loaded():
	discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib')

class Music(discord.Cog):
	def __init__(self, bot):
		self.bot: discord.Bot = bot
		self.queue: list[pytubefix.YouTube] = []

	async def play_song(self, ctx):
		if len(self.queue) > 0:
			stream = self.queue[0].streams.filter(only_audio=True).first()
			audio_url = stream.url

			ffmpeg_opts = {
				"options": "-vn",
				"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
			}

			ctx.voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts), after=self.play_song)
			await ctx.send(f"Now playing: **{self.queue[0].title}** by **{self.queue[0].author}**")
			self.queue.pop(0)
		else:
			await ctx.send("The queue is empty.")

	@discord.command(description="Play music via search or direct URL from YouTube.")
	async def play(self, ctx: discord.ApplicationContext, song: str):
		await self.join(ctx)
		print("joined")

		# if song[:4] == "http":
		# 	self.queue.append(pytubefix.YouTube(song))
		# else:
		# 	search = pytubefix.Search(song)
		#
		# 	class SongView(discord.ui.View):
		# 		def __init__(self, author_id):
		# 			super().__init__(timeout=30)
		# 			self.author_id = author_id
		# 			self.choice = None
		#
		# 		async def handle_choice(self, interaction: discord.Interaction, number: int):
		# 			if interaction.user.id != self.author_id:
		# 				return
		# 			self.choice = number
		# 			self.stop()
		#
		# 		@discord.ui.button(label="1")
		# 		async def button_1(self, _button, interaction: discord.Interaction):
		# 			await self.handle_choice(interaction, 0)
		#
		# 		@discord.ui.button(label="2")
		# 		async def button_2(self, _button, interaction: discord.Interaction):
		# 			await self.handle_choice(interaction, 1)
		#
		# 		@discord.ui.button(label="3")
		# 		async def button_3(self, _button, interaction: discord.Interaction):
		# 			await self.handle_choice(interaction, 2)
		#
		# 		@discord.ui.button(label="4")
		# 		async def button_4(self, _button, interaction: discord.Interaction):
		# 			await self.handle_choice(interaction, 3)
		#
		# 		@discord.ui.button(label="5")
		# 		async def button_5(self, _button, interaction: discord.Interaction):
		# 			await self.handle_choice(interaction, 4)
		#
		# 	view = SongView(ctx.author.id)
		#
		# 	await ctx.send_followup(f"1. {search.videos[0].title} - {search.videos[0].author}\n2. {search.videos[1].title} - {search.videos[1].author}\n3. {search.videos[2].title} - {search.videos[2].author}\n4. {search.videos[3].title} - {search.videos[3].author}\n5. {search.videos[4].title} - {search.videos[4].author}", view=view)
		#
		# 	await view.wait()
		# 	if view.choice is not None:
		# 		self.queue.append(search.videos[view.choice])
		#
		# if not ctx.voice_client.is_playing():
		# 	await self.play_song(ctx)

	@discord.command(description="Display a list of the current songs in the queue.")
	async def list(self, ctx: discord.ApplicationContext):
		response = ""

		for idx, song in enumerate(self.queue):
			response += f"**{idx + 1}**. {song}\n"

		await ctx.respond(response)

	@discord.command(description="Display the currently playing track.")
	async def nowplaying(self, ctx: discord.ApplicationContext):
		pass

	skip_group = discord.SlashCommandGroup("skip", "")

	@skip_group.command(name="first", description="Skip one or more tracks in the beginning of the queue.")
	async def skip_first(self, ctx: discord.ApplicationContext):
		pass

	@skip_group.command(name="number", description="Skip a track at a specific position in the queue.")
	async def skip_number(self, ctx: discord.ApplicationContext):
		pass

	@skip_group.command(name="user", description="Skip tracks added by a user.")
	async def skip_user(self, ctx: discord.ApplicationContext):
		pass

	@skip_group.command(name="range", description="Skip a range of tracks in the queue.")
	async def skip_range(self, ctx: discord.ApplicationContext):
		pass

	voteskip_group = discord.SlashCommandGroup("voteskip", "")

	@voteskip_group.command(name="vote",
							description="Vote to skip the current track. Skips after a simple majority is reached.")
	async def voteskip_vote(self, ctx: discord.ApplicationContext):
		pass

	@voteskip_group.command(name="undo", description="Remove your vote to skip the current track.")
	async def voteskip_undo(self, ctx: discord.ApplicationContext):
		pass

	@voteskip_group.command(name="list", description="Lists the users voting to skip the track.")
	async def voteskip_list(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Stop the player and clear the playlist.")
	async def stop(self, ctx: discord.ApplicationContext):
		pass

	pause_group = discord.SlashCommandGroup("pause", "")

	@pause_group.command(name="on", description="Pause the player.")
	async def pause_on(self, ctx: discord.ApplicationContext):
		pass

	@pause_group.command(name="off", description="Unpause the player.")
	async def pause_off(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Make NOTME join your current audio channel.")
	async def join(self, ctx: discord.ApplicationContext):
		await ctx.defer()

		if not ctx.author.voice or not ctx.author.voice.channel:
			await ctx.respond("You're not in a voice channel!", ephemeral=True)
			return

		voice_channel = ctx.author.voice.channel

		if ctx.voice_client:
			await ctx.voice_client.move_to(voice_channel)
			await ctx.respond(f"Moved to {voice_channel.name}")
		else:
			await voice_channel.connect()
			await ctx.respond(f"Joined {voice_channel.name}")

	@discord.command(description="Make NOTME leave the current audio channel.")
	async def leave(self, ctx: discord.ApplicationContext):
		await ctx.defer()

		if not ctx.author.voice or not ctx.author.voice.channel:
			await ctx.respond("You're not in a voice channel!", ephemeral=True)
			return

		voice_channel = ctx.author.voice.channel

		if ctx.voice_client:
			await ctx.voice_client.disconnect()
			await ctx.followup.send(f"Left {voice_channel.name}")
		else:
			await ctx.followup.send(f"I'm not in a voice channel!", ephemeral=True)

	@discord.command(description="Reset the player and clear the playlist.")
	async def destroy(self, ctx: discord.ApplicationContext):
		pass

	repeat_group = discord.SlashCommandGroup("repeat", "")

	@repeat_group.command(name="all", description="Repeat all tracks.")
	async def repeat_all(self, ctx: discord.ApplicationContext):
		pass

	@repeat_group.command(name="single", description="Repeat the same track.")
	async def repeat_single(self, ctx: discord.ApplicationContext):
		pass

	@repeat_group.command(name="off", description="Play the queue normally.")
	async def repeat_off(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="on to activate shuffle mode and off to deactivate shuffle mode.")
	async def shuffle(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Reshuffle the queue.")
	async def reshuffle(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Forward the track by the given amount of time.")
	async def forward(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Rewind the track by the given amount of time.")
	async def rewind(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Set the position of the track to the given time.")
	async def seek(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Restart the currently playing track.")
	async def restart(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Show history of recently played tracks.")
	async def history(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Export the current queue to Wastebin.")
	async def export(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Change the position of a track in the queue.")
	async def reposition(self, ctx: discord.ApplicationContext):
		pass

	@discord.command(description="Change the volume of the player.")
	async def volume(self, ctx: discord.ApplicationContext):
		pass

	playlist_group = discord.SlashCommandGroup("playlist", "")

	@playlist_group.command(name="play", description="Play a saved playlist.")
	async def playlist_play(self, ctx: discord.ApplicationContext):
		pass

	@playlist_group.command(name="list", description="Display the server's saved playlists.")
	async def playlist_list(self, ctx: discord.ApplicationContext):
		pass

	@playlist_group.command(name="list-tracks", description="List the tracks from the specified playlist.")
	async def playlist_list_tracks(self, ctx: discord.ApplicationContext):
		pass

	playlist_manage_group = discord.SlashCommandGroup("playlist-manage", "")

	@playlist_manage_group.command(name="create", description="Create a new playlist.")
	async def playlist_manage_create(self, ctx: discord.ApplicationContext):
		pass

	@playlist_manage_group.command(name="rename", description="Rename the specified playlist.")
	async def playlist_manage_rename(self, ctx: discord.ApplicationContext):
		pass

	@playlist_manage_group.command(name="delete", description="Delete the specified playlist.")
	async def playlist_manage_delete(self, ctx: discord.ApplicationContext):
		pass

	@playlist_manage_group.command(name="add-track", description="Add the specified track to specified playlist.")
	async def playlist_manage_add_track(self, ctx: discord.ApplicationContext):
		pass

	@playlist_manage_group.command(name="remove-track",
								   description="Remove the specified track from specified playlist.")
	async def playlist_manage_remove_track(self, ctx: discord.ApplicationContext):
		pass

	@playlist_manage_group.command(name="reposition-track",
								   description="Reposition the specified track in the specified playlist.")
	async def playlist_manage_reposition_track(self, ctx: discord.ApplicationContext):
		pass

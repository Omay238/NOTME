import discord
import asyncio
import random
from math import ceil


class Money(discord.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.moneys = {}

	async def cog_check(self, ctx):
		if ctx.author.id not in self.moneys:
			self.moneys[ctx.author.id] = 100

		return True

	money_group = discord.SlashCommandGroup("money", "Moneys commands.")

	@money_group.command(description="Check your moneys.")
	async def balance(self, ctx):
		await ctx.respond(f"You've got {self.moneys[ctx.author.id]} moneys", ephemeral=True)

	@money_group.command(description="Give someone your moneys.")
	async def give(self, ctx, member: discord.Member, amount: int):
		if member.id not in self.moneys:
			self.moneys[member.id] = 100

		if amount < 0:
			await ctx.respond("You can't give someone negative moneys!", ephemeral=True)
		elif amount > self.moneys[ctx.author.id]:
			await ctx.respond("You haven't got the moneys for that!", ephemeral=True)
		else:
			self.moneys[ctx.author.id] -= amount
			self.moneys[member.id] += amount
			await ctx.respond(
				f"You sent {amount} moneys to {member.mention}.\nYou now have {self.moneys[ctx.author.id]} moneys.",
				ephemeral=True)

	@money_group.command(description="Set somebodies moneys.", permissions=discord.Permissions.view_audit_log)
	async def set(self, ctx, member: discord.Member, amount: int):
		self.moneys[member.id] = amount
		await ctx.respond(f"{member.mention} now has {amount} moneys.", ephemeral=True)

	gambling_group = discord.SlashCommandGroup("gamble", "Let's go gambling!!!")

	@gambling_group.command(description="Slots machine.")
	async def slots(self, ctx: discord.ApplicationContext, bet: int):
		if bet > self.moneys[ctx.author.id]:
			await ctx.respond("You haven't got the moneys for that!", ephemeral=True)
			return

		self.moneys[ctx.author.id] -= bet

		emojis = {"🍒": {3: 5, 4: 25, 5: 100}, "🍉": {3: 8, 4: 40, 5: 120}, "🍋": {3: 8, 4: 40, 5: 120},
			"🍎": {3: 10, 4: 50, 5: 150}, "🍇": {3: 12, 4: 60, 5: 180}, "❤️": {3: 15, 4: 75, 5: 250},
			"🔔": {3: 20, 4: 100, 5: 300}, "⭐️": {3: 25, 4: 125, 5: 500}, "7️⃣": {3: 50, 4: 250, 5: 1000}}
		wild = "⭐️"
		paylines = [[0, 3, 6, 9, 12], [0, 3, 6, 9, 13], [0, 3, 6, 10, 12], [0, 3, 6, 10, 13], [0, 3, 6, 10, 14],
					[0, 3, 7, 9, 12], [0, 3, 7, 9, 13], [0, 3, 7, 10, 12], [0, 3, 7, 10, 13], [0, 3, 7, 10, 14],
					[0, 3, 7, 11, 13], [0, 3, 7, 11, 14], [0, 4, 6, 9, 12], [0, 4, 6, 9, 13], [0, 4, 6, 10, 12],
					[0, 4, 6, 10, 13], [0, 4, 6, 10, 14], [0, 4, 7, 9, 12], [0, 4, 7, 9, 13], [0, 4, 7, 10, 12],
					[0, 4, 7, 10, 13], [0, 4, 7, 10, 14], [0, 4, 7, 11, 13], [0, 4, 7, 11, 14], [0, 4, 8, 10, 12],
					[0, 4, 8, 10, 13], [0, 4, 8, 10, 14], [0, 4, 8, 11, 13], [0, 4, 8, 11, 14], [1, 3, 6, 9, 12],
					[1, 3, 6, 9, 13], [1, 3, 6, 10, 12], [1, 3, 6, 10, 13], [1, 3, 6, 10, 14], [1, 3, 7, 9, 12],
					[1, 3, 7, 9, 13], [1, 3, 7, 10, 12], [1, 3, 7, 10, 13], [1, 3, 7, 10, 14], [1, 3, 7, 11, 13],
					[1, 3, 7, 11, 14], [1, 4, 6, 9, 12], [1, 4, 6, 9, 13], [1, 4, 6, 10, 12], [1, 4, 6, 10, 13],
					[1, 4, 6, 10, 14], [1, 4, 7, 9, 12], [1, 4, 7, 9, 13], [1, 4, 7, 10, 12], [1, 4, 7, 10, 13],
					[1, 4, 7, 10, 14], [1, 4, 7, 11, 13], [1, 4, 7, 11, 14], [1, 4, 8, 10, 12], [1, 4, 8, 10, 13],
					[1, 4, 8, 10, 14], [1, 4, 8, 11, 13], [1, 4, 8, 11, 14], [1, 5, 7, 9, 12], [1, 5, 7, 9, 13],
					[1, 5, 7, 10, 12], [1, 5, 7, 10, 13], [1, 5, 7, 10, 14], [1, 5, 7, 11, 13], [1, 5, 7, 11, 14],
					[1, 5, 8, 10, 12], [1, 5, 8, 10, 13], [1, 5, 8, 10, 14], [1, 5, 8, 11, 13], [1, 5, 8, 11, 14],
					[2, 4, 6, 9, 12], [2, 4, 6, 9, 13], [2, 4, 6, 10, 12], [2, 4, 6, 10, 13], [2, 4, 6, 10, 14],
					[2, 4, 7, 9, 12], [2, 4, 7, 9, 13], [2, 4, 7, 10, 12], [2, 4, 7, 10, 13], [2, 4, 7, 10, 14],
					[2, 4, 7, 11, 13], [2, 4, 7, 11, 14], [2, 4, 8, 10, 12], [2, 4, 8, 10, 13], [2, 4, 8, 10, 14],
					[2, 4, 8, 11, 13], [2, 4, 8, 11, 14], [2, 5, 7, 9, 12], [2, 5, 7, 9, 13], [2, 5, 7, 10, 12],
					[2, 5, 7, 10, 13], [2, 5, 7, 10, 14], [2, 5, 7, 11, 13], [2, 5, 7, 11, 14], [2, 5, 8, 10, 12],
					[2, 5, 8, 10, 13], [2, 5, 8, 10, 14], [2, 5, 8, 11, 13], [2, 5, 8, 11, 14]]

		def r():
			return random.choices(list(emojis.keys()), weights=[31, 20, 23, 5, 6, 6, 4, 4, 1])[0]

		def render(box):
			return (f"Spinning for {bet} moneys!\n"
					f"`{box[0]}` `{box[3]}` `{box[6]}` `{box[9]}` `{box[12]}`\n"
					f"`{box[1]}` `{box[4]}` `{box[7]}` `{box[10]}` `{box[13]}`\n"
					f"`{box[2]}` `{box[5]}` `{box[8]}` `{box[11]}` `{box[14]}`")

		def calculate_score(box):
			lines = []
			wild_lines = []
			for line in paylines:
				temp = list(box[idx] for idx in line)
				checking_char = temp[0]
				count = 0
				for item in temp:
					if not (item == wild or checking_char == item or checking_char == wild):
						break
					if checking_char == wild and item != wild:
						checking_char = item
					count += 1
				if count > 2 and checking_char != wild:
					lines.append(line[:count])
				elif count > 2 and checking_char == wild:
					wild_lines.append(line[:count])

			wild_counted = {}
			counted = {}
			score = 0

			for line in wild_lines:
				for el in line:
					if len(line) > wild_counted.get(el, 0):
						wild_counted[el] = len(line)

			for line in lines:
				for el in line:
					if len(line) > counted.get(el, 0):
						counted[el] = len(line)

			for idx, val in {**counted, **wild_counted}.items():
				score += emojis[box[idx]][val] * (1 / val)

			return ceil((score / 50) * bet)

		box = [r() for _ in range(15)]

		stopped_cols = [False] * 5
		current_col = 0

		class ButtonView(discord.ui.View):
			@discord.ui.button(label="Lock In")
			async def lockin(self, _button, interaction: discord.Interaction):
				nonlocal stopped_cols
				nonlocal current_col
				if interaction.user.id == ctx.author.id:
					stopped_cols[current_col] = True
					current_col += 1
				await interaction.response.defer()

		interaction = await ctx.respond(render(box), view=ButtonView())
		msg = await interaction.original_response()

		while not all(stopped_cols):
			for col in range(5):
				if not stopped_cols[col]:
					for row in range(3):
						box[row + col * 3] = r()
			await msg.edit(content=render(box))
			await asyncio.sleep(0.3)

		await msg.edit(content=render(box), view=None)
		score = calculate_score(box)

		if score > 0:
			await ctx.send_followup(content=f"Wow, {ctx.author.mention} won {score} moneys after betting {bet}!")
			self.moneys[ctx.author.id] += score

import discord
from discord.ext import commands
import random

TOKEN=""

# Bot object、設定指令開頭
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

games = {}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from myself, prevent loop

    if message.content.startswith('!ping'):
        await message.channel.send('Hey there!')

    await client.process_commands(message)


@client.command(help="Say Hi", brief="Say Hi")
async def hi(ctx):  # extension: 使用者輸入要加入的功能
    await ctx.send('hihi!')

#結束遊戲
@client.command(help="End game", brief="End game")
async def end_game(ctx):
    await ctx.send("The game has ended")
    del games[ctx.channel.id]

# 猜數字
@client.command(help="Start a new guess-the-number game or make a guess", brief="Start a new game or guess a number")
async def guess(ctx, number: int = None):
    global games
    if number is None:
        # Start a new game
        secret_number = random.randint(1, 100)
        games[ctx.channel.id] = {
            'secret_number': secret_number,
            'attempts': 0
        }
        await ctx.send("New game started! Guess a number between 1 and 100.")
    else:
        if ctx.channel.id in games:
            game = games[ctx.channel.id]
            game['attempts'] += 1
            secret_number = game['secret_number']

            if number < secret_number:
                await ctx.send("Too low! Try again.")
            elif number > secret_number:
                await ctx.send("Too high! Try again.")
            else:
                attempts = game['attempts']
                await ctx.send(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
                del games[ctx.channel.id]
        else:
            await ctx.send("Please start a new game using `!guess`.")

# 幾A幾B
@client.command(help="Play a guessing game", brief="Play a game")
async def guess_AB(ctx, attempt: str = None):
    global games
    if attempt is None:
        random_string = ''.join(random.sample('123456789', 4))
        games[ctx.channel.id] = {
            'random_string': random_string,
            'attempts': 0
        }
        await ctx.send("New game started! Guess a four-digit number.")
    else:
        if ctx.channel.id in games:
            game = games[ctx.channel.id]
            game['attempts'] += 1
            random_string = game['random_string']

            a = b = 0
            for i in range(4):
                if attempt[i] == random_string[i]:
                    a += 1
                elif attempt[i] in random_string:
                    b += 1

            await ctx.send(f'{attempt}: {a}A{b}B')

            if a == 4:
                attempts = game['attempts']
                await ctx.send(f'Correct! You guessed the number {random_string} in {attempts} attempts.')
                del games[ctx.channel.id]

@client.command(help="???", brief="????")
async def ass(ctx):  # extension: 使用者輸入要加入的功能
    await ctx.send('汪汪 我是林建甫的狗')

@client.command(help="騷阿", brief="原來是我燒起來了")
async def image(ctx):
    dcFile = discord.File("E:\\git repo\\螢幕擷取畫面 2023-12-18 223700.png")
    await ctx.send(file=dcFile)
    await ctx.send('我帥嗎')





client.run(TOKEN)  # 注意替換 'TOKEN' 為您自己的 bot token


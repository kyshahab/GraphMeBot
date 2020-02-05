# bot.py
import os
from os import path
import math
import re
import discord
import numpy as np  
from discord import TextChannel 
from discord import message 
import matplotlib.pyplot as plt  
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# set up environment variable with bot key
token = os.getenv('DISCORD_TOKEN')

# set up bot to respond to messages that begin with !
bot = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# add two numbers
@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(str(a) + ' + ' + str(b) + ' = ' + str(a+b)) 

# subtract two numbers
@bot.command()
async def subtract(ctx, a: float, b: float):
    await ctx.send(str(a) + ' - ' + str(b) + ' = ' + str(a-b)) 

# multiply two numbers
@bot.command()
async def multiply(ctx, a: float, b: float):
    await ctx.send(str(a) + ' x ' + str(b) + ' = ' + str(a*b)) 

#divide two numbers
@bot.command()
async def divide(ctx, a: float, b: float):
	# make sure denominator is not 0
	if (b == 0):
		await ctx.send("Cannot divide by 0")
	else:
		await ctx.send(str(a) + '/' + str(b) + ' = ' + str(a/b)) 
# take the power of one number to another
@bot.command()
async def pow(ctx, a: float, b: float):
	await ctx.send(str(a) + '^' + str(b) + ' = ' + str(a**b)) 
# take the factorial of a number
@bot.command()
async def fact(ctx, a: int):
	await ctx.send(str(math.factorial(a)))

# graph an equation
@bot.command()
async def graph(ctx, graph: str):
	# give default x range
	x = np.linspace(-10, 10, 250)
	# set x equal to input equation
	y = equation(graph)(x)

	#shade the x and y axes
	ax = plt.gca()
	ax.plot(x, y)
	ax.grid(True)
	ax.spines['left'].set_position('zero')
	ax.spines['right'].set_color('none')
	ax.spines['bottom'].set_position('zero')
	ax.spines['top'].set_color('none')

	plt.xlim(-10, 10)
	plt.ylim(-10, 10)

	plt.savefig("images/graph.png")
	await ctx.send(file=discord.File("images/graph.png"))
	plt.close()

# graphs equation with upper and lower limit
@bot.command()
async def boundGraph(ctx, graph: str, lowLim: float, upLim: float):
	# set x equal to bound range
	x = np.linspace(lowLim, upLim, 250)
	# set y equal to input equation
	y = equation(graph)(x)

	# shade the x and y axes
	ax = plt.gca()
	ax.plot(x, y)
	ax.grid(True)
	ax.spines['left'].set_position('zero')
	ax.spines['right'].set_color('none')
	ax.spines['bottom'].set_position('zero')
	ax.spines['top'].set_color('none')

	plt.xlim(lowLim,upLim)

	plt.savefig('images/graph1.png')
	await ctx.send(file=discord.File('images/graph1.png'))
	plt.close()

# counts the number of messages that contains a specific word 
@bot.command()
async def count(ctx, word: str, channel: discord.TextChannel = None):
	wordLower = word.lower()
	count = 0
	channel = ctx.channel
	# go through every message in chat
	async for message in channel.history():
		# if the word is in a message, count that it has been said
		if (wordLower in (message.content).lower()):
			count = count + 1
	await ctx.send("The word " + word + " has been said in " + str(count) + " messages")


# algorithm obtained from https://stackoverflow.com/questions/32726992/how-to-plot-a-math-function-from-string
# convert a string equation to a function
replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'tan' : 'np.tan',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
    'e' : '2.718281828459045'
}

allowed_words = [
    'x',
    'sin',
    'cos',
    'tan',
    'sqrt',
    'exp',
    'e'
]

def equation(string):
    ''' evaluates the string and returns a function of x '''
    # find all words and check if all are allowed:
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            raise ValueError(
                '"{}" is forbidden to use in math expression'.format(word)
            )

    for old, new in replacements.items():
        string = string.replace(old, new)

        def func(x):
        	return eval(string)

    return func

bot.run(token)

import discord
import os
from discord.ext import commands

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'TestBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
	{
		'import_path': 'chatterbot.logic.BestMatch',
		'default_response': 'I\'m sorry, but I don\'t understand. I am still learning.',
		'maximum_similarity_threshold': 0.90
	},
	    
	{
		'import_path': 'chatterbot.logic.TimeLogicAdapter',
	},
	    
	{
		'import_path': 'chatterbot.logic.MathematicalEvaluation'
	}				
    ],
    database_uri='sqlite:///database.sqlite3'
) 


# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english'
    )


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	elif str(message.content) == '$tag':
		for _ in range(3):
			for guild in client.guilds:
				for member in guild.members:
					print(message.author)
					if str(member) == str(message.author):
						continue
					if str(member) == 'Taggy#8351':
						continue
					await message.channel.send(str('<@{member}>'.format(member=member.id)))

	elif str(message.content)[0] == '$':
		await message.channel.send(str(chatbot.get_response(str(message.content)[1:])))



client.run(os.getenv('DISCORD_TOKEN_TEST'))


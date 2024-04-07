#! /usr/bin/env python3

from mailbox import Message
from telethon import TelegramClient
from telethon.hints import EntityLike

def read_config():
	import json
	
	with open('src/TelegramNotifier.json', 'r', encoding='utf-8') as file:
		return json.load(file)

async def CreateTelegaApiClient() -> TelegramClient:
	config = read_config()

	api_id = config['api_id']
	api_hash = config['api_hash']
	phone = config['phone']

	client = TelegramClient('session', api_id, api_hash)

	# connecting and building the session
	await client.connect()

	# in case of script ran first time it will
	# ask either to input token or otp sent to
	# number or sent or your telegram id
	if not await client.is_user_authorized():
		from telethon.errors import SessionPasswordNeededError

		try:
			await client.send_code_request(phone)
			# signing in the client
			await client.sign_in(phone=phone, code=input('Enter the code: '))
		except SessionPasswordNeededError:
			import getpass
			await client.sign_in(password=getpass.getpass(prompt='Enter the password:'))
		except Exception as e:
			print('Exception', e)

	return client if client.is_connected() else None


async def DestroyTelegaApiClient(client: TelegramClient):
	await client.disconnect()


def DoCheck() -> list:
	import requests
	import regex as re

	url = 'http://194.44.37.173/certificates.html'

	resp = requests.get(url=url)
	resp.encoding = 'utf-8'

	# Finding what I want
	founded:list = re.findall('[гГ]ородец', resp.text)

	return founded


async def NotifyMe(client: TelegramClient, message: str):
	print(message)

	try:
		receiver = await client.get_input_entity('@skulazkiy')

		# sending message using telegram client
		await client.send_message(receiver, message, parse_mode='html')
	except Exception as e:
		print(e)

	return


async def StartChecker():
	import time
	import datetime

	client:TelegramClient = None

	try:
		client = await CreateTelegaApiClient()

		if not (client):
			print('Client not connected!')
			return

		while (True):
			resp:list = DoCheck()

			if resp:
				await NotifyMe(client=client, message=str(resp))
				return
			else:
				print(str(datetime.datetime.now()) + ': Nothing...')

			time.sleep(60)

	finally:
		if (client):
			await DestroyTelegaApiClient(client)

	return


async def UpdateChannelMasseges():
	import time
	import datetime
	from telethon import hints
	from telethon.client import messages
	from telethon.errors import MessageNotModifiedError

	client:TelegramClient = None

	try:
		client = await CreateTelegaApiClient()

		if not client:
			print('Client not connected!')
			return

		cfg = read_config()
		chat_id = cfg['chat_id']
		channel_fullname = cfg['channel_fullname']
		channel_link = cfg['channel_link']
		
		async for msg in client.iter_messages(entity=chat_id, limit=100):
			if (channel_fullname in msg.message):
				new_msg: str = msg.message.replace(channel_fullname,
					f'[{channel_fullname}]({channel_link})')

				print('OLD', msg.message)
				print('NEW', new_msg)
				print('------------------------')
				try:
					await client.edit_message(
						entity=chat_id, 
						message=msg.id, 
						text=new_msg,
						link_preview=False
						)
				except MessageNotModifiedError as e:
					# API throw an exception if message was 'the same'
					if 'Content of the message was not modified' not in e.args[0]:
						raise e

	except Exception as e:
		print('Exception\n', e)
	finally:
		if client:
			await DestroyTelegaApiClient(client)

	return


if __name__ == '__main__':
	import asyncio

	print('Started')

	loop = asyncio.get_event_loop()
	loop.run_until_complete(
		# DoCheck()
		UpdateChannelMasseges()
	)

	print('Exited')

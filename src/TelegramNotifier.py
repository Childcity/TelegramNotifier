#! /usr/bin/env python3

from telethon import TelegramClient

async def CreateTelegaApiClient() -> TelegramClient:
    api_id = 123123123
    api_hash = '21b3b123b13b123bb123b'
    token = '576575757:AAE_-favKJBLJB Jb KJVvlvl'
    phone = '+380999445665'

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
            print(e)

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


if __name__ == '__main__':
    import asyncio

    print('Started')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait(
            [StartChecker()]
        )
    )

    print('Exited')

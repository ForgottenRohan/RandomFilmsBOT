import aiohttp
import asyncio

from random_user_agent.user_agent import UserAgent
from bs4 import BeautifulSoup

import sqlite3


url = 'https://rezka.ag/films/best/page/'

user_agent_rotator = UserAgent(software_names=['chrome'], operating_systems=['windows', 'linux'])
user_agent = user_agent_rotator.get_random_user_agent()
headers = {'User-Agent': user_agent}


async def database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS films (id INTEGER PRIMARY KEY, name TEXT, info TEXT, link TEXT)''')
    conn.commit()
    conn.close()


async def main():
    await database()
    async with aiohttp.ClientSession(headers=headers) as session:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        for i in range(0, 1269):
            new_url = url + str(i+1) + '/'
            try:
                async with session.get(new_url) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    for item in soup.find_all('div', class_='b-content__inline_item'):
                        film = item.find('div', class_='b-content__inline_item-link')
                        link = film.find('a').get('href')
                        name = film.find('a').text
                        info = film.find('div').text
                        cursor.execute('''INSERT INTO films (name, info, link) VALUES (?, ?, ?)''', (name, info, link))
                        connect.commit()
                        print(f'Film: {name} added to database')

            except:
                continue
            finally:
                connect.commit()
        connect.close()


if __name__ == '__main__':
    asyncio.run(main())
            
import aiohttp
import io
import random

from typing import List

try:
    from bs4 import BeautifulSoup
except ImportError:
    import logging
    logging.warning('Beatiful soup not installed')

from discord import File
from discord.ext.commands import cooldown, check, group, Cog

try:
    from requests import get
except ImportError:
    import logging
    logging.warning('requests not installed')

from noheavenbot.utils.constants import Fields


# Not optimal but html was so fucked up had to do something ugly like this.
def filter_crap(l: List[str]) -> List[str]:
    craps = ['i', '.', 'i', '/', '#', 'h', 'pass', 'http', 'index',
             'https', 'comments', 'register', '#inline', 'password']
    _set = set(l)
    temp_set = _set.copy()
    for i in _set:
        for crap in craps:
            if i.startswith(crap):
                temp_set.remove(i)
                break

    return list(temp_set)


def is_nsfw(ctx):
    return ctx.channel.is_nsfw()


class Fun(Cog):
    """
    Yes I do know this is al terribly hardcoded but hey, it works, if it pains you watching this
    ->MR/PR are welcome.
    """
    def __init__(self, bot):
        self.bot = bot

    @group(invoke_without_command=True, aliases=['p'])
    @cooldown(2, 5)
    @check(is_nsfw)
    async def porn(self, ctx, arg):
            src = 'data-src'
            link = f'http://www.sex.com/pics/{arg.lower()}/'

            if arg.lower() not in Fields.nsfw_categories:
                return await ctx.send('Wrong category')

            async with ctx.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        full_html = await resp.text()
                soup = BeautifulSoup(full_html, 'html.parser')

                images = [link.get(src) for link in soup.find_all('img') if link.get(src)]  #

                # link.get('data-src') can also return None
                async with aiohttp.ClientSession() as session:
                    async with session.get(random.choice(images)) as resp:
                        if resp.status != 200:
                            return await ctx.channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.channel.send(file=File(data, 'cool_image.png'))

    # lol command is very similar to porn one, only changes the way the html is being parsed, the good way would be
    # to make it work regardless of the web page html organization (kinda difficult) but i'm lazy, feel free to mr/pr
    @check(is_nsfw)
    @group(invoke_without_command=True, aliases=['lol', 'l'])
    @cooldown(2, 5)
    async def _lol(self, ctx, arg):
        src = 'href'

        if arg in ('random', 'r'):
            arg = random.choice(Fields.nsfw_lol)

        if arg.lower() not in Fields.nsfw_lol:
            return await ctx.send('Wrong category')
        if arg.lower() in Fields.nsfw_conversion['conversion_index']:
            arg = Fields.nsfw_conversion[arg]

        link = f'http://www.lolhentai.net/index?/category/{arg.lower()}/'

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    full_html = await resp.text()

            soup = BeautifulSoup(full_html, 'html.parser')

            # This is gotten from requests, yes I do know that it could block but aiohttp loses html code that is
            # critical to get the final image, requests on the other hand doesn't, the http call lasts less than
            # a second so as long as the original webpage is alright, there should be be no blocking. Maybe change to
            # requests-html since it supports asyncio operations?
            # Todo implemente a timeout so we are always 100% sure
            images = [link.get(src) for link in soup.find_all('a') if link.get(src)]  #
            images = filter_crap(images)

            # link.get('data-src') can also return None
            img_link = f'http://www.lolhentai.net/{random.choice(images)}'
            full_html = get(img_link)
            soup = BeautifulSoup(full_html.text, 'html.parser')
            final_link = soup.find(id='theMainImage')
            final_link = final_link.get('src')
            final_link = f'http://www.lolhentai.net/{final_link}'
            async with aiohttp.ClientSession() as session:
                async with session.get(final_link) as resp:
                    if resp.status != 200:
                        return await ctx.channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.channel.send(file=File(data, 'cool_image.png'))

    @check(is_nsfw)
    @group(invoke_without_command=True, aliases=['g'])
    @cooldown(2, 5)
    async def gif(self, ctx, arg):

        if arg.lower() not in Fields.nsfw_categories:
            return await ctx.send('Wrong category')

        async with ctx.channel.typing():
            link = f'http://www.sex.com/gifs/{arg.lower()}/'
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    full_html = await resp.text()
            soup = BeautifulSoup(full_html, 'html.parser')

            images = [link.get('data-src') for link in soup.find_all('img')
                        if link.get('data-src')]

            await ctx.channel.send(random.choice(images))

    #  There are ways to put all of this together but I'm lazy lazy.
    @staticmethod
    async def nsfw_list(ctx):

        if str(ctx.command.parent) in ('porn', 'gif'):
            return await ctx.channel.send("** - **".join(Fields.nsfw_categories))
        await ctx.channel.send("** - **".join(Fields.nsfw_lol))

    @gif.command(name='list')
    async def _list(self, ctx):
        await Fun.nsfw_list(ctx)

    @porn.command(name='list')
    async def __list(self, ctx):
        await Fun.nsfw_list(ctx)

    @_lol.command(name='list')
    async def ___list(self, ctx):
        await Fun.nsfw_list(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))

# http://www.lolhentai.net/picture?/40855-2651186_ahri_league_of_legends_tofuubear/category
# http://www.lolhentai.net/_data/i/upload/2018/10/25/20181025185210-26dc9d44-me.jpg

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json

commands = commands.Bot(command_prefix='')


@commands.event
async def on_ready():
    print('Masuk dengan {0.user}'.format(commands))


@commands.command()
async def cari(ctx):
    if (len(ctx.message.attachments) == 1):  # just to make sure the image is only one
        gambar = ctx.message.attachments[0].url
        await ctx.reply('Mencari anime...')

        # get API URL
        apiurl = 'https://api.trace.moe/search?anilistInfo&url=' + gambar
        r = requests.get(apiurl)  # get the response from the trace.moe API
       # print(r.text)  # this will print the responses

        detik = int(r.json()['result'][0]['from'])
        m, s = divmod(detik, 60)
        h, m = divmod(m, 60)

        # await ctx.reply('Judul native: ' + str(r.json()['result'][0]['anilist']['title']['native']) + '\n' +
        #                 'Judul romaji: ' + str(r.json()['result'][0]['anilist']['title']['romaji']) + '\n' +
        #                 'Judul english: ' + str(r.json()['result'][0]['anilist']['title']['english']) + '\n' +
        #                 'Episode: ' +
        #                 str(r.json()['result'][0]['episode']) + '\n' +
        #                 'Pada menit ke:' + f'{h:d}:{m:02d}:{s:02d}' + '\n' +
        #                 ('%.2f%%' % (float(r.json()['result'][0]['similarity']) * 100) + ' similarity'))

        # with embed
        judulnative = str(r.json()['result'][0]['anilist']['title']['native'])
        judulromaji = str(r.json()['result'][0]['anilist']['title']['romaji'])
        judulenglish = str(r.json()['result'][0]
                           ['anilist']['title']['english'])
        eps = str(r.json()['result'][0]['episode'])
        menit = f'{h:d}:{m:02d}:{s:02d}'
        similiarity = '%.2f%%' % (
            float(r.json()['result'][0]['similarity']) * 100) + ' similarity'
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_image(url=gambar)
        embed.add_field(name='Judul', value='Native:' + judulnative + '\n' +
                        'Romaji: ' + judulromaji + '\n' + 'English: ' + judulenglish, inline=False)
        embed.add_field(name='Episode', value=eps)
        embed.add_field(name='Pada menit ke', value=menit)
        embed.add_field(name='Similarity', value=similiarity, inline=False)
        await ctx.reply(embed=embed)

        # this will get the video from the trace.moe API
        video = r.json()['result'][0]['video']
        reqvideo = requests.get(video)
        videoname = r.json()['result'][0]['filename'] + '.mp4'
        with open(videoname, 'wb') as f:
            f.write(reqvideo.content)
            f.close()
        # and then send the video
        await ctx.reply(file=discord.File(videoname))
        os.remove(videoname)

    elif (len(ctx.message.attachments) > 1):
        await ctx.reply('Hanya boleh 1 gambar')
    else:
        await ctx.reply('kirim gambar dulu!')


# baca token method
def baca_token():
    with open('token.txt', 'r') as filetoken:
        lines = filetoken.readlines()
        return lines[0].strip()


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
commands.run(TOKEN)

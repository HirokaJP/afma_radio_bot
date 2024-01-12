# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import os
from datetime import time, timezone, timedelta
import datetime
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive

JST = timezone(timedelta(hours=+9), "JST")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  loop.start()


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


@tasks.loop(seconds=60)
async def loop():
  now = datetime.datetime.now().astimezone(JST)
  #print(now)
  #print(now.date().weekday())
  """
    Day
    0 Mon
    1 Tue
    2 Wed
    3 Thur
    4 Fri
    5 Sat
    6 Sun
    """
  if now.date().weekday() >= 5:
    channel = client.get_channel(int(os.getenv("CHANNEL_ID")))
    if now.hour == 12 and now.minute == 00:
      message = '<@&1158088019459444817>\r\n' + '<:emoji_4:1101469155712045117>'
      if now.date().weekday() == 5:
        message += '今日は土曜日だよ！<:emoji_3:1101469120790278164>\r\n' + '<:emoji_2:1101469083108659301>21時からアフマ部ラジオ収録に来られる人手を挙げて！'
      else:
        message += '今日は日曜日だよ！<:emoji_3:1101469120790278164>\r\n' + '<:emoji_2:1101469083108659301>23時からアフマ部ラジオ収録に来られる人手を挙げて！'
      message += '<:emoji_1:1101469044042891304>\r\n' + ':radio:リアクションが3人以上集まったら収録しよう！:microphone2:'
      await channel.send(message)
    elif now.hour == 18 and now.minute == 0:
      end_date = datetime.datetime.now()
      start_date = end_date - datetime.timedelta(hours=7)
      messages = []
      async for message in channel.history(after=start_date, before=end_date):
        messages.append(message)

      for message in messages:
        content = message.content
        author = message.author.name
        if author == "今日はラジオ収録する？":
          #print(f"Received message '{content}' from {author} in channel {channel.name}")
          reactions = message.reactions
          # Iterate through the reactions
          user_list = []
          for reaction in reactions:
            # Process each reaction as desired
            #print(f"Reaction {reaction.emoji} has {reaction.count} counts")
            users = []
            async for user in reaction.users():
              users.append(user)
            # Iterate through the users
            for user in users:
              print(f"User {user.name} ")
              user_list.append(user.mention)
          mention_str = ""
          unique_user_list = list(set(user_list))
          for each_user in unique_user_list:
            mention_str += each_user + " "

          message = ""
          if len(unique_user_list) == 0:
            await channel.send(f'3人にならなかったので、今週はスキップです。')

          elif len(unique_user_list) < 3:
            await channel.send(
                f'{mention_str}\r\nリアクションありがとう。3人にならなかったので、今週はスキップです。')
          else:
            hold_time = 23
            if now.date().weekday() == 5:
              hold_time = 21
            await channel.send(
                f'{mention_str}\r\n 開催決定です！{hold_time}時に集まりましょう！')

      ##await channel.send('ゴミ出しに行こうね！')


try:
  keep_alive()
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
##except discord.HTTPException as e:
##    if e.status == 429:
##        print(
##"The Discord servers denied the connection for making too many requests"
##)
##print(
##"Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
##)
##else:
##raise e
except:
  os.system("kill 1")

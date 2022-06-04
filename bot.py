from discord.ext import commands
import discord
import keep_alive
import json
import os
import random

intents=discord.Intents.all()
bot=commands.Bot(command_prefix="~",intents=intents)

# calc
from math import *
def operation(s):
    s = s.replace(' ', '')
    s = s.replace('^', '**')
    s = s.replace('log', 'log10')
    s = s.replace('ln', 'log')
    i, t = len(s) - 1, 0
    while i >= 0: # 處理 "factorial 階乘"
        if s[i] == '!':
            if s[i - 1].isdigit():
                t, i = i, i - 1
                while s[i].isdigit():
                    i -= 1
                tmp = s[i + 1: t]
                s = s[:i + 1] + 'factorial(' + tmp + ')' + s[t + 1:]
            else:
                t, right, i = i, 1, i - 2
                while right:
                    if s[i] == ')':
                        right += 1
                    if s[i] == '(':
                        right -= 1
                    i -= 1
                tmp = s[i + 1:t]
                s = s[:i + 1] + 'factorital(' + tmp + ')' + s[t + 1:]
        i -= 1
    try:
        res = round(eval(s), 3)
        return res
    except:
        res = '(type error or too difficult)'
        return res

 # now
import datetime
def gettime():
    x = datetime.datetime.now()
    err = datetime.timedelta(hours=8)
    x += err
    y = x.year
    m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
         'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x.month - 1]
    d = x.day
    h = x.hour
    mi = x.minute
    s = x.second
    w = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][(x.weekday() + 1) % 7]
    res = '{} {} {:02d} {:02d}:{:02d}:{:02d} {}'.format(w, m, d, h, mi, s, y)
    return res

@bot.event
async def on_ready():
    global coins
    data = None
    try:
        with open("coins.json", 'r') as f:
            data = f.read()
        coins = json.loads(data)
    except:
        with open("coins.json", 'x') as f:
            f.write("{}\n")
        coins = dict()
    await bot.change_presence(status = discord.Status.idle,\
        activity = discord.Activity(name = '~help',\
            type = discord.ActivityType.listening))
    print("I'm online now.")
"""
@bot.event
async def on_message(message):
    if message.author==bot.user:
        return
    if message.content=='hi':
        await message.channel.send(":D")
"""
@bot.event
async def on_member_join(member):
    await member.send(f'Welcome {member.name} to join this server!')

@bot.event
async def on_member_remove(member):
    await member.send(f'So sad to see {member.name} leave this server, hope you to join here again.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'My ping is {round(bot.latency * 1000)} (ms) :stopwatch:')

@bot.command()
async def say(ctx, *,args):
    if ctx.author.bot:
        return 
    is_admin = bool(False)
    for role in ctx.author.roles:
        if role.name == 'admin':
            is_admin = True
            break
    if is_admin == False:
        await ctx.send('You are not admin!')
        return
    tmp=args
    await ctx.message.delete()
    try:
        await ctx.send(tmp)
    except:
        await ctx.send("Type error. (You can't made me say empty sentence.)")

@bot.command()
async def calc(ctx, *,args):
    ans=operation(args)
    await ctx.send(f'Result of {args} is {ans}.')

@bot.command()
async def now(ctx):
    await ctx.send(gettime())

@bot.command()
async def guess(ctx, *,args):
    # guess
    import random
    def Guess(n):
        tmp = random.randint(1, 5)
        a = ['false', 'true']
        s = f'right ans is {tmp}, your ans is {a[n == tmp]}'
        return s
    await ctx.send(Guess(int(args)))

@bot.command()
async def join(ctx):
    if coins.get(str(ctx.message.author.id),-1)==-1:
        coins[str(ctx.message.author.id)]=48763
        await ctx.send("Successfully Registered.")
    else:
        await ctx.send("You've registered it.")
    with open("coins.json", 'w') as f:
        json.dump(coins, f)

@bot.command()
async def dice(ctx, *,args):
    money=int(args)
    if str(ctx.message.author.id) not in coins:
        await ctx.send('You should join first.')
    elif money>coins[str(ctx.message.author.id)]:
        await ctx.send('You don\'t have enough money!')
    elif money<=0:
        await ctx.send('Type error!')
    else:
        a=random.randint(1,6)
        b=random.randint(1,6)
        c=random.randint(1,6)
        d=random.randint(1,6)
        await ctx.send(f'You roll {a} and {b}, {a+b} in total.')
        await ctx.send(f'I roll {c} and {d}, {c+d} in total.')
        if a+b>c+d and a==b:
            await ctx.send(f'Orz! You roll the same points. You can earn {money}*2 dollars!')
            coins[str(ctx.message.author.id)]+=2*money
        elif a+b>c+d:
            await ctx.send(f'Congrats! You won {money} dollars!')
            coins[str(ctx.message.author.id)]+=money
        elif a+b<c+d:
            await ctx.send(f'You lost {money} dollars.')
            coins[str(ctx.message.author.id)]-=money
        else:
            await ctx.send('Tie')
        await ctx.send(f'Now you have {coins[str(ctx.message.author.id)]} dollars.')
        with open("coins.json",'w') as f:
            json.dump(coins,f)

@bot.command()
async def spam(ctx, *,args):
    tmp=args.split(' ',1)
    times=int(tmp[1])
    sentence=tmp[0]
    if times>=0:
        for i in range(times):
            await ctx.send(sentence)
    else:
        await ctx.send('The spam times can\'t be zero or lower.')
@bot.command()
async def coins(ctx):
    await ctx.send(f'You have {coins[str(ctx.message.author.id)]} dollars now.')

@bot.command()
async def give(ctx, *,args):
    if str(ctx.message.author.id in coins):
        tmp=args.split(' ',1)
        money=int(tmp[1])
        if money>0:
            person=str(ctx.message.mentions[0].id)
            name=str(ctx.message.mentions[0].name)
            if person not in coins:
                coins[person]=1000
            await ctx.send(f'You\'ve given {name} {money} dollars.')
            coins[person]+=money
            coins[str(ctx.message.author.id)]-=money
            with open("coins.json",'w') as f:
                json.dump(coins,f)
        else:
            await ctx.send("That's illegal.The money number should be positive!")
    else:
        await ctx.send("You should join first.")
bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help",color = 2123412)
    embed.add_field(name = 'My prefix',\
    	value = '~',\
    	inline = False)
    embed.add_field(name = '~help',\
    	value = 'To get help',\
    	inline = False)
    embed.add_field(name = '~calc <formula>',\
    	value = 'To calculate your formula',\
    	inline = False)
    embed.add_field(name = '~now', 
    	value = 'To get the current time',\
    	inline = False)
    embed.add_field(name = '~guess <number>',\
    	value = 'To guess a number (range : 1 ~ 5)',\
    	inline = False)
    embed.add_field(name = '~ping',\
    	value = 'To get the latency of the bot.',\
    	inline = False)
    embed.add_field(name = '~say <sentence>',\
    	value = 'To repeat a sentence you typed in.(\'admin\' roles only)',\
    	inline = False)
    embed.add_field(name = '~join',\
    	value = 'To join the game and then you can earn your money by playing.',\
    	inline = False)
    embed.add_field(name = '~dice <money>',\
    	value = 'To roll a dice.',\
    	inline = False)
    embed.add_field(name = '~give <user> <counts>',\
    	value = 'To give someone you mentioned money.',\
    	inline = False)
    embed.add_field(name = '~coins',\
    	value = 'To show how much money you have now.',\
    	inline = False)
    await ctx.send(embed = embed)

keep_alive.keep_alive()
bot.run('My TOKEN')

from discord.ext import commands
import discord
import json
import os
from random import choice
import random
import asyncio
from googletrans import Translator

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
    while i >= 0: 
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

def getdate():
    x = datetime.datetime.now()
    err = datetime.timedelta(hours=8)
    x += err
    y = x.year
    m = x.month
    d = x.day
    res=str(y)+'-'+str(m)+'-'+str(d)
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
        print(f'{str(ctx.message.author.name)}: {tmp}')
    except:
        await ctx.send("Type error. (You can't made me say empty sentence.)")

@bot.command()
async def translate(ctx, *,args):
    translator = Translator()
    translation = translator.translate(args, dest='en')
    s=str(translation.text)
    s=s.capitalize()
    await ctx.send(s)

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
async def vote(ctx, *,args):
    emoji=['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣',]
    options=args.split('|')
    print(options)
    question=options[0]
    embed = discord.Embed(title='Vote started in '+getdate(),description=str(question),color = 1752220)
    for i in range(1,len(options)):
        embed.add_field(name=emoji[i-1]+": "+str(options[i]),\
                        value='------------------------------------',\
                        inline=False)
    msg=await ctx.send(embed=embed)
    for i in range(1,len(options)):
        await msg.add_reaction(emoji[i-1])
    
@bot.command()
async def join(ctx):
    if coins.get(str(ctx.message.author.name),-1)==-1:
        coins[str(ctx.message.author.name)]=48763
        await ctx.send("Successfully Registered.")
    else:
        await ctx.send("You've registered it.")
    with open("coins.json", 'w') as f:
        json.dump(coins, f)

@bot.command()
async def dice(ctx, *,args):
    money=int(args)
    if str(ctx.message.author.name) not in coins:
        await ctx.send('You should join first.')
    elif money>coins[str(ctx.message.author.name)]:
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
            coins[str(ctx.message.author.name)]+=2*money
        elif a+b>c+d:
            await ctx.send(f'Congrats! You won {money} dollars!')
            coins[str(ctx.message.author.name)]+=money
        elif a+b<c+d:
            await ctx.send(f'You lost {money} dollars.')
            coins[str(ctx.message.author.name)]-=money
        else:
            await ctx.send('Tie')
        await ctx.send(f'Now you have {coins[str(ctx.message.author.name)]} dollars.')
        with open("coins.json",'w') as f:
            json.dump(coins,f)

@bot.command()
async def remindme(ctx, *,args):
    tmp=args.split(' ',1)
    date=tmp[0]
    thing=tmp[1]
    a=date.split('h')
    hour=int(a[0])
    b=a[1].split('m')
    mins=int(b[0])
    c=b[1].split('s')
    sec=int(c[0])
    total=3600*hour+60*mins+sec
    embed=discord.Embed(title=thing,description=f'I will remind you in {hour}hrs {mins}mins {sec}s.')
    await ctx.send(embed=embed)
    await asyncio.sleep(total)
    embed=discord.Embed(title=thing,description=f"{ctx.author.mention} You were going to {thing} and asked me to remind you.")
    await ctx.send(embed=embed)

@bot.command()
async def rps(ctx, *,args):
    if str(ctx.message.author.name) in coins:
        res=args.split(' ')
        op=str(res[0])
        money=int(res[1])
        ges=["rock","paper","scissor"]
        x=choice(ges)
        await ctx.send(f'You threw {op}, I threw {x}.')
        if op==x:
            await ctx.send('Tie')
        elif (op=="rock" and x=="scissor") or (op=="paper" and x=="rock") or (op=="scissor" and x=="paper"):
            await ctx.send(f'Congrats! You won and earned {money} dollars.')
            coins[str(ctx.message.author.name)]+=money
        else:
            await ctx.send(f'QQ! You lost {money} dollars.')
            coins[str(ctx.message.author.name)]-=money
        with open("coins.json",'w') as f:
                json.dump(coins,f)
        await ctx.send(f'Now you have {coins[str(ctx.message.author.name)]} dollars.')
    else:
        await ctx.send('You should join first.')

@bot.command()
async def slots(ctx):
    if str(ctx.message.author.name) in coins:
        emoji=['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣',]
        a=choice(emoji)
        b=choice(emoji)
        c=choice(emoji)
        embed=discord.Embed(title="Lottery",color=3066993)
        embed.add_field(name = a,\
        	value = '-----',\
        	inline = True)
        embed.add_field(name = b,\
        	value = '-----',\
        	inline = True)
        embed.add_field(name = c,\
        	value = '-----',\
        	inline = True)
        if a==b==c:
            embed.add_field(name = 'Result',\
        	    value = 'ORZ! You earned the first prize, 48763 dollars.',\
        	    inline = False)
            coins[str(ctx.message.author.name)]+=48763
        elif a==b or b==c or a==c:
            embed.add_field(name = 'Result',\
        	    value = 'Congrats! You earned 1000 dollars.',\
        	    inline = False)
            coins[str(ctx.message.author.name)]+=1000
        else:
            embed.add_field(name = 'Result',\
        	    value = 'You lost 1000 dollars. QwQ',\
        	    inline = False)
            coins[str(ctx.message.author.name)]-=1000
        await ctx.send(embed=embed)
        with open("coins.json",'w') as f:
                json.dump(coins,f)
        await ctx.send(f'Now you have {coins[str(ctx.message.author.name)]} dollars.')
    else:
        await ctx.send("You should join first.")

@bot.command()
async def rank(ctx):
    if len(coins)==0:
        await ctx.send("No one has registered yet.")
    else:
        num=min(10,len(coins))
        sortedcoins=dict(sorted(coins.items(),key=lambda x:x[1],reverse=True))
        embed=discord.Embed(title='Coins Ranking',description='Let\'s see who earned the most money!',color=15844367)
        j=0
        for i in sortedcoins.keys():
            j+=1
            embed.add_field(name=f"#{j} "+i,value=sortedcoins[i],inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def spam(ctx, *,args):
    tmp=args.split(' ',1)
    times=int(tmp[1])
    sentence=tmp[0]
    if times>=0:
        if times<=20:
            for i in range(times):
                await ctx.send(sentence)
        else:
            await ctx.send("The spam times are too high.")
    else:
        await ctx.send('The spam times can\'t be zero or lower.')
@bot.command()
async def coins(ctx):
    if str(ctx.message.author.name) in coins:
        await ctx.send(f'You have {coins[str(ctx.message.author.name)]} dollars now.')
    else:
        await ctx.send('You should join first.')

@bot.command()
async def give(ctx, *,args):
    if str(ctx.message.author.name in coins):
        tmp=args.split(' ',1)
        money=int(tmp[1])
        if money>0:
            if money<=coins[str(ctx.message.author.name)] and ctx.message.mentions[0].name!=ctx.message.author.name:
                person=str(ctx.message.mentions[0].name)
                name=str(ctx.message.mentions[0].name)
                if person not in coins:
                    coins[person]=48763
                    await ctx.send(f'{person} has been registered.')
                await ctx.send(f'You\'ve given {name} {money} dollars.')
                coins[person]+=money
                coins[str(ctx.message.author.name)]-=money
                with open("coins.json",'w') as f:
                    json.dump(coins,f)
                await ctx.send(f'Now you have {coins[str(ctx.message.author.name)]} dollars.')
                
            elif str(ctx.message.mentions[0].name)==str(ctx.message.author.name):
                await ctx.send("You can't give money to yourself. That\'s meaningless.")
            else :
                await ctx.send("You don't have enough money.")
        else:
            await ctx.send("That's illegal.The money number should be positive!")
    else:
        await ctx.send("You should join first.")
bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help",color = 2123412)
    embed.add_field(name = 'My prefix.',\
    	value = '~',\
    	inline = True)
    embed.add_field(name = '~help',\
    	value = 'To get help.',\
    	inline = True)
    embed.add_field(name = '~calc <formula>',\
    	value = 'To calculate your formula.',\
    	inline = True)
    embed.add_field(name = '~now', 
    	value = 'To get the current time.',\
    	inline = True)
    embed.add_field(name = '~guess <number>',\
    	value = 'To guess a number (range : 1 ~ 5).',\
    	inline = True)
    embed.add_field(name = '~ping',\
    	value = 'To get the latency of the bot.',\
    	inline = True)
    embed.add_field(name = '~say <sentence>',\
    	value = 'To repeat a sentence you typed in.(\'admin\' roles only)',\
    	inline = True)
    embed.add_field(name = '~vote <question>|<option1>|<option2>|...(up to ten options)',\
    	value = 'To start a vote.',\
    	inline = True)
    embed.add_field(name = '~choose <option1> <option2> <option3>....',\
    	value = 'To choose between the options you gived randomly.',\
    	inline = True)
    embed.add_field(name = '~join',\
    	value = 'To join the game and then you can earn your money by playing.',\
    	inline = True)
    embed.add_field(name = '~dice <money>',\
    	value = 'To roll a dice.',\
    	inline = True)
    embed.add_field(name = '~slots',\
    	value = 'To play a tiny lottery game.',\
    	inline = True)
    embed.add_field(name = '~rps <option> <money>',\
    	value = 'To play the rps game.',\
    	inline = True)
    embed.add_field(name = '~give <user> <counts>',\
    	value = 'To give someone you mentioned money.',\
    	inline = True)
    embed.add_field(name = '~coins',\
    	value = 'To show how much money you have now.',\
    	inline = True)
    embed.add_field(name = '~rank',\
    	value = 'To see who earned the most money.',\
    	inline = True)
    await ctx.send(embed = embed)

bot.run('MY TOKEN')

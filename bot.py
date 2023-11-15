import discord
from discord.ext import commands
import deck
import player
import dealer
import os
import asyncio


intents = discord.Intents.all() #allowing all intents
intents.members = True
bot = commands.Bot(command_prefix = "+",help_command=None,intents = intents) #Creating our bot

#Global variable (I know I shouldn't do this but I couldn't think of another way)
def set_up_players():
    bot.bet_amount = {}
    bot.players_money = {}
    bot.isinround = {}
    bot.turn = {}
    bot.game_start = {}
    bot.list_of_players = {}
    bot.deck_of_cards = {}
    for guild in bot.guilds:
        bot.bet_amount[guild.id] = {}
        bot.isinround[guild.id] = False
        bot.turn[guild.id] = 0
        bot.game_start[guild.id] = False
        bot.list_of_players[guild.id] = {}
        bot.deck_of_cards[guild.id] = deck.Deck() 
        for member in guild.members:
            # print(member)
            bot.players_money[member] = 100
    # print(bot.players_money)
    # print(bot.isinround)
    # print(bot.game_start)
    # print(bot.list_of_players)


@bot.event
async def on_ready():  
    try: # If bot can connect to the discord
        print('Discord bot succesfully connected')
        set_up_players()
    except:
        print("[!] Couldn't connect, an Error occured")


async def display_winner(ctx, dealer_score):
    '''Display the winner of that round of blackjack and how many round each person won'''
    for pl in bot.list_of_players[ctx.guild.id]:
        player_score = bot.list_of_players[ctx.guild.id][pl].score()
        print(bot.bet_amount[ctx.guild.id])
        print(bot.bet_amount[ctx.guild.id][pl])
        if player_score > 21 or dealer_score > player_score and dealer_score <= 21:
            # bot.players_money[pl] -= bot.bet_amount[ctx.guild.id][pl]
            await ctx.send(f'{pl.name} lost ${bot.bet_amount[ctx.guild.id][pl]}')
        elif dealer_score > 21 or player_score > dealer_score and player_score <= 21:
            bot.players_money[pl] += 2 * bot.bet_amount[ctx.guild.id][pl]
            await ctx.send(f'{pl.name} won ${bot.bet_amount[ctx.guild.id][pl]}')
        else:
            bot.players_money[pl] += bot.bet_amount[ctx.guild.id][pl]
            await ctx.send(f'{pl.name} tied with the dealer')
        print(bot.players_money[pl])


@bot.command(name='help')
async def help(ctx):
    await ctx.send(
'''
```
        How to use TwentyOne to play Blackjack:
1. Use the "+RestlessGambler" command to start a game
2. During buy in phase, use "+buyin <bet amount>" to join the round
3. Use +start to end buy in phase and start the round
4. One player can hit or stand at a time, use +hit or +stand
5. Once all players finish, the dealer will play and winnings will be distributed

                List of Commands:
+help - Display the all the commands for the bot
+bal - Shows your balance that is shared through all the server the bot is in
+RestlessGambler - Begin the game of blackjack by sending it to the buy in phase
+buyin <bet amount> - How to join the round of blackjack. Minimum buy in is $5
+leave - Back out of playing and get a refund on the amount you paid in
+start - End buy in phase and start the game of blackjack. One player gets to hit or stand at a time
+hit - Draw a card from the deck, the card will be displayed 
+stand - End your turn
```
'''
)   


@bot.command(name='bal')
async def balance(ctx):
    await ctx.send(f'{ctx.author} has ${bot.players_money[ctx.author]} in their pockets')
    #If i want to allow +bal @User then change the key from member to member.id. Might work?
    # await ctx.send(f'{arg} has ${bot.players_money[arg]} in their pockets')


@bot.command(name='loan')
async def loan(ctx, arg: int):
    if arg <= 0:
        await ctx.send('Ask for more money')
    if arg > 10000:
        await ctx.send("You can't handle that much money")
    await ctx.send(f'{ctx.author} has just taken a ${arg} loan with a 20% interest rate')
    bot.players_money[ctx.author] += arg


@bot.command(name='buyin')
async def buy_in(ctx, arg: int): #Take in a certain amount of money
    if not bot.game_start[ctx.guild.id]:
        await ctx.send('Use +RestlessGambler command to start a game of Blackjack')
        return
    if bot.isinround[ctx.guild.id]:
        await ctx.send('Wait till after this round to join into the game')
        return
    if bot.players_money[ctx.author] < arg:
        await ctx.send("You don't have enough money")
        return
    if ctx.author not in bot.list_of_players[ctx.guild.id] and arg >= 5:
        await ctx.send(f'{ctx.author} joins the round') 
        # bot.list_of_players[ctx.guild.id].append(ctx.author)
        bot.list_of_players[ctx.guild.id][ctx.author] = player.Player(bot.deck_of_cards[ctx.guild.id])
        bot.bet_amount[ctx.guild.id][ctx.author] = arg
        print(bot.bet_amount[ctx.guild.id][ctx.author])
        await ctx.send(f'{ctx.author} has betted ${arg} to join the round')
        bot.players_money[ctx.author] -= arg
        # await ctx.send(f'{ctx.author} has ${bot.players_money.get(ctx.author)} in their pocket')
        # print(bot.list_of_players)
    else:
        await ctx.send('Minimum bet amount is $5')


@bot.command(name='leave')
async def leave(ctx):
    if not bot.game_start[ctx.guild.id]:
        await ctx.send('Use +RestlessGambler command to start a game of Blackjack')
        return
    if bot.isinround[ctx.guild.id]:
        await ctx.send("You can't leave once you are in!")
        return
    if ctx.author not in bot.list_of_players[ctx.guild.id]:
        await ctx.send("You haven't join in yet")
        return
    await ctx.send(f'{ctx.author} chickened out!')
    del bot.list_of_players[ctx.guild.id][ctx.author]
    bot.players_money[ctx.author] += bot.bet_amount[ctx.guild.id][ctx.author]
    print(bot.players_money[ctx.author])


@bot.command(name='start')
async def start(ctx):
    if not bot.game_start[ctx.guild.id]:
        await ctx.send('Use +RestlessGambler command to start a game of Blackjack')
        return
    bot.isinround[ctx.guild.id] = True


@bot.command(name='hit')
async def hit(ctx):
    if not bot.game_start[ctx.guild.id]:
        await ctx.send('Use +RestlessGambler command to start a game of Blackjack')
        return
    if not bot.isinround[ctx.guild.id]:
        await ctx.send('Use +start to start the round')
        return
    # print(list(bot.list_of_players[ctx.guild.id])[bot.turn[ctx.guild.id]])
    if ctx.author != list(bot.list_of_players[ctx.guild.id])[bot.turn[ctx.guild.id]]:
        await ctx.send('It is not your turn yet')
    #dictionary bot.list_of_players = {guild.id, {member, player.Player}}
    card_drawn = bot.list_of_players[ctx.guild.id][ctx.author].hit()
    await ctx.author.send('Your hand:\n')
    await ctx.author.send(bot.list_of_players[ctx.guild.id][ctx.author])
    await ctx.send(f'{ctx.author} drew the card {card_drawn}')
    

@bot.command(name='stand')
async def stand(ctx): #WORK ON STAND PLS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not bot.game_start[ctx.guild.id]:
        await ctx.send('Use +RestlessGambler command to start a game of Blackjack')
        return
    if not bot.isinround[ctx.guild.id]:
        await ctx.send('Use +start to start the round')
        return
    # print(list(bot.list_of_players[ctx.guild.id])[bot.turn[ctx.guild.id]])
    if ctx.author != list(bot.list_of_players[ctx.guild.id])[bot.turn[ctx.guild.id]]:
        await ctx.send('It is not your turn yet')
    bot.turn[ctx.guild.id] += 1


@bot.command(name="RestlessGambler")
async def main(ctx):
    if bot.game_start[ctx.guild.id] is True: #prevent calling the game twice
        await ctx.send('The game has already started')
        return
    bot.game_start[ctx.guild.id] = True
    await ctx.send(
'''
```
Ready to lose your money? IT IS TIME FOR BLACKJACK!

If you would like to join, type in the command "+buyin <bet amount>"
```
'''
)   
    bot.deck_of_cards[ctx.guild.id].shuffle()
    while not bot.isinround[ctx.guild.id]: #this is when you buyin
        await asyncio.sleep(1)

    await ctx.send("let's begin this round!")
    for pl in bot.list_of_players[ctx.guild.id]:
        # Player = player.Player(deck_of_cards)
        player_object = bot.list_of_players[ctx.guild.id][pl]
        await pl.send('Your hand:\n')
        await pl.send( player_object)
        await ctx.send(f'Would {pl.name} like to hit or stand?')
        current_turn_number = bot.turn[ctx.guild.id]
        # bot.current_player[ctx.guild.id] = pl
        while bot.turn[ctx.guild.id] == current_turn_number: #each player's turn
            if player_object.score() > 21:
                bot.turn[ctx.guild.id] += 1
                await asyncio.sleep(1)
                await ctx.send('Bust!!!!!')
            await asyncio.sleep(1)
        # await pl.send(Player)
        # await pl.send(bot.list_of_players[ctx.guild.id][pl])
    
    #Dealer's turn
    Dealer = dealer.Dealer(bot.deck_of_cards[ctx.guild.id])
    await ctx.send(Dealer.play())
    asyncio.sleep(2) #delay displaying the winner to let player process
    await display_winner(ctx, Dealer.score())
    await ctx.send('Good round! You should gamble again!')

    bot.bet_amount[ctx.guild.id] = {}
    bot.isinround[ctx.guild.id] = False
    bot.turn[ctx.guild.id] = 0
    bot.game_start[ctx.guild.id] = False
    bot.list_of_players[ctx.guild.id] = {}
    bot.deck_of_cards[ctx.guild.id] = deck.Deck()



bot.run(os.getenv('discord_token'))
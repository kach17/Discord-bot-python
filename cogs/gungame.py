import random
from discord.ext import commands


#add a quit command ffs
#and load from the main directory
#bye for now


# Global variables:
# shield : 0 | shoot : 1 | reload : 2
cpu_bullets = 1
p1_bullets = 1
cpu_won = False
p1_won = False
p1_action = 0
cpu_action = 0
moveOutcome = [ [0,0,0], [0,0,-1], [0, 1, 0] ]
move = 0
gunGame = False
playerTurn = False
correctInput = True




class GunGameCog(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  @commands.Cog.listener()
  async def on_message(self, message):
    message.content.lower()
    if message.author.bot:
      return
    

    global cpu_bullets, p1_bullets, cpu_won, p1_won, p1_action, cpu_action, moveOutcome, move, gunGame, playerTurn, correctInput



    # Game starts with the keyWord: $play
    if message.content==('$play'):
        if(gunGame): 
            await message.channel.send('```Game has already started```')
        else:
            await message.channel.send('```Starting game...```')
            cpu_bullets = 1
            p1_bullets = 1
            cpu_won = False
            p1_won = False
            p1_action = 0
            cpu_action = 0
            moveOutcome = [ [0,0,0], [0,0,-1] ,[0, 1, 0] ]
            move = 0
            gunGame = True
            correctInput = True
            playerTurn = False
    # Prints out rules of the game when the command "$rules" is called       
    if message.content==('$rules'):
        rules_message =  '```Play against the computer: Can shoot, block, or reload. \n' \
                        'Blocking  -- Negates a shooting action from the computer. \n' \
                        'Reloading -- Increases number of bullets owned (up to a maximum of 5). \n' \
                        'Shooting  -- Must have a bullet. If the oponent is reloading, you win. \n' \
                        '             If both players shoot, nothing happens, other than losing a bullet. \n```' \

        await message.channel.send(rules_message)
        return 

    # Prints out the game commands and their functions when the command "$help" is called. 
    if message.content==('$help'):
        help_message =  '```$rules -- Shows rules of GunGame \n' \
                        '$play -- Starts Game \n' \
                        '$end -- Ends Game```' \

        await message.channel.send(help_message)
        return 

    # Ends the current game session
    if message.content==('$end'):
        if(gunGame):
            await message.channel.send('```Ending game...```')
            gunGame = False
            return
        else:
             await message.channel.send('```No game in progress```')
             return
    
        
    # CPU chooses action
    def cpuAction():
        global cpu_bullets, cpu_action

        #Firstly, we check bullets of the cpu, if it does not have any, then it can't do the shoot action
        if(cpu_bullets != 0):
            #if player has no bullets, then cpu should reload or shoot, as shielding wont be beneficial
            if(p1_bullets == 0):
                cpu_action = random.randint(1, 2)
            else:
                cpu_action = random.randint(0,2)
        #cpu has no bullets, so reloading or shielding are our only options
        elif (cpu_bullets == 0):
            #again, reload if player has no bullets, else randomly choose btwn shielding n reloading
            if(p1_bullets == 0):
                cpu_action = 2
            else:
                cpu_action = random.choice([0, 2])
        else:
            cpu_action = 0

        #2 -> reload so we add 1 to bullet count. 1 -> shoot so we subtract 1 from bullet count
        if(cpu_action == 2): cpu_bullets += 1
        if(cpu_action == 1): cpu_bullets -= 1

    # Gets the users action
    if(gunGame):
        if((not p1_won) and (not cpu_won)):

            # Goes here if player chose to shield
            if message.content==('$0'):
                p1_action = 0
                playerTurn = True
                correctInput = True
                cpuAction()

            # Goes here if player chose to shoot
            if message.content==('$1'):
                correctInput = True

                # Checks if player has enough bullets. esle...
                if (p1_bullets>0):
                    p1_action = 1
                    p1_bullets -= 1
                    playerTurn = True
                    cpuAction()

                # Player needs to try anoher action
                else:
                    await message.channel.send("```No more bullets. Try Again.```")
                    return
            # Goes here if player decided to shield
            if message.content==('$2'):
                correctInput = True
                p1_action = 2
                p1_bullets += 1
                playerTurn = True
                cpuAction()

    if(not correctInput):
        await message.channel.send("```Wrong Input```")
        return

    # Prints out each player's bullets and determines if a player has shot one another (won) yet.
    if (not p1_won and not cpu_won):
        disc_message = ""
        
        # Prints the amount of bullets each player has... up to 5 bullets
        if cpu_bullets > 5:
            cpu_bullets = 5
        if p1_bullets > 5:
            p1_bullets = 5
        disc_message += "```     P1 Bullets     CPU Bullets"+"\n"
        disc_message += "     "
        for n in range(p1_bullets):
            disc_message += "\u25AE"
        for n in range(5 - p1_bullets):
            disc_message += "\u25AF"
        disc_message += "      "
        for n in range(cpu_bullets):
            disc_message += "\u25AE"
        for n in range(5 - cpu_bullets):
            disc_message += "\u25AF"
        disc_message += "    "
        disc_message += "\n\n"

        # choices =    Block,          Shoot,        Reload
        choices = ['\U0001f6e1\uFE0F', '\U0001F3F9', '\U0001F504']

        # After the player chooses their turn, the outcome is determined...
        if(playerTurn):
            disc_message += "       P1: " + choices[p1_action] + "        "  + "CPU: " + choices[cpu_action] + "\n\n"

            # Player wins if they shoots and computer reloads
            if moveOutcome[cpu_action][p1_action] == 1:
                p1_won = True
    
            # CPU wins if it shoots and player reloads
            if moveOutcome[cpu_action][p1_action] == -1:
                cpu_won = True

            # Reset the player turn to false since the turn ended  
            playerTurn = False

        # Prints the actions possible with their corresponding picture
        disc_message += "Choose Action: \U0001f6e1\uFE0F[$0] \U0001F3F9[$1] \U0001F504[$2] " + "\n"
        await message.channel.send(disc_message + "```")

        correctInput = False

    # Prints the outcome of the game
    if(p1_won):
        await message.channel.send("```YOU WON```")
        gunGame = False
        playerTurn = True
    if(cpu_won):
        await message.channel.send("```YOU LOSE```")
        gunGame = False
        playerTurn = True


def setup(bot):
    bot.add_cog(GunGameCog(bot))


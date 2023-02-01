# Import Needed Libraries
import random as rand

# Define Constants
INVALID_INPUT = "\nYour input was invalid\n"
HENCHMAN_ATTACK_RANGE = [5,21]
HENCHMAN_HEALTH_RANGE = [20,401]
COMMANDER_ATTACK_RANGE = [20,71]
COMMANDER_HEALTH_RANGE = [200,1201]
WARLORD_ATTACK_RANGE = [200,501]
WARLORD_HEALTH_RANGE = [1000,3001]

# Creates a function to write into the file
def file_store(name,score,enemies_found,tower_beat,win):
    # Intialize Variables
    lines = []
    str_message = ""
    score_message = ""
    # Identifies the file needed to be searched and opens it as readable
    file_name = "player_data.txt"
    player_data = open(file_name,"r")
    # Stores all the lines (since just appending makes the format a little weird)
    lines = player_data.readlines()
    player_data.close()
    # Opens the file as writeable
    player_data = open(file_name,"w")
    # Writes a loop to rewrite the lines originally in a document
    for i in range(len(lines)):
        player_data.write(lines[i])
    # Creates a message using the player's name, and other pieces of data
    str_message = "\n"+name
    str_message += " has encountered "+str(enemies_found)+" enemies"
    str_message += " and had beaten "+str(tower_beat)+" towers "
    # Writes a different message depending on whether the player had won or not
    if win:
        str_message += "and defeated the Evil Warlord Zanondorf "
        str_message += "saving the Princess Lelda\n"
    else:
        str_message += "but dying on the journey, another soul lost to the "
        str_message += "Evil Warlord Zanondorf's Empire\n"
    # Creates a message to write the user's score
    score_message = name + "'s Final Score: " + str(score) + "\n"
    # Writes the messages into the document
    player_data.write(str_message)
    player_data.write(score_message)
    player_data.close()
    print("\nProgram End\n")
    input("Click Enter to Close the Program")
    print("\n================================================================"
          +"================================================================"
          +"=======================================")

# Creates a function to validate inputs   
def input_valid(input_list,input_message):
    # Initialize Variables
    user_input = ""
    # Writes an input using the message given
    user_input = input(input_message)
    # Creates a loop to check if the user's input is valid by checking if it is in
    # a list with all valid inputs
    while not input_list.count(user_input):
        # If it is not in the list it will print a message to indicate the input is
        # invalid
        print(INVALID_INPUT)
        # Allows user to input after declaring their input was invalid
        user_input = input(input_message)
    # Returns the user's input (the lines above ensure it is valid)
    return user_input

# Creats a function to create an enemy  
def initialize_enemy(condition, boss_mod):
    # Initialize Variables
    attack_range = 0
    health_range = 0
    enemy_name = ""
    attack = 0
    health = 0
    max_health = 0
    boss = 0
    boss_chance = 0
    # Checks the conditions variable (1 indicates a boss, 0 is just a regular henchman
    if condition == 1:
        # Randomizes variable boss to a number between 1 - 100
        boss = rand.randrange(1,101)
        # Automatically sets the enemy name, attack, and health ranges to a commanders
        attack_range = COMMANDER_ATTACK_RANGE
        health_range = COMMANDER_HEALTH_RANGE
        enemy_name = "Commander"
        # Sets the chance to find the warlord, starts of as 5%, +5% for beating a
        # tower, -1% for every rest, and -1% for every time player runs away
        boss_chance = 95 - boss_mod
        if boss >= boss_chance:
            # Sets the enemy name, attack and health ranges to a warlords 
            attack_range = WARLORD_ATTACK_RANGE
            health_range = WARLORD_HEALTH_RANGE
            enemy_name = "Warlord Zanondorf"
    # If not condition 1 then set the name, attack, and health ranges to a henchmans
    else:
        attack_range = HENCHMAN_ATTACK_RANGE
        health_range = HENCHMAN_HEALTH_RANGE
        enemy_name = "Henchman"
    # Sets attack, and health based on range
    attack = rand.randrange(attack_range[0],attack_range[1])
    health = rand.randrange(health_range[0],health_range[1])
    # Records the max_health (for calculations regarding heals)
    max_health = health
    # Returns a list with the enemy's stats + name
    return[attack,health,enemy_name,max_health]

# Creats a function to deal with the battles in the game
def tower_battle(enemy_data,heals_remain):
    # Intializes variables for the function
    engage = True
    score = 0
    hero_analysis = False
    enemy_analysis = False
    enemy_attack = True
    vunerable = False
    engage = True
    enemy_action = True
    result = []
    enemy_stats = []
    boss_heal = 3
    round_num = 0
    boss = enemy_data[2] != "Henchman"
    valid_inputs = ["1","2","3","4"]
    input_message = "Would you like to Attack[1], Analyze[2], Heal[3] or"
    input_message += " Run Away[4]: "
    warlord_check = enemy_data[2] == "Warlord Zanondorf"
    # Creats a border
    print("================================================================"
          +"================================================================"
          +"=======================================")
    print()
    # Creates a unique message if you find the Warlord
    if warlord_check:
        print("You have found the evil Warlord Zanondorf, defeat him and save"
              + " the princess\n")
    # Creates a message if you found an enemy that isn't the warlord
    else:
        print("You have found an enemy", enemy_data[2])
        print()
    print("================================================================"
          +"================================================================"
          +"=======================================")
    print()
    # While the user is engaged in battle
    while engage:
        # Starts your turn and creates a mini border(condition so it doesn't
        # Repeat your turn when you made an invalid play)
        if enemy_action:
            print("Your Turn")
            print("----------------------------------------------------------------"
          +"----------------------------------------------------------------"
          +"---------------------------------------\n")
        # Sets the enemy's action to be true, turned false when user makes an invalid
        # choice, or the enemy is not engaged
        enemy_action = True
        
        # Loops until you made a valid decision
        choice = input_valid (valid_inputs,input_message)
        print()
        # Sets border as True (used to prevent border when user heals at when they
        # are unable to)
        #border = True
        # If user chose to run away
        if choice == "4":
            # Gives user a 50% chance of successfully running away
            if rand.randrange(0,2):
                # Sends a code to identify that the player had run away 
                result = [False,True,0]
                # Tells user they had ran away
                print("You have successfully ran away")
                # Disengages and prevents enemy action
                engage = False
                enemy_action = False
            else:
                # Tells user they failed to run away
                print("You have failed to escape")
                # Creates a variable vunerable which means user takes increased damage
                vunerable = True
                
        # If user chose to attack
        elif choice == "1":
            # Calculates damage using damage_calc function
            damage = damage_calc(player_stats[0],hero_analysis)
            # If damage = 0, then it is also equal to False, meaning the user had
            # missed, so if user missed tell them they missed
            if not damage:
                print("You missed your attack")
            # Otherwise deal the damage and update the enemy's health
            else:
                print("You dealt",damage,"damage")
            enemy_data[1] -= damage
            # round the health (floats can be weird)
            enemy_data[1] = round(enemy_data[1],1)
            # Check if user's health is below or equal to 0 
            if enemy_data[1]<=0:
                # Tell user they have deafeated the enemy they were fighting
                print()
                print ("You have defeated",enemy_data[2])
                # Giver user a score based on the type of enemy they faced
                if boss:
                    # If the player beat a boss auto set score to 500
                    score = 500
                else:
                    # If user beat a henchman, set score to 50
                    score = 50
                # Sets user's health to 0 (Didn't want any negative numbers)
                enemy_data[1] = 0
                # Stops loop and prevents enemy turn
                enemy_action = False
                engage = False
                # Sets result to indicate user won but didn't beat the warlord yet
                result = [True,False,score]
                # If player had fought (and beat) the warlord
                if warlord_check:
                    # Sets result to indicate player beat the game
                    result = [True,True,1000]

        # If user chose to analyze the enemy
        elif choice == "2":
            # Sets the variable hero analysis to true which increases user's damage
            # output
            hero_analysis = True
            # Tell the user they analyzed the enemy, and the enemy's current health
            print("You analyze the enemy")
            print()
            print(enemy_data[2],"has",enemy_data[1],"health")

        # If user chose to heal themself
        else:
            # Checks if there is any heals remaining
            if heals_remain:
                # Makes the user have one less heal
                heals_remain -= 1
                # Heals the player of 2/3 of their health, then rounds it
                player_stats[1] += player_stats[2]/3
                player_stats[1] = round(player_stats[1],1)
                # Ensures the user's health does not exceed it's maximun value
                if player_stats[1] > player_stats[2]:
                    player_stats[1] = player_stats[2]
                # Tell the user they had healed themself, and how many heals remain
                print("You heal yourself")
                print()
                print("You have",heals_remain,"heals remaining")
            # If user didn't have any heals remaining
            else:
                # Tell the user they ran out of heals
                print("You do not have any heals left")
                # Prevent the enemy frm attacking so the user can do their action
                enemy_action = False
        print()
        
        # Starts enemy turn
        if enemy_action:
            # Creates a border to seperate Player's and Enemy's Turn
            print("================================================================"
          +"================================================================"
          +"=======================================")
            # Uses an input statement so pause until the user wants to continue
            input()
            print("Enemy Turn")
            # Creates enemy mini border
            print("----------------------------------------------------------------"
          +"----------------------------------------------------------------"
          +"---------------------------------------\n")
            # If it is the first round, and the enemy is a boss
            if round_num == 0 and boss:
                # Tell the user that the warlord/commander analyzed them
                if warlord_check:
                    print("The evil Warlord Zandorf analyzes you")
                else:
                    print("The Commander analyses you")
                # Set the enemy analysis variable as true so their damage output is
                # increased
                enemy_analysis = True
                
            # Checks if the enemy is a boss if they have any heals remaining
            # and if their health is below or equal to 1/4 of their max health
            elif boss and boss_heal and enemy_data[1]<=(enemy_data[3]/4):
                # Tells the user that the warlord/commander healed themself
                if warlord_check:
                    print("The evil Warlord Zandorf healed himself")
                else:
                    print("The Commander has healed himself")
                # Increased the boss's current health and makes it so they have 1
                # less boss heal
                enemy_data[1] += enemy_data[3]/3
                boss_heal -= 1

            # If the enemy should attack
            else:
                # Calculated damage using damage calc funtion
                damage = damage_calc(enemy_data[0],enemy_analysis)
                # Increase the damage by 1.5 times if vunerable, then resets vunerable
                damage *= (vunerable)*0.5 + 1
                vunerable = False
                # Round cause floats are weird
                damage = round(damage,1)
                # If the enemy missed let the user know the enemy missed
                if not damage:
                    print(enemy_data[2]+ " missed their attack")
                # If the enemy hit let the user know how much damage they take
                else:
                    print("You take",damage,"damage")
                # Update the user's health and round cause floats are weird
                player_stats[1] -= damage
                player_stats[1] = round(player_stats[1],1)
                # Checks if the user is dead
                if player_stats[1]<=0:
                    # Resets the user's health to 0 to prevent negative numbers
                    player_stats[1] = 0
                    # Tells the user they died, and the enemies's remaining health
                    print("You have died")
                    print(enemy_data[2],"had",enemy_data[1],"health left")
                    # Sets result to indicate a game over loss
                    result = [False,False,0]
                    # Disengages the user
                    engage = False
            print()
            
            # Uses battle_stats to show player's current health and a message
            # to indicate the enemies health range
            battle_stats(player_stats[1],enemy_data)
        # Increases the round number
        round_num += enemy_action
    # Returns result once battle is over to indicate what happen
    return [result[0],result[1],result[2],heals_remain]

# Creates a function to state the status of you and the enemy
def battle_stats(player_health,enemy_data):
    # Sets variable names so its easier to comprehend
    enemy_health = enemy_data[1]
    enemy_name = enemy_data[2]
    enemy_max_health = enemy_data[3]
    # Checks if both player's are alive
    if enemy_health >0 and player_health >0:
        # Creates border 
        print("================================================================"
              +"================================================================"
              +"=======================================")
        # Wait till user clicks enter
        input()
        # identifies the section as the status report
        print("Status Report")
        print("----------------------------------------------------------------"
          +"----------------------------------------------------------------"
          +"---------------------------------------\n")
        # Tells user their current health
        print("Your Health: "+str(player_health)+"/"+str(player_stats[2]))
        print()
        # Creates a message depending on the enemies's health range
        if enemy_health/enemy_max_health >= 0.5: # greater than 50%
            print("The",enemy_name,"looks unfazed by you")
        elif enemy_health/enemy_max_health >= 0.2: # 49% - 20%
            print("The",enemy_name,"looks visibly damaged and unnerved")
        elif enemy_health/enemy_max_health >= 0.1: #19% - 10%
            print("The",enemy_name,"looks very exhausted and scared")
        else: # Less than 10%
            print("The",enemy_name,"looks like they might collapse at any second")
        print()
        # Creates Border
        print("================================================================"
          +"================================================================"
          +"=======================================")
        input()

# Creates a function to calculate damage being dealt   
def damage_calc(attack,analysis):
    damage = 0
    # Creates a damage multiplier between 0.5 to 1.5
    damage_roll = (rand.randrange(5,16)/10)
    # Creates a crit change of 10%
    crit_roll = (rand.randrange(1,11)>9)+1
    # Creates a miss chance of 5%
    hit = (rand.randrange(1,21)!=1)
    # Checks if the target has been analyzed (double damage)
    analyzed = analysis + 1
    # Calculates damaged by applying multipliers to the
    # attacker's attack stat
    damage = attack*damage_roll*crit_roll*hit*analyzed
    # Rounds cause floats are weird
    damage = round(damage,1)
    # Sends the damage over
    return damage
    
def main():
    # Globalizes variable player_stats
    global player_stats
    # Intializes Variables
    over = False
    tower_beat = 0
    rests_total = 0
    run_num = 0
    score = 0
    enemies_found = 0
    name = ""
    direction = ""
    battle = True
    valid_inputs = []
    player_stats = [50,1,1]
    enemy_remain = 0
    heals_remain = 5
    # Lets the user start the game by clicking enter
    print("Please full screen the command line\n")
    input("Click Enter to Begin")
    # Creates a border
    print("\n================================================================"
          +"================================================================"
          +"=======================================")
    print("\nProgram Start\n") # States the program started
    # Creates another border
    print("================================================================"
          +"================================================================"
          +"=======================================\n")
    # Makes a heading for Lore/Beginning
    print("Lore/Start")
    print("----------------------------------------------------------------"
          +"----------------------------------------------------------------"
          +"---------------------------------------\n")
    #Prints lore for the game
    print("You are a knight trying to save Princess Lelda, who got kidnapped "
          +"by the Evil Warlord Zanondorf. Raid the towers in Zanondorf's"
          +" territories in search of Zanondorf to\nsave your Princess.\n")
    # Lets the user start the game by clicking enter
    input("Click Enter to Begin Your Journey")
    # Allow user to input their name
    name = input("\nWhat is your name young knight: ")
    # Give a generic message before the user goes on their jouney
    print()
    print(name, ",it's all up to you, go and save Princess Lelda\n")
    print("================================================================"
          +"================================================================"
          +"=======================================")
    #Sets up user to input the tower they travel to
    while not over:
        print()
        valid_inputs = ["1","2","3"]
        input_message = "You see three towers in the distance,"
        input_message += " Which tower do you travel to [1/2/3]: "
        tower = input_valid (valid_inputs,input_message)
        # Sets battle as true
        battle = True
        # Creates a random number of enemies for the tower (1 - 6)
        enemy_remain = rand.randrange(1,6)
        # Sets the heals for the tower as 5 (only 5 heals per tower)
        heals_remain = 5
        # While the user in the battle
        print()
        while battle:
            # Intialize the enemy's stats using initialize_enemy function
            enemy_stats = initialize_enemy(0,((tower_beat*5)-rests_total-
                                                    run_num))
            # If there is 1 enemy remaining make him a boss
            if enemy_remain == 1:
                enemy_stats = initialize_enemy(1,((tower_beat*5)-rests_total-
                                                  run_num))
            # Gets the outcome + score allocated from the function
            # tower_battle
            battle_data = (tower_battle(enemy_stats,heals_remain))
            # Creates a border ()
            print("================================================================"
                +"================================================================"
                +"=======================================")
            print()
            # Increases the number of enemies found, and removes an
            # enemy remaining and saves remaining heals
            enemies_found += 1
            enemy_remain -= 1
            heals_remain = battle_data[3]
            # If the user ran away
            if not battle_data[0] and battle_data[1]:
                # stop the battle
                battle = False
                # Increase the number of times ran
                run_num += 1
                # Show's user's current health
                print("Health:",str(player_stats[1])+"/"+str(player_stats[2]))

            # If user has won, and no enemies remaining
            elif enemy_remain == 0 and battle_data[0]:
                # stop the battle
                battle = False
                # increase the number of towers beat
                tower_beat += 1
                # Update the stats (attack increases by 25,
                # health by 200)
                player_stats[0] += 25
                player_stats[1] += 200
                player_stats[2] += 200
                print("Health:",str(player_stats[1])+"/"+str(player_stats[2]))

            # If user beat an enemy (and there are still enemies
            # cause it uses elif)
            elif battle_data[0] and not battle_data[1]:
                # Show how many enemies remain
                print("Enemies Remain:", enemy_remain)

            print()
            
            # If user died
            if not battle_data[0] and not battle_data[1]:
                # Tell the user Game Over (Loss)
                print("You have failed to save the princess, GAME OVER")
                # Stops Loops
                over = True
                battle = False
                
            # Updates the score, 1000 for warlord, 500 for commander
            # 50 for henchman
            score += battle_data[2]

        # If user beat the warlord
        if battle_data[0] and battle_data[1]:
            # Tell the user Game Over (Win)
            print("You have defeated the evil Zanondorf and saved the princess."
                  + " Congratulations on saving the kingdom, GAME OVER")
            # Stops Loops
            over = True
            battle = False
        # If the game is not over
        if not over:
            # Sets up and ask user if they want rest
            valid_inputs = ["Y","N"]
            input_message = "Would you like to rest after battling that tower?"
            input_message += " [Y/N]: "
            rest = input_valid (valid_inputs,input_message)
            # If user wants to rest
            if rest == "Y":
                # Increase rest total and reset health to max
                rests_total += 1
                player_stats[1] = player_stats[2]
        # Create a border
        print()
        print("================================================================"
          +"================================================================"
          +"=======================================")
    # Writes a story about the game into a file using function
    # file_store
    file_store(name,score,enemies_found,tower_beat,battle_data[0])
main()

# class TerrariaModifier:


class ProbalityGenerator:
    # fail and success strings are predefined here so the system detecting what is valid input can be changed with ease
    fail_string = "f"
    success_string = "s"
    def __init__(self, game_name):
        self.game_name = game_name
        self.printGame() # Print the name of the selected mode

    '''
    Simple function that prints the current game that this object is calculating the odds for
    - This object will be able to change name in the future based on strategy
    '''
    def printGame(self):
        print("The current game selected is " + self.game_name)

    '''
    Will initiate by prompt the user for percentage and calls the function that calculates the odds.
    '''
    def askForOdds(self):
        print("What is the chance of this role to be successful? (The input is looking for the percentage - [x]%)")
        while True:
            try: 
                number_odd = float(input("Enter here: "))
                break
            except ValueError:
                print("Invalid input")
        self.__calculateOdds(number_odd)

    '''
    Calculates the odds - to do this it will call a helper that asks for the number of times and prints the final odds
    '''
    def __calculateOdds(self, number_odd):
        invalid_input = True
        while invalid_input:
            mode = input("Enter whether Succeeded or Failed [S/F]: ").lower() # lowercase to handle both upper and lower cases
            if(mode.startswith(self.success_string) or mode.startswith(self.fail_string)): # startswith in case the user types out the full word
                invalid_input = False
            else:
                print("INVALID INPUT")
        odds = self.__calculateConsecutiveOdds(number_odd, mode)
        final_odds = self.__askForTimes(odds)
        print(f"Your odds were: {round(final_odds * 100,2)}%") # rounds to 2 decimals points
        

    '''
    This handles whether users is basing on fails or success roles
    '''
    def __calculateConsecutiveOdds(self, odds, mode):
        if(mode.startswith(self.success_string)):
            percentage_in_100 = (odds / 100)
        elif(mode.startswith(self.fail_string)):
            percentage_in_100 = 1 - (odds / 100)
        return percentage_in_100
    '''
    Prompts the user the number of times the user has rolled on those odds and calculate based on the given input.
    '''
    def __askForTimes(self, odds):
        while True:
            try: 
                number_of = int(input("Enter the number of times (in a row) this occured: "))
                break
            except ValueError:
                print("Invalid input")
        return odds ** number_of # to the power of
    
knownGames = ["Terraria"]
newTerraria = ProbalityGenerator("Terraria")
newTerraria.askForOdds()
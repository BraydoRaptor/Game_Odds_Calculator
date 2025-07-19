from abc import ABC, abstractmethod
import math

# Terraria Exclusive Statements
TerrariaOddsExplanation = ["The odds in terraria are rolled in the following cases: ", "Enemy or Boss Rolls", "Fishing", "Certain Events spawning within a world", "\n", 
                           "There is an additional influence of a standard percentage chance for these events to occur, this is known as luck.", 
                           "Without any luck influences, you have a luck value of 0.0 meaning that standard odds don't change, however",
                            "your luck be decreased or increased in various circumstances", "Some of the positive influences are Potions, Accessories, Torches", 
                            "Ladybugs are a source of both negative and positive, so for the following calculations you need to estimate how much luck you had on average (usually 0.0)"]
TerrariaDisclamer = "It is important to note that the influence of luck on your odds is random, so a standardised value is used"

'''
    Parent Class that is the basis of all game modifiers as it may change the algorithm to adjust the odds
'''
class GameOddsModifier(ABC):
    @abstractmethod
    def adjustOdds(self, current_odds:float):
        pass

'''
    Terraria Class that has a luck influence
'''
class TerrariaModifier(GameOddsModifier):
    '''
        This will set of the chains
        it also returns the new odds based on a formula on your luck number
    '''
    def adjustOdds(self, current_odds:float) -> float:
        self.__handleExplanation()
        luck = self.__promptLuckAmount()
        self.__printdisclaimer(luck)
        rounded_odds_n = math.floor(100/current_odds) # -> n is based on the chance in the form of 1/n
        if luck > 0:
            return (self.__summation(rounded_odds_n/2, rounded_odds_n-1) / (rounded_odds_n / 2) * luck + 1/rounded_odds_n * (1 - luck))
        elif luck < 0:
            return (self.__summation(rounded_odds_n, 2*rounded_odds_n-1) / (rounded_odds_n / 2) * abs(luck) + 1/rounded_odds_n * (1 - abs(luck)))
        else:
            return current_odds/100
    '''
        This is a function to add for a summation (greek used in statistics) formula
    '''
    def __summation(self, lower_bound:float, upper_bound:float) -> float:
        total = 0
        for k in range(math.floor(lower_bound), math.floor(upper_bound)):
            total += 1/k
        return total
    '''
        helper to print out what needs to be explaned about terraria luck
    '''
    def __handleExplanation(self) -> None:
        for sentence in TerrariaOddsExplanation:
            print(f"| {sentence}")
    '''
        prompts for a known luck value
    '''
    def __promptLuckAmount(self) -> float:
        while True:
            try: 
                number_luck = float(input("Enter your luck here (-/+): "))
                break
            except ValueError:
                print("Invalid luck, luck needs to be a number")
        return number_luck
    def __printdisclaimer(self, luck:float) -> None:
        print(f"== {TerrariaDisclamer}, the luck you inputted was {luck} ==")

class MinecraftModifier(GameOddsModifier):
    '''
        This will set of the chains
        it also returns the new odds based on a formula on your luck number
    '''

    # Minecraft Exclusive Statements
    MinecraftOddsExplanation = ["Minecraft has mob drops and fishing as their two primary rng rolling mechanics", "Looting, which has three levels can affect the chance of rolls as well as increase the number of rolls"]
    MinecraftDisclamer = "Minecraft has so many items, especially common and uncommon mod drops, fishing is completely different and depends on different lure mechanics which are currently not explored"
    rare_string = "R"
    common_string = "C"


    def adjustOdds(self, current_odds:float) -> float:
        self.__handleExplanation()
        lootingNumber = self.__promptForLooting("looting")
        self.__printdisclaimer(lootingNumber)
        user_item_type = self.__promptItemType()
        if(user_item_type == self.rare_string):
            influence_number = 1
            return current_odds / 100 + lootingNumber * influence_number
        elif(user_item_type == self.common_string):
            current_odds = self.__handleCommonDrops(lootingNumber, current_odds)
            return current_odds

        return current_odds
    '''
        Prompts for looting 0-3 based on a string
    '''
    def __promptForLooting(self, change_cond:str) -> int:
        user_looting = 0
        min_looting = 0
        max_looting = 3
        while user_looting >= min_looting and user_looting <= max_looting:
            try: 
                user_looting = int(input(f"Enter the number of {change_cond} you had: "))
                break
            except ValueError:
                print(f"Invalid input, enter a number between {min_looting} and {max_looting}")
        return user_looting
    '''
        helper to print out what needs to be explaned about minecraft looting
    '''
    def __handleExplanation(self) -> None:
        for sentence in self.MinecraftOddsExplanation:
            print(f"| {sentence}")

    '''
        handles the martix boost of odds that apply with looting using a reference matrix (or a list of dictionaries)
    '''

    def __handleCommonDrops(self,looting:int, current_odds:float) -> int:
        current_odds = current_odds /100 # assume success
        loot_alteration_matrix = [{0:0.5,1:0.5,2:0,3:0}, {0:0.25,1:0.5,2:0.25,3:0}, {0:0.17,1:0.33,2:0.33,3:0.17}]
        index = 0
        current_drops = self.__promptForLooting("average drops")
        while index < len(loot_alteration_matrix):
            if(looting == index+1):
                for num_modifier in loot_alteration_matrix[index]:
                    if(num_modifier == current_drops):
                        return current_odds + current_odds*loot_alteration_matrix[index][num_modifier]
            index=index+1
        return 0 # not possible odds
                
                
    '''
        prompts for the type of mod drop which will differ based on looting
    '''
    def __promptItemType(self) -> str:
        
        invalid_input = True
        while invalid_input:
            type_item = input(f"Enter whether {self.common_string} (common or uncommon drops) or {self.rare_string} (rare drops): ").upper() # uppercase to handle both upper and lower cases
            if(type_item.startswith(self.common_string) or type_item.startswith(self.rare_string)): # startswith in case the user types out the full word
                invalid_input = False
            else:
                print("INVALID INPUT")
        return type_item
    def __printdisclaimer(self, looting:int) -> None:
        print(f"== {self.MinecraftDisclamer}, the looting you inputted was {looting} ==")


class ProbabilityGenerator():
    # fail and success strings are predefined here so the system detecting what is valid input can be changed with ease
    fail_string = "f"
    success_string = "s"
    def __init__(self, game_name:str, modifier: GameOddsModifier):
        self._modifier = modifier
        self.game_name = game_name
        self.printGame() # Print the name of the selected mode
    @property
    def modifier(self) -> GameOddsModifier:
        return self._modifier
    @modifier.setter
    def modifier(self, modifier:GameOddsModifier) -> None:
        self._modifier = modifier

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
    def __calculateOdds(self, number_odd:float):
        invalid_input = True
        while invalid_input:
            mode = input("Enter whether Succeeded or Failed [S/F]: ").lower() # lowercase to handle both upper and lower cases
            if(mode.startswith(self.success_string) or mode.startswith(self.fail_string)): # startswith in case the user types out the full word
                invalid_input = False
            else:
                print("INVALID INPUT")
        
        odds = self.__calculateModeOfOdds(self._modifier.adjustOdds(number_odd), mode) # n 10 succeed 90
        final_odds = self.__calculateFinalOdds(odds, self.__askForTimes())
        print(f"Your odds were: {round(final_odds * 100,2)}%") # rounds to 2 decimals points
    
    '''
    This handles whether users is basing on fails or success roles
    '''
    def __calculateModeOfOdds(self, odds:float, mode:str):
        if(mode.startswith(self.success_string)): # 2 -> 2% N=50  20 -> 20% N=5
            odds_100 = odds
        elif(mode.startswith(self.fail_string)): # 2 -> 2% N=1/(98/100) 20 -> 20% N= 0.8
            odds_100 = 1-odds
        return odds_100

    '''
    Prompts the user the number of times the user has rolled on those odds and calculate based on the given input.
    '''
    def __askForTimes(self) -> int:
        while True:
            try: 
                number_of = int(input("Enter the number of times (in a row) this occured: "))
                break
            except ValueError:
                print("Invalid input")
        return number_of
    def __calculateFinalOdds(self, odds:float, times:int) -> float:
        return odds ** times # to the power of
if __name__ == "__main__":  
    knownGames = ["terraria", "minecraft"]
    print("The current known games with odd modifiers are the following:")
    for _index, _game in enumerate(knownGames):
        print(f"{_index}: {_game}")
    invalid_input = True
    while invalid_input:
        game = input("Which game would you like to choose? ").lower()
        if game in knownGames:
            invalid_input = False
        else:
            print("INVALID INPUT, please reference the available games")
    newGenerator = ProbabilityGenerator(game, TerrariaModifier())
    match game:
        case "terraria":  
            newGenerator.modifier = TerrariaModifier()
            newGenerator.askForOdds() # Starts the chain of events in the program
        case "minecraft":
            newGenerator.modifier = MinecraftModifier()
            newGenerator.askForOdds() # Starts the chain of events in the program

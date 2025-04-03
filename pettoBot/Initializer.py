import Personalities, Actions, Food

class Initializer:
    
    def __init__(self):
        with open('pettoBot/personalities.txt', 'r') as file:
            self.personalities = []
            for line in file:
                pers = line.split("/")
                personality = Personalities.Personalities(pers[0], pers[1], pers[2], pers[3], pers[4], pers[5], pers[6], pers[7], pers[8], pers[9], pers[10], pers[11], pers[12])
                self.personalities.append(personality)

        with open('pettoBot/food.txt', 'r') as file:
            self.food = []
            for line in file:
                fd = line.split()
                self.food.append(Food.Food(fd[0], fd[1], fd[2]))
                
        with open('pettoBot/actions.txt', 'r') as file:
            self.actions = []
            for line in file:
                ac = line.split()
                self.actions.append(Actions.Actions(ac[0], ac[1], ac[2], ac[3], ac[4]))
        
        self.picturelist = open("pettoBot/pictures.txt").readlines()
    
    def get_personalities(self):
        return self.personalities
    
    def get_food(self):
        return self.food
    
    def get_actions(self):
        return self.actions
    
    def get_pictures(self):
        return self.picturelist
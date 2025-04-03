import unittest
from unittest.mock import MagicMock, patch
import time
import Command_logic, Initializer, Personalities, Actions


command_logic = Command_logic.Command_logic([], [], Initializer.Initializer(), MagicMock())


## TEST 1

@patch('Initializer.Initializer.get_pictures')
@patch('Initializer.Initializer.get_personalities')
@patch('Command_logic.Command_logic.hasadopted')
class TestAdopt(unittest.TestCase):
    
    def test_adopt_valid(self, mock1, mock2, mock3):
        mock1.return_value = False
        mock2.return_value = [Personalities.Personalities('', '', '', '', '', '', '', '', '', '', '', 'answer', '')]
        mock3.return_value = ['']
        self.assertEqual(command_logic.adopt("user", "M"), "PettoBot: Congratulations! You successfully adopted a new pet!\n\nJordy: answer")
    
    def test_adopt_invalid(self, mock1, mock2, mock3):
        mock1.return_value = True
        mock2.return_value = [Personalities.Personalities('', '', '', '', '', '', '', '', '', '', '', 'answer', '')]
        mock3.return_value = ['']
        self.assertEqual(command_logic.adopt("user", "M"), "PettoBot: Oops! Looks like you already have a pet.")


## TEST 2

@patch('Command_logic.Command_logic.hasadopted')
class TestChangeName(unittest.TestCase):
    
    def test_change_name_valid(self, mock1):
        mock1.return_value = True
        self.assertEqual(command_logic.change_name("user", "Martin"), "PettoBot: Alright! Your pet's name will now be Martin")
    
    def test_change_name_invalid_name(self, mock1):
        mock1.return_value = True
        self.assertEqual(command_logic.change_name("user", "&5.:uB/Nr=CD+UY_YRH/Mr+B]N/ga&$}8=jX?N)48y/FM8i8VW0jCTa@RmQ-wip,G5J#zK=VTbwexRXuwF#_eqYiC5vy4fhr4zSvp"), "PettoBot: Whoops, looks like the name you suggested is too long!")
    
    def test_change_name_invalid_pet(self, mock1):
        mock1.return_value = False
        self.assertEqual(command_logic.change_name("user", "Martin"), "PettoBot: You do not have a pet!")


## TEST 3

@patch('Command_logic.Command_logic.hasadopted')
class TestActionValid(unittest.TestCase):
    def test_action_valid_invalid(self, mock1):
        mock1.return_value = False
        command_logic.db.select.return_value = [["Martin", time.time(), 0]]
        self.assertEqual(command_logic.action_valid("user", Actions.Actions("pet", 1, 0, 0, 2)), "PettoBot: You do not have a pet!")
    
    def test_action_valid_valid(self, mock1):
        mock1.return_value = True
        command_logic.db.select.return_value = [["Martin", 0, 0]]
        self.assertIsNone(command_logic.action_valid("user", Actions.Actions("pet", 1, 0, 0, 2)))
    
    def test_action_valid_pet(self, mock1):
        mock1.return_value = True
        command_logic.db.select.return_value = [["Martin", time.time(), 0]]
        self.assertEqual(command_logic.action_valid("user", Actions.Actions("pet", 1, 0, 0, 2)), "PettoBot: You have already petted Martin. Wait 2 minutes to pet again.")
    
    def test_action_valid_walk(self, mock1):
        mock1.return_value = True
        command_logic.db.select.return_value = [["Martin", time.time(), 0]]
        self.assertEqual(command_logic.action_valid("user", Actions.Actions("walk", 1, 0, 0, 3)), "PettoBot: You have already walked Martin. Wait 3 minutes to walk again.")
        
    def test_action_valid_train(self, mock1):
        mock1.return_value = True
        command_logic.db.select.return_value = [["Martin", time.time(), 0]]
        self.assertEqual(command_logic.action_valid("user", Actions.Actions("train", 0, 10, 0, 5)), "PettoBot: You have already trained Martin. Wait 5 minutes to train again.")
        
    def test_action_valid_battle_valid(self, mock1):
        mock1.return_value = True
        command_logic.db.select.return_value = [["Martin", time.time(), 4]]
        self.assertEqual(command_logic.action_valid("user", Actions.Actions("battle", 0, 0, 3, 10)), "PettoBot: Martin has already battled. Wait 10 minutes to battle again.")
    
    def test_action_valid_battle_invalid(self, mock1):
        mock1.return_value = True
        command_logic.db.select.return_value = [["Martin", 0, 0]]
        self.assertEqual(command_logic.action_valid("user", Actions.Actions("battle", 0, 0, 3, 10)), "PettoBot: Martin does not have enough love points for battle.")


## TEST 4

@patch('random.choice')
class TestShowLove(unittest.TestCase):
    def test_show_love_pet(self, mock1):
        mock1.return_value = "ok"
        command_logic.db.select.return_value = [[0, "Martin", "Aggressive", ""]]
        self.assertEqual(command_logic.show_love("user", Actions.Actions("pet", 1, 0, 0, 2)), ("Martin", "ok", "", 1))
    
    def test_show_love_walk(self, mock1):
        mock1.return_value = "ok"
        command_logic.db.select.return_value = [[0, "Martin", "Aggressive", ""]]
        self.assertEqual(command_logic.show_love("user", Actions.Actions("walk", 1, 0, 0, 3)), ("Martin", "ok", "", 1))


## TEST 5

class TestTrain(unittest.TestCase):
    def test_train_valid(self):
        command_logic.db.select.return_value = [[0, "Martin", "Aggressive", ""]]
        self.assertEqual(command_logic.train("user", Actions.Actions("train", 0, 10, 0, 5)), ("Martin", "Oh yeah, im liftin' straight up metal! Beware, enemies of mine!", ""))


## TEST 6

class TestBattle(unittest.TestCase):
    def test_battle_valid(self):
        command_logic.db.select.return_value = [["Martin", "", "Aggressive", 2, 0, 0, 5]]
        command_logic.db.select.return_value = [["Martinette", "", "Gloomy", 1, 0, 0, 5]]
        results = command_logic.battle("user1", "user2")
        self.assertEqual(results[0].name, "user1")


## TEST 7

@patch('Initializer.Initializer.get_personalities')
class TestPickPersonality(unittest.TestCase):
    def test_pickPersonality_valid(self, mock1):
        pers1 = Personalities.Personalities("name1", "", "", "", "", "", "", "", "", "", "", "", "")
        pers2 = Personalities.Personalities("name2", "", "", "", "", "", "", "", "", "", "", "", "")
        pers3 = Personalities.Personalities("name3", "", "", "", "", "", "", "", "", "", "", "", "")
        mock1.return_value = [pers1, pers2, pers3]
        self.assertEqual(command_logic.pickPersonality("name1"), pers1)
        
    def test_pickPersonality_invalid(self, mock1):
        pers1 = Personalities.Personalities("name1", "", "", "", "", "", "", "", "", "", "", "", "")
        pers2 = Personalities.Personalities("name2", "", "", "", "", "", "", "", "", "", "", "", "")
        pers3 = Personalities.Personalities("name3", "", "", "", "", "", "", "", "", "", "", "", "")
        mock1.return_value = [pers1, pers2, pers3]
        self.assertEqual(command_logic.pickPersonality("name"), None)


## TEST 8

class TestHasAdopted(unittest.TestCase):
    def test_hasAdopted_valid(self):
        command_logic.db.select.return_value = [["user1"], ["user2"], ["user3"]]
        self.assertEqual(command_logic.hasadopted("user2"), True)
    
    def test_hasAdopted_invalid(self):
        command_logic.db.select.return_value = [["user1"], ["user2"], ["user3"]]
        self.assertEqual(command_logic.hasadopted("user"), False)
        

## TEST 9

class TestPickGender(unittest.TestCase):
    def test_pickGender_valid(self):
        self.assertEqual(command_logic.pickGender("M"), "Male")
        self.assertEqual(command_logic.pickGender("F"), "Female")
        self.assertEqual(command_logic.pickGender("N"), "Neutral")
    
    def test_pickGender_invalid(self):
        self.assertEqual(command_logic.pickGender("L"), None)


## TEST 10

class TestPickPastForm(unittest.TestCase):
    def test_pickPastForm_valid(self):
        act1 = Actions.Actions("pet", "", "", "", "")
        act2 = Actions.Actions("walk", "", "", "", "")
        act3 = Actions.Actions("train", "", "", "", "")
        act4 = Actions.Actions("battle", "", "", "", "")
        self.assertEqual(command_logic.pickPastForm(act1), "petted")
        self.assertEqual(command_logic.pickPastForm(act2), "walked")
        self.assertEqual(command_logic.pickPastForm(act3), "trained")
        self.assertEqual(command_logic.pickPastForm(act4), "battled")
    



if __name__ == '__main__':
    unittest.main()




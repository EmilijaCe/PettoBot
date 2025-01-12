import unittest



def change_name(user, name):
    if (len(name) > 100):
        return "PettoBot: Whoops, looks like the name you suggested is too long!"
    
    return f"PettoBot: Alright! Your pet's name will now be {name}"



class TestChangeName(unittest.TestCase):
    def test_change_name_valid(self):
        self.assertEqual(change_name("user", "Martin"), "PettoBot: Alright! Your pet's name will now be Martin")
    
    def test_change_name_invalid(self):
        self.assertEqual(change_name("user", "&5.:uB/Nr=CD+UY_YRH/Mr+B]N/ga&$}8=jX?N)48y/FM8i8VW0jCTa@RmQ-wip,G5J#zK=VTbwexRXuwF#_eqYiC5vy4fhr4zSvp"), "PettoBot: Whoops, looks like the name you suggested is too long!")




if __name__ == '__main__':
    unittest.main()




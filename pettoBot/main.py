import Command_logic
import Initializer
import Commands
import Database
import configs


token = configs.settings['token']
defaultItems = ["name", "love_points", "strength_points", "coins", "battle_wins", "battle_losses", "pet_time", "walk_time", "train_time", "battle_time", "tookcoin", "hasloved"]
defaultValues = ["Jordy", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
HOST = configs.settings['host']
MASTER_KEY = configs.settings['master_key']
DATABASE_ID = configs.settings['database_id']
CONTAINER_ID = configs.settings['container_id']


database = Database.Database(HOST, MASTER_KEY, DATABASE_ID, CONTAINER_ID)
command_logic = Command_logic.Command_logic(defaultItems, defaultValues, Initializer.Initializer(), database)
Commands.__init__(command_logic, token, Initializer.Initializer())



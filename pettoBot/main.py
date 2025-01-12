import time
import discord
import random
import mysql.connector
from discord.ui import Button, View
import Personalities, Actions, Food
import Database, Commands


'''
things to improve:
1. find out how to run two tasks at the same time -> schedule times to reset daily coins and love points
2. set environment variables for database and token
3. fix battle buttons: add timeout, make them available only for the opponent (no one else can press them)
4. extend the program: add food options, more personalities, explore the possibility of having multiple pets
5. draw pictures for pets and bot's profile
6. (if there is a possibility) find a way to modify pictures for commands (add elements, make a gif, etc.)
7. find a better way to store personality comments (for example, a table)
8. use a different database to store data
'''
from util import *
from time import sleep

game = ZombieSurvival()

while True:
    end = False
    while not end:
        game.generate_zombies()
        game.step()
        game.blit()
        end = game.check_collision()
        sleep(0.01)
        if end:
            print("SCORE:", game.points)
            game.reset()
import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
from dataclasses import dataclass
import time
from threading import Thread
import random

HEIGHT = 6
DEPTH = 3
BLOCK_TYPE = block.STONE_BRICK.id

animating_blocks = []

@dataclass()
class MovingBlock:
    current_position: vec3.Vec3()
    target_position: vec3.Vec3()


def get_logo_cooridnates(start_position):

    coordinates = []

    # set the position to the start position + the height of the logo
    position = vec3.Vec3(start_position.x, start_position.y + HEIGHT, start_position.z)

    # read the file and loop for each line
    f = open("logo.txt", "r")
    for line in f.readlines():
        
        # loop one for each amount of depth
        for z in range(0, DEPTH):

            # read each character in the line
            for character in list(line):

                # if 'X' then this is a block
                if character == 'X':
                    coordinates.append(vec3.Vec3(position.x, position.y, position.z))
                
                # increment the X position
                position.x = position.x + 1

            # reset x and move one back
            position.x = start_position.x
            position.z = position.z + 1

        # reset the depth
        position.z = start_position.z 

        # move down a line
        position.y = position.y - 1 

    # sort t he coordinates so the lowest ones are always first
    coordinates = sorted(coordinates, key= lambda coordinate : coordinate.y, reverse=True)

    return coordinates


def populate_animation_blocks(feeder=[], delay=1, random_size=10):
 
    while len(feeder) > 0:

        if len(feeder) > random_size:
            index = len(feeder) - random.randint(0, random_size - 1)
            # print(f'index: { index } of { len(feeder) }')
            animating_blocks.append(feeder.pop(index - 1))
        else:
            animating_blocks.append(feeder.pop())

        time.sleep(delay)


def animate_blocks(delay=1):

    mc = minecraft.Minecraft.create(address="minecraft")

    while len(animating_blocks) > 0:

        for animating_block in animating_blocks:

            # has the animation finished?
            if animating_block.current_position == animating_block.target_position:

                # stop animating this block
                animating_blocks.remove(animating_block)
                # print(f'removing { animating_block }')

            else:
                # calculate next block position
                next_position = vec3.Vec3(animating_block.current_position.x, animating_block.current_position.y - 1, animating_block.current_position.z)

                # draw the block at the next position
                mc.setBlock(next_position.x, next_position.y, next_position.z, BLOCK_TYPE)

                # replace the block at the current position with air
                mc.setBlock(animating_block.current_position.x, animating_block.current_position.y, animating_block.current_position.z, block.AIR.id)

                # update the current position with the next position
                animating_block.current_position = next_position

        time.sleep(delay)

    print("Animation Finished")


def make_logo(coordinates):
    mc = minecraft.Minecraft.create(address="minecraft")

    for coordinate in coordinates:
        mc.setBlock(coordinate.x, coordinate.y, coordinate.z, BLOCK_TYPE)


def make_logo_rain(coordinates, height):

    blocks = []
    speed = 0.09

    # populate the blocks
    for coordinate in coordinates:
        blocks.append(MovingBlock(current_position=vec3.Vec3(coordinate.x, height, coordinate.z), target_position=coordinate))

    # start feeder process
    Thread(target=populate_animation_blocks, args=(blocks, speed,)).start()

    time.sleep(1)

    # start rain ainmation process
    print("making it rain...")
    Thread(target=animate_blocks, args=(speed,)).start()


def clear_logo(coordinates):
    for coordinate in get_logo_cooridnates(start_position):
        mc.setBlock(coordinate.x, coordinate.y, coordinate.z, block.AIR.id)


mc = minecraft.Minecraft.create(address="minecraft")

start_position = mc.player.getTilePos()

# get logo coordinates
logo_coordinates = get_logo_cooridnates(start_position)

# draw static logo
# make_logo(logo_coordinates)

# make it rain
make_logo_rain(logo_coordinates, start_position.y + 10)

# clean up
time.sleep(20)
clear_logo(logo_coordinates)

import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.vec3 as vec3
from skyscraper import Skyscraper
from random import randrange

mc = minecraft.Minecraft.create(address="minecraft")

# make lists of the things that we can change
floors_numbers = range(20, 45)
frame_colours = [0, 7, 8, 15] 
widths = range(16, 26, 2)

# create some random skyscrapers
skyscrapers = []
for skyscraper_number in range(10):
    skyscrapers.append(Skyscraper(
        number_of_floors=floors_numbers[randrange(0, len(floors_numbers))],
        width=widths[randrange(0, len(widths))], 
        structure_brick_colour=frame_colours[randrange(0, len(frame_colours))]))

x_building_spacer = 10
z_building_spacer = 10
player_position = mc.player.getTilePos()

# build first building at player position + spacer
x = player_position.x + x_building_spacer
z = player_position.z

skyscraper_number = 0
for skyscraper in skyscrapers:
    
    # on alternative buildings...
    if skyscraper_number % 2 == 0:
        # move to next x position to build the next skyscraper
        x = x + skyscraper.width + x_building_spacer

        # move the z to the left of the plaer position
        z = player_position.z - z_building_spacer - skyscraper.width
    else:
        # move the z to the right of the plaer position
        z = player_position.z + z_building_spacer

    # build the skyscraper at the ground height
    skyscraper.build(mc, position=vec3.Vec3(x, mc.getHeight(x, z), z))

    skyscraper_number = skyscraper_number + 1
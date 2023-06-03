import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import math
from random import randrange
from buidings.skyscrapers.skyscraper import Skyscraper
from games.arena import PittedArena, Arena


class Cityscape:

    arena = None

    def __init__(self, arena):
        self.arena = arena

   
    def build(self, mc):

        floors_numbers = range(10, 20)
        frame_colours = [0, 7, 8, 15, 4, 3, 14, 0, 7, 8, 15] 

        building_width = 15
        building_spacer = 8
        building_gap = building_width + building_spacer

        # work out the number of buildings needed
        number_of_x_buildings = math.ceil(arena.width / building_gap) + 2
        number_of_y_buildings = math.ceil(arena.length / building_gap) + 2
        print(f"Building city scape of { number_of_x_buildings } by { number_of_y_buildings } buildings")

        # work out the length and width of the cityscape
        city_scape_width = (building_width * number_of_x_buildings) + (building_spacer * (number_of_x_buildings - 1))
        city_scape_length = (building_width * number_of_y_buildings) + (building_spacer * (number_of_y_buildings - 1))

        # work out the start position based on the centre of the arena
        city_scape_start_position = arena.position - vec3.Vec3((city_scape_width / 2), arena.position.y, (city_scape_length / 2))

        # clear the entire area
        mc.setBlocks(
            city_scape_start_position.x - building_spacer, 
            city_scape_start_position.y, 
            city_scape_start_position.z - building_spacer, 
            city_scape_start_position.x + city_scape_width + building_spacer, 
            city_scape_start_position.y + (floors_numbers[-1] * 5), 
            city_scape_start_position.z + city_scape_length + building_spacer, 
            block.AIR.id)

        # build a large base for the city
        mc.setBlocks(
            city_scape_start_position.x - building_spacer, 
            city_scape_start_position.y, 
            city_scape_start_position.z - building_spacer, 
            city_scape_start_position.x + city_scape_width + building_spacer, 
            city_scape_start_position.y, 
            city_scape_start_position.z + city_scape_length + building_spacer, 
            Arena.CONCRETE, 15)

        for y in range(0, number_of_y_buildings):

            for x in range(0, number_of_x_buildings):

                # should we build it?
                is_x_edge = (x == 0 or x == (number_of_x_buildings - 1))
                is_y_edge = (y == 0 or y == (number_of_y_buildings - 1))
                if is_x_edge or is_y_edge:
                    building_pos = city_scape_start_position + vec3.Vec3(building_gap * x, 0, building_gap * y)
                    Skyscraper(
                        width=building_width, 
                        number_of_floors=floors_numbers[randrange(0, len(floors_numbers))], 
                        structure_brick_colour=frame_colours[randrange(0, len(frame_colours))]).build(mc, position=building_pos)

        # build the arena
        arena.build(mc)

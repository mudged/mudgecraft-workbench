import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
from games.arenas.arena import PittedArena
from games.arenas.cityscape import Cityscape
from games.players.player import PlayerMonitor
from games.players.teleporter import PlayerTeleporter, BelowLevelSourceArea, AreaSourceArea
from games.blocks.chagingblocks import ChangingBlock, ChangingBlockController, OrangeBlockTransition, ThinAirBlockTransition, ResetBlockTransition
import common
import math
import time
from random import randrange

mc = minecraft.Minecraft.create(address="minecraft")

# variables
falling_floor = False
numer_of_walls = 4
number_of_doors_per_wall = 4
number_of_open_doors_per_wall = 2

# create the cityscape and arena
game_arena = PittedArena(position=vec3.Vec3(0 ,5, 0), pit_fill_block_id=block.LAVA.id, length=50, width=30, floor_brick_colour=common.WHITE, wall_brick_colour=common.LIGHT_BLUE)
Cityscape(game_arena).build(mc)

player_monitor = PlayerMonitor()
block_controller = ChangingBlockController(player_monitor)
player_teleporter = PlayerTeleporter(player_monitor)

# teleport any player that goes below the area floor
player_teleporter.addSourceArea(BelowLevelSourceArea(game_arena.getArenaBoxStartPosition().y - 2))
player_teleporter.addTargetPositions(game_arena.getArenaStartArea())

# create a "lid" over the arena pit using chaning blocks
pit_start_pos = game_arena.getPitBoxStartPosition()
pit_end_pos = game_arena.getPitBoxEndPosition()
if falling_floor:
    for x in range(math.floor(pit_start_pos.x), math.floor(pit_end_pos.x) + 1):
        for z in range(math.floor(pit_start_pos.z), math.floor(pit_end_pos.z) + 1):
            block_controller.addBlock(ChangingBlock(
                position=vec3.Vec3(x, pit_end_pos.y, z), 
                block_id=game_arena.floor_brick_id, 
                block_colour=game_arena.floor_brick_colour))
else:
    mc.setBlocks(pit_start_pos.x, pit_end_pos.y, pit_start_pos.z, pit_end_pos.x, pit_end_pos.y, pit_end_pos.z, game_arena.floor_brick_id, game_arena.floor_brick_colour)

# change the activated block to orange before disapraing. And reappear after 10 seconds
block_controller.addTransition(OrangeBlockTransition())
block_controller.addTransition(ThinAirBlockTransition())
block_controller.addTransition(ResetBlockTransition(10 * 1000))

# work out where the walls and doors go
length_of_pit = pit_end_pos.z - pit_start_pos.z
width_of_pit = pit_end_pos.x - pit_start_pos.x
print(f"The pit is { length_of_pit } long and { width_of_pit } wide")
wall_gap = length_of_pit / (numer_of_walls + 1)
door_gap = width_of_pit / (number_of_doors_per_wall + 1)
print(f"Wall gap { wall_gap }. Door gap { door_gap }")

# create walls
for wall_index in range(1, numer_of_walls + 1):
    wall_z = pit_start_pos.z + (wall_gap * wall_index)
    print(f"Creating Wall { wall_index } at z:{ wall_z }")
    mc.setBlocks(pit_start_pos.x, pit_end_pos.y + 1, wall_z, pit_end_pos.x, pit_end_pos.y + game_arena.height, wall_z, game_arena.floor_brick_id, game_arena.floor_brick_colour)

    door_areas = []

    # create doors
    for door_index in range(1, number_of_doors_per_wall + 1):
        door_x = pit_start_pos.x + (door_gap * door_index)

        # frame & gap
        mc.setBlocks(door_x - 2, pit_end_pos.y + 1, wall_z, door_x + 1, pit_end_pos.y + 4, wall_z, game_arena.wall_brick_id, game_arena.wall_brick_colour)
        mc.setBlocks(door_x - 1, pit_end_pos.y + 1, wall_z, door_x, pit_end_pos.y + 3, wall_z, block.AIR.id)

        # door area
        door_areas.append(AreaSourceArea(vec3.Vec3(door_x - 2, pit_end_pos.y, wall_z - 1), vec3.Vec3(door_x + 1, pit_end_pos.y + 4, wall_z + 1)))

    # remove random doors from transporter list
    for n in range(0, number_of_open_doors_per_wall):
        door_area_to_remove = door_areas[randrange(0, len(door_areas))]
        door_areas.remove(door_area_to_remove)
    for door_area in door_areas:
        player_teleporter.addSourceArea(door_area)


# start the block controller and teleporter
if falling_floor:
    block_controller.start()
player_teleporter.start()

# add the players and start the player monitor
for player_entity_id in mc.getPlayerEntityIds():
    player_monitor.addPlayerEntityId(player_entity_id)
# player_teleporter.interval = 0.2
# player_monitor.interval = 0.2
player_monitor.start()

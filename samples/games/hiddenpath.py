import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
from games.arenas.arena import PittedArena
from games.arenas.cityscape import Cityscape
from games.commands.commands import run_standard_setup, run_command_script_on_server
from games.players.player import PlayerMonitor
from games.players.teleporter import PlayerTeleporter, BelowLevelSourceArea
from games.blocks.chagingblocks import ChangingBlock, ChangingBlockController, GreenBlockTransition, ThinAirBlockTransition, ResetBlockTransition
import common
import math
import time
from random import randrange


def model_safe_path(width: int, length: int):
    
    # randomly select a path to the other side of the pit
    safe_postions = []
    path_z = 0
    path_x = randrange(2, width - 2)
    path_y = 0
    
    # add the first safe position
    safe_postions.append(vec3.Vec3(path_x, path_y, path_z))

    while path_z < length:

        last_safe_position = safe_postions[-1]
        path_x = last_safe_position.x
        path_z = last_safe_position.z

        # what are the options?
        available_transforms = []

        # forward
        available_transforms.append(common.NORTH)

        already_gone_right = (last_safe_position + common.WEST) in safe_postions
        already_gone_left = (last_safe_position + common.EAST) in safe_postions
        at_left_edge = path_x <= 2
        at_right_edge = path_x >= (width - 1)
        previously_gone_left = (last_safe_position + common.SOUTH_WEST) in safe_postions
        previously_gone_right = (last_safe_position + common.SOUTH_EAST) in safe_postions

        # can we go left?
        if not at_left_edge and not already_gone_right and not previously_gone_left:
            available_transforms.append(common.WEST)

        # can we go right?
        if not at_right_edge and not already_gone_left and not previously_gone_right:
            available_transforms.append(common.EAST)

        # select a tranformation randomly
        selected_transform = available_transforms[randrange(0, len(available_transforms))]
        next_safe_position = last_safe_position + selected_transform
        safe_postions.append(next_safe_position)

    return safe_postions
        

mc = minecraft.Minecraft.create(address="minecraft")

# create the cityscape and arena
game_arena = PittedArena(position=vec3.Vec3(0 ,5, 0), pit_fill_block_id=block.LAVA.id, length=50, width=30, floor_brick_colour=common.WHITE, wall_brick_colour=common.LIGHT_BLUE)
Cityscape(game_arena).build(mc)

player_monitor = PlayerMonitor()
safe_block_controller = ChangingBlockController(player_monitor, transitions=[], blocks=[], use_large_area=False, interval=0.1)
unsafe_block_controller = ChangingBlockController(player_monitor, transitions=[], blocks=[], use_large_area=False, interval=0.1)
player_teleporter = PlayerTeleporter(player_monitor)

# teleport any player that goes below the area floor
player_teleporter.addSourceArea(BelowLevelSourceArea(game_arena.getArenaBoxStartPosition().y - 2))
player_teleporter.addTargetPositions(game_arena.getArenaStartArea())

# get pit dimentions
pit_start_pos = game_arena.getPitBoxStartPosition()
pit_end_pos = game_arena.getPitBoxEndPosition()

# model a scaled down version of our path
safe_path_model = model_safe_path(math.floor((pit_end_pos.x - pit_start_pos.x) / 2), math.floor((pit_end_pos.z - pit_start_pos.z) / 2))

# scale up the model 1x1 becomes 2x2
safe_postions = []
for position in safe_path_model:
    x = pit_start_pos.x + (position.x * 2)
    z = pit_start_pos.z + (position.z * 2)
    y = pit_end_pos.y
    safe_postions.append(vec3.Vec3(x, y, z))
    safe_postions.append(vec3.Vec3(x, y, z) + common.NORTH)
    safe_postions.append(vec3.Vec3(x, y, z) + common.NORTH_EAST)
    safe_postions.append(vec3.Vec3(x, y, z) + common.EAST)

# create the floor
x_group_id_offset = 0.0
z_group_id_offset = 0.0
for x in range(math.floor(pit_start_pos.x), math.floor(pit_end_pos.x) + 1):
    for z in range(math.floor(pit_start_pos.z), math.floor(pit_end_pos.z) + 1):
        block_position = vec3.Vec3(x, pit_end_pos.y, z)
        
        # calculate group id
        group_value = int(str(math.floor(x_group_id_offset) + 1) + str(math.floor(z_group_id_offset) + 1))

        if block_position in safe_postions:
            safe_block_controller.addBlock(ChangingBlock(
                position=block_position, 
                group=int(group_value),
                block_id=game_arena.floor_brick_id,
                block_colour=game_arena.floor_brick_colour))
        else:
            unsafe_block_controller.addBlock(ChangingBlock(
                position=block_position, 
                group=int(group_value),
                block_id=game_arena.floor_brick_id, 
                block_colour=game_arena.floor_brick_colour))
        z_group_id_offset = z_group_id_offset + 0.5
    x_group_id_offset = x_group_id_offset + 0.5
    z_group_id_offset = 0.0


# make path blocks highlight in green for 60 seconds
safe_block_controller.addTransition(GreenBlockTransition())
safe_block_controller.addTransition(ResetBlockTransition(60 * 1000))

# make non-path blocks disapear and reappear after 30 seconds
unsafe_block_controller.addTransition(ThinAirBlockTransition())
unsafe_block_controller.addTransition(ResetBlockTransition(30 * 1000))

# start the block controllers and teleporter
safe_block_controller.start()
unsafe_block_controller.start()
player_teleporter.start()

# add the players and start the player monitor
for player_entity_id in mc.getPlayerEntityIds():
    player_monitor.addPlayerEntityId(player_entity_id)
player_monitor.start()

run_standard_setup()
run_command_script_on_server("walking-only")
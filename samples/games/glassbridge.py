import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
from games.arenas.arena import PittedArena
from games.arenas.cityscape import Cityscape
from games.commands.commands import run_standard_setup
from games.players.player import PlayerMonitor
from games.players.teleporter import PlayerTeleporter, BelowLevelSourceArea
from games.blocks.chagingblocks import ChangingBlock, ChangingBlockController, ChangingBlockTransition, GreenGlassBlockTransition, ThinAirBlockTransition, ResetBlockTransition
import common
import math
from random import randrange
from typing import List

# variables
step_width = 4
step_depth = 2
step_gap = 2

mc = minecraft.Minecraft.create(address="minecraft")

# create the cityscape and arena
game_arena = PittedArena(position=vec3.Vec3(0 ,5, 0), pit_fill_block_id=block.LAVA.id, length=50, width=30, floor_brick_colour=common.WHITE, wall_brick_colour=common.LIGHT_BLUE)
Cityscape(game_arena).build(mc)

# safe blocks turn green and then reset after 10 seconds
safe_block_transitions: List[ChangingBlockTransition] = [GreenGlassBlockTransition(), ResetBlockTransition(10 * 1000)]

# unsafe blocks turn to air and reset after 10 seconds
unsafe_block_transitions: List[ChangingBlockTransition] = [ThinAirBlockTransition(), ResetBlockTransition(10 * 1000)]

# create the player monitor
player_monitor = PlayerMonitor()
safe_block_controller = ChangingBlockController(player_monitor, blocks=[], transitions=safe_block_transitions)
unsafe_block_controller = ChangingBlockController(player_monitor, blocks=[], transitions=unsafe_block_transitions, interval=0.2)
player_teleporter = PlayerTeleporter(player_monitor)

# teleport any player that goes below the area floor
player_teleporter.addSourceArea(BelowLevelSourceArea(game_arena.getArenaBoxStartPosition().y - 1))
player_teleporter.addTargetPositions(game_arena.getArenaStartArea())

# work out the pit positions
pit_start_pos = game_arena.getPitBoxStartPosition()
pit_end_pos = game_arena.getPitBoxEndPosition()
pit_halfway_x = math.floor(pit_start_pos.x + (game_arena.width / 2))

# create steps
block_group_id = 0
for z in range(math.floor(pit_start_pos.z) + 1, math.floor(pit_end_pos.z) + 1, step_depth + step_gap):

    # start a new block group
    block_group_id = block_group_id + 1

    # choose which step will be safe
    safe_step = randrange(1, 3)
    if safe_step == 1:
        first_step_block_controller = safe_block_controller
        second_step_block_controller = unsafe_block_controller
    else:
        first_step_block_controller = unsafe_block_controller
        second_step_block_controller = safe_block_controller

    # first step
    x = pit_halfway_x - step_width
    for x_offset in range(0, step_width):
        block_position = vec3.Vec3(x + x_offset, pit_end_pos.y, z)
        for step_z in range(0, step_depth):
            first_step_block_controller.addBlock(ChangingBlock(
                position=block_position + vec3.Vec3(0, 0, step_z), 
                block_id=block.STAINED_GLASS.id, 
                block_colour=common.NONE,
                group=block_group_id))

    # start a new block group
    block_group_id = block_group_id + 1

    # second step
    x = pit_halfway_x + 1
    for x_offset in range(0, step_width):
        block_position = vec3.Vec3(x + x_offset, pit_end_pos.y, z)
        for step_z in range(0, step_depth):
            second_step_block_controller.addBlock(ChangingBlock(
                position=block_position + vec3.Vec3(0, 0, step_z), 
                block_id=block.STAINED_GLASS.id, 
                block_colour=common.NONE,
                group=block_group_id))
    

# start the block controller and teleporter
safe_block_controller.start()
unsafe_block_controller.start()
player_teleporter.start()

# add the players and start the player monitor
for player_entity_id in mc.getPlayerEntityIds():
    player_monitor.addPlayerEntityId(player_entity_id)
player_monitor.start()

run_standard_setup()
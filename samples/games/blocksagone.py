import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
from games.arenas.arena import PittedArena
from games.arenas.cityscape import Cityscape
from games.commands.commands import run_standard_setup
from games.players.player import PlayerMonitor
from games.players.teleporter import PlayerTeleporter, BelowLevelSourceArea
from games.blocks.chagingblocks import ChangingBlock, ChangingBlockController, ChangingBlockTransition, GlassBlockTransition, ThinAirBlockTransition, ResetBlockTransition
import common
import math
from random import randrange

# variables
layer_gap_height = 8
number_of_layers = 4
side_buffer = 3

mc = minecraft.Minecraft.create(address="minecraft")

# create the cityscape and arena
game_arena = PittedArena(position=vec3.Vec3(0 ,5, 0), pit_fill_block_id=block.WATER.id, length=50, width=30, floor_brick_colour=common.WHITE, wall_brick_colour=common.LIGHT_BLUE)
Cityscape(game_arena).build(mc)

player_monitor = PlayerMonitor()
block_controller = ChangingBlockController(player_monitor)
player_teleporter = PlayerTeleporter(player_monitor)

# get the dimentions of the pit
pit_start_pos = game_arena.getPitBoxStartPosition()
pit_end_pos = game_arena.getPitBoxEndPosition()
pit_length = game_arena.length - (game_arena.pit_sides_length * 2)

# teleport any player that goes below the area floor
player_teleporter.addSourceArea(BelowLevelSourceArea(game_arena.getArenaBoxStartPosition().y))

# target position(s) should be above the top layer
spawn_y_offset = (layer_gap_height * number_of_layers) + layer_gap_height
layer_start_pos = pit_start_pos + vec3.Vec3(side_buffer, spawn_y_offset, side_buffer)
layer_end_pos = pit_start_pos + vec3.Vec3(game_arena.width - (side_buffer * 2), spawn_y_offset, pit_length - (side_buffer * 2))

# target corners of the top layer 
player_teleporter.addTargetPosition(layer_start_pos + vec3.Vec3(1, 0, 1))
player_teleporter.addTargetPosition(layer_start_pos + vec3.Vec3(layer_end_pos.x - layer_start_pos.x - 1, 0, 1))
player_teleporter.addTargetPosition(layer_end_pos - vec3.Vec3(1, 0, 1))
player_teleporter.addTargetPosition(layer_start_pos + vec3.Vec3(1, 0, layer_end_pos.z - layer_start_pos.z - 1))

# target middle of the top layer
player_teleporter.addTargetPosition(layer_start_pos + vec3.Vec3( (layer_end_pos.x - layer_start_pos.x) / 2, 0, (layer_end_pos.z - layer_start_pos.z) / 2))

# the colours of the layers
layer_colours = [common.PINK, common.LIGHT_BLUE, common.WHITE, common.ORANGE, common.PURPLE, common.YELLOW, common.BLUE, common.PINK, common.PINK, common.LIGHT_BLUE]

# create the layers
for layer_number in range(number_of_layers, 0, -1):

    layer_y = pit_end_pos.y + (layer_gap_height * layer_number)
    layer_colour = layer_colours[randrange(0, len(layer_colours))]
    
    print(f"Creating layer { layer_number } at { layer_y }")
    for x in range(math.floor(pit_start_pos.x) + side_buffer, math.floor(pit_end_pos.x) - side_buffer - 1):
        for z in range(math.floor(pit_start_pos.z) + side_buffer, math.floor(pit_end_pos.z) - side_buffer - 1):
            block_controller.addBlock(ChangingBlock(
                position=vec3.Vec3(x, layer_y, z), 
                block_id=common.CONCRETE, 
                block_colour=layer_colour))

# change the activated block to yello before disapraing. And reappear after 60 seconds
block_controller.addTransition(GlassBlockTransition())
block_controller.addTransition(ThinAirBlockTransition())
block_controller.addTransition(ResetBlockTransition(60 * 1000))

# start the block controller and teleporter
block_controller.start()
player_teleporter.start()

# add the players and start the player monitor
for player_entity_id in mc.getPlayerEntityIds():
    player_monitor.addPlayerEntityId(player_entity_id)
player_monitor.start()

run_standard_setup()
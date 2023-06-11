import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import common
from games.arenas.arena import PittedArena
from games.arenas.cityscape import Cityscape
from games.players.player import PlayerMonitor
from games.players.teleporter import PlayerTeleporter, BelowLevelSourceArea
from games.blocks.chagingblocks import *
import math
import time
from random import randrange

mc = minecraft.Minecraft.create(address="minecraft")

# create the cityscape and arena
game_arena = PittedArena(position=vec3.Vec3(0 ,5, 0), pit_fill_block_id=block.LAVA.id, length=50, width=30, floor_brick_colour=common.WHITE, wall_brick_colour=common.LIGHT_BLUE)
Cityscape(game_arena).build(mc)

player_monitor = PlayerMonitor()
block_controller = ChangingBlockController(player_monitor)
player_teleporter = PlayerTeleporter(player_monitor)

# teleport any player that goes below the area floor
player_teleporter.addSourceArea(BelowLevelSourceArea(game_arena.getArenaBoxStartPosition().y - 1))
player_teleporter.addTargetPosition(game_arena.getArenaBoxStartPosition() + vec3.Vec3(game_arena.width / 2, 1, 2))
player_teleporter.addTargetPosition(game_arena.getArenaBoxStartPosition() + vec3.Vec3((game_arena.width / 2) - 1, 1, 2))
player_teleporter.addTargetPosition(game_arena.getArenaBoxStartPosition() + vec3.Vec3((game_arena.width / 2) + 1, 1, 2))

# create a "lid" over the arena pit using chaning blocks
pit_start_pos = game_arena.getPitBoxStartPosition()
pit_end_pos = game_arena.getPitBoxEndPosition()
for x in range(math.floor(pit_start_pos.x), math.floor(pit_end_pos.x) + 1):
    for z in range(math.floor(pit_start_pos.z), math.floor(pit_end_pos.z) + 1):
        block_controller.addBlock(ChangingBlock(
            position=vec3.Vec3(x, pit_end_pos.y, z), 
            block_id=game_arena.floor_brick_id, 
            block_colour=game_arena.floor_brick_colour))

# change the activated block to orange before disapraing. And reappear after 10 seconds
block_controller.addTransition(OrangeBlockTransition())
block_controller.addTransition(ThinAirBlockTransition())
block_controller.addTransition(ResetBlockTransition(10 * 1000))

# start the block controller and teleporter
block_controller.start()
player_teleporter.start()

# add the players and start the player monitor
for player_entity_id in mc.getPlayerEntityIds():
    player_monitor.addPlayerEntityId(player_entity_id)
player_monitor.start()

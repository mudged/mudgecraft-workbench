import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import common
from games.arenas.arena import PittedArena
from games.arenas.cityscape import Cityscape
from games.players.player import PlayerMonitor
from games.players.teleporter import PlayerTeleporter, AnywhereExceptSourceArea
from games.blocks.chagingblocks import *
import math
import time
from random import randrange

mc = minecraft.Minecraft.create(address="minecraft")

# create the cityscape and arena
game_arena = PittedArena(position=vec3.Vec3(0 ,5, 0), pit_fill_block_id=block.GLOWSTONE_BLOCK.id, length=50, width=30, floor_brick_colour=common.WHITE, wall_brick_colour=common.LIGHT_BLUE)
Cityscape(game_arena).build(mc)

player_monitor = PlayerMonitor()
player_teleporter = PlayerTeleporter(player_monitor)

# teleport any player back to the side of the arena
player_teleporter.addTargetPosition(game_arena.getArenaBoxStartPosition() + vec3.Vec3(game_arena.width / 2, 0, 2))
player_teleporter.addTargetPosition(game_arena.getArenaBoxStartPosition() + vec3.Vec3((game_arena.width / 2) - 1, 0, 2))
player_teleporter.addTargetPosition(game_arena.getArenaBoxStartPosition() + vec3.Vec3((game_arena.width / 2) + 1, 0, 2))

# create a "lid" over the arena pit using glass blocks
pit_start_pos = game_arena.getPitBoxStartPosition()
pit_end_pos = game_arena.getPitBoxEndPosition()

mc.setBlocks(pit_start_pos.x, pit_end_pos.y, pit_start_pos.z, pit_end_pos.x, pit_end_pos.y, pit_end_pos.z, block.STAINED_GLASS.id)


# start the teleporter
player_teleporter.start()

# add the players and start the player monitor
for player_entity_id in mc.getPlayerEntityIds():
    player_monitor.addPlayerEntityId(player_entity_id)
player_monitor.start()


while True:

    # red light
    time.sleep(randrange(1, 6))

    mc.postToChat("Red Light!")
    mc.setBlocks(pit_start_pos.x, pit_end_pos.y, pit_start_pos.z, pit_end_pos.x, pit_end_pos.y, pit_end_pos.z, block.STAINED_GLASS.id, common.RED)

    # allow humamns to react
    time.sleep(0.5)

    # get the players positions
    allowed_positions: List[vec3.Vec3] = []
    for player in player_monitor.getPlayers():
        allowed_positions.append(player.position)
    player_teleporter.addSourceArea(AnywhereExceptSourceArea(positions=allowed_positions))

    # green light
    time.sleep(randrange(1, 6))

    # remove the teleporter source
    player_teleporter.source_areas.clear()

    mc.postToChat("Green Light!")
    mc.setBlocks(pit_start_pos.x, pit_end_pos.y, pit_start_pos.z, pit_end_pos.x, pit_end_pos.y, pit_end_pos.z, block.STAINED_GLASS.id, common.GREEN)

    
import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import time
from threading import Thread

mc = minecraft.Minecraft.create(address="minecraft")

# clear
mc.setBlocks(0,0,0,100,100,100, block.AIR.id)

activated_blocks = []
disapearing_blocks = []

# populate the disapearing block list
for x in range(10, 40):
    for y in range(5, 20, 5):
        for z in range(10, 40):
            disapearing_blocks.append(vec3.Vec3(x, y, z))

# create the blocks
for block_position in disapearing_blocks:
    mc.setBlock(block_position.x, block_position.y, block_position.z, block.STONE.id)

def make_block_disapear(block_position):
    mc.setBlock(block_position.x, block_position.y, block_position.z, block.WOOL.id, 8)
    time.sleep(0.5)
    mc.setBlock(block_position.x, block_position.y, block_position.z, block.WOOL.id, 1)
    time.sleep(0.5)
    mc.setBlock(block_position.x, block_position.y, block_position.z, block.AIR.id)


while True:
    # check the position of the block below the player
    block_below_player_position = mc.player.getTilePos() - vec3.Vec3(0, 1, 0);

    blocks_to_activate = []
    blocks_to_activate.append(block_below_player_position)
    blocks_to_activate.append(block_below_player_position + vec3.Vec3(1, 0, 0))
    blocks_to_activate.append(block_below_player_position - vec3.Vec3(1, 0, 0))
    blocks_to_activate.append(block_below_player_position + vec3.Vec3(0, 0, 1))
    blocks_to_activate.append(block_below_player_position - vec3.Vec3(0, 0, 1))

    for block_to_activate in blocks_to_activate:

        # if this is our block and it's not already in the activated list
        if block_to_activate in disapearing_blocks and not block_to_activate in activated_blocks:
        
            print("activating: ", block_to_activate)

            # add it to the activated list
            activated_blocks.append(block_to_activate)

            # start it disapearing on a new thread
            Thread(target=make_block_disapear, args=(block_to_activate,)).start()

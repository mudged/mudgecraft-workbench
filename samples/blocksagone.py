import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import time
from threading import Thread

mc = minecraft.Minecraft.create(address="minecraft")

# clear
mc.setBlocks(0,0,0,100,100,100, block.AIR.id)

activatedBlocks = []
disapearingBlocks = []

# populate the disapearing block list
for x in range(10, 40):
    for y in range(5, 20, 5):
        for z in range(10, 40):
            disapearingBlocks.append(vec3.Vec3(x, y, z))

# create the blocks
for blockPos in disapearingBlocks:
    mc.setBlock(blockPos.x, blockPos.y, blockPos.z, block.STONE.id)

def make_block_disapear(blockPos):
    mc.setBlock(blockPos.x, blockPos.y, blockPos.z, block.WOOL.id, 8)
    time.sleep(0.5)
    mc.setBlock(blockPos.x, blockPos.y, blockPos.z, block.WOOL.id, 1)
    time.sleep(0.5)
    mc.setBlock(blockPos.x, blockPos.y, blockPos.z, block.AIR.id)


while True:
    # check the position of the block below the player
    blockBelowPlayerPos = mc.player.getTilePos() - vec3.Vec3(0, 1, 0);

    blocksToActivate = []
    blocksToActivate.append(blockBelowPlayerPos)
    blocksToActivate.append(blockBelowPlayerPos + vec3.Vec3(1, 0, 0))
    blocksToActivate.append(blockBelowPlayerPos - vec3.Vec3(1, 0, 0))
    blocksToActivate.append(blockBelowPlayerPos + vec3.Vec3(0, 0, 1))
    blocksToActivate.append(blockBelowPlayerPos - vec3.Vec3(0, 0, 1))

    for blockToActivate in blocksToActivate:

        # if this is our block and it's not already in the activated list
        if blockToActivate in disapearingBlocks and not blockToActivate in activatedBlocks:
        
            print("activating: ", blockToActivate)

            # add it to the activated list
            activatedBlocks.append(blockToActivate)

            # start it disapearing on a new thread
            Thread(target=make_block_disapear, args=(blockToActivate,)).start()

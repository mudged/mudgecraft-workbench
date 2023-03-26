import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block

mc = minecraft.Minecraft.create(address="minecraft")

height = 5
width = 8
length = 8

wallBlock = block.BEDROCK
doorSuroundBlock = wallBlock
windowBlock = block.STAINED_GLASS
doorBlock = block.DOOR_DARK_OAK
carpetColour = 11

# work out the dimensions (inside and out)
startPos = vec3.Vec3(10, -1, 10)
endPos = startPos + vec3.Vec3(width, height, length)

#work out the inside space
insideStartPos = startPos + vec3.Vec3(1, 1, 1)
insideEndPos = endPos - vec3.Vec3(1, 1, 1)

# build structure
mc.setBlocks(startPos.x, startPos.y, startPos.z, endPos.x, endPos.y, endPos.z, wallBlock.id)
mc.setBlocks(insideStartPos.x, insideStartPos.y, insideStartPos.z, insideEndPos.x, insideEndPos.y, insideEndPos.z, block.AIR.id)

# let there be light
mc.setBlocks(insideStartPos.x, insideEndPos.y, insideStartPos.z, insideEndPos.x, insideEndPos.y, insideEndPos.z, block.GLOWSTONE_BLOCK.id)

# carpet
mc.setBlocks(insideStartPos.x, insideStartPos.y - 1, insideStartPos.z, insideEndPos.x, insideStartPos.y - 1, insideEndPos.z, block.WOOL.id, carpetColour)

# door
doorPosition = vec3.Vec3(startPos.x + int(width / 2), startPos.y + 1, startPos.z)
mc.setBlocks(doorPosition.x - 1, doorPosition.y, doorPosition.z, doorPosition.x + 1, doorPosition.y + 2, doorPosition.z, doorSuroundBlock.id)
mc.setBlocks(doorPosition.x, doorPosition.y, doorPosition.z, doorPosition.x, doorPosition.y + 1, doorPosition.z, block.AIR.id)
mc.setBlock(doorPosition.x, doorPosition.y + 1, doorPosition.z, block.DOOR_DARK_OAK.id, 8)
mc.setBlock(doorPosition.x, doorPosition.y, doorPosition.z, block.DOOR_DARK_OAK.id, 5)

# door torchs
mc.setBlock(doorPosition.x - 1, doorPosition.y + 1, doorPosition.z - 1, block.TORCH.id, 4)
mc.setBlock(doorPosition.x + 1, doorPosition.y + 1, doorPosition.z - 1, block.TORCH.id, 4)

# windows
windowPosition = vec3.Vec3(startPos.x, startPos.y + 2, startPos.z + int(length/2) - 1)
mc.setBlocks(windowPosition.x, windowPosition.y, windowPosition.z, windowPosition.x, windowPosition.y, windowPosition.z + 2, windowBlock.id)
windowPosition = vec3.Vec3(endPos.x, startPos.y + 2, startPos.z + int(length/2) - 1)
mc.setBlocks(windowPosition.x, windowPosition.y, windowPosition.z, windowPosition.x, windowPosition.y, windowPosition.z + 2, windowBlock.id)
windowPosition = vec3.Vec3(startPos.x + int(width / 2) - 1, startPos.y + 2, endPos.z)
mc.setBlocks(windowPosition.x, windowPosition.y, windowPosition.z, windowPosition.x + 2, windowPosition.y, windowPosition.z, windowBlock.id)

# bed
mc.setBlock(insideStartPos.x, insideStartPos.y, insideStartPos.z, block.BED.id, 10)
mc.setBlock(insideStartPos.x, insideStartPos.y, insideStartPos.z + 1, block.BED.id, 2)

# chest
mc.setBlock(insideEndPos.x, insideStartPos.y, insideEndPos.z, block.CHEST.id);

# crafting table
mc.setBlock(insideEndPos.x, insideStartPos.y, insideStartPos.z, block.CRAFTING_TABLE.id)

# furnace
mc.setBlock(insideStartPos.x, insideStartPos.y, insideEndPos.z, block.FURNACE_ACTIVE.id)

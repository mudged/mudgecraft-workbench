import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block

mc = minecraft.Minecraft.create(address="minecraft")

height = 5
width = 8
length = 8

wall_block = block.BEDROCK
door_suround_block = wall_block
window_block = block.STAINED_GLASS
door_block = block.DOOR_DARK_OAK
carpet_colour = 11

# work out the dimensions (inside and out)
start_position = vec3.Vec3(10, -1, 10)
start_position = mc.player.getTilePos()
end_position = start_position + vec3.Vec3(width, height, length)

#work out the inside space
inside_start_position = start_position + vec3.Vec3(1, 1, 1)
inside_end_position = end_position - vec3.Vec3(1, 1, 1)

# build structure
mc.setBlocks(start_position.x, start_position.y, start_position.z, end_position.x, end_position.y, end_position.z, wall_block.id)
mc.setBlocks(inside_start_position.x, inside_start_position.y, inside_start_position.z, inside_end_position.x, inside_end_position.y, inside_end_position.z, block.AIR.id)

# let there be light
mc.setBlocks(inside_start_position.x, inside_end_position.y, inside_start_position.z, inside_end_position.x, inside_end_position.y, inside_end_position.z, block.GLOWSTONE_BLOCK.id)

# carpet
mc.setBlocks(inside_start_position.x, inside_start_position.y - 1, inside_start_position.z, inside_end_position.x, inside_start_position.y - 1, inside_end_position.z, block.WOOL.id, carpet_colour)

# door
door_position = vec3.Vec3(start_position.x + int(width / 2), start_position.y + 1, start_position.z)
mc.setBlocks(door_position.x - 1, door_position.y, door_position.z, door_position.x + 1, door_position.y + 2, door_position.z, door_suround_block.id)
mc.setBlocks(door_position.x, door_position.y, door_position.z, door_position.x, door_position.y + 1, door_position.z, block.AIR.id)
mc.setBlock(door_position.x, door_position.y + 1, door_position.z, block.DOOR_DARK_OAK.id, 8)
mc.setBlock(door_position.x, door_position.y, door_position.z, block.DOOR_DARK_OAK.id, 5)

# door torchs
mc.setBlock(door_position.x - 1, door_position.y + 1, door_position.z - 1, block.TORCH.id, 4)
mc.setBlock(door_position.x + 1, door_position.y + 1, door_position.z - 1, block.TORCH.id, 4)

# windows
window_position = vec3.Vec3(start_position.x, start_position.y + 2, start_position.z + int(length/2) - 1)
mc.setBlocks(window_position.x, window_position.y, window_position.z, window_position.x, window_position.y, window_position.z + 2, window_block.id)
window_position = vec3.Vec3(end_position.x, start_position.y + 2, start_position.z + int(length/2) - 1)
mc.setBlocks(window_position.x, window_position.y, window_position.z, window_position.x, window_position.y, window_position.z + 2, window_block.id)
window_position = vec3.Vec3(start_position.x + int(width / 2) - 1, start_position.y + 2, end_position.z)
mc.setBlocks(window_position.x, window_position.y, window_position.z, window_position.x + 2, window_position.y, window_position.z, window_block.id)

# bed
mc.setBlock(inside_start_position.x, inside_start_position.y, inside_start_position.z, block.BED.id, 10)
mc.setBlock(inside_start_position.x, inside_start_position.y, inside_start_position.z + 1, block.BED.id, 2)

# chest
mc.setBlock(inside_end_position.x, inside_start_position.y, inside_end_position.z, block.CHEST.id);

# crafting table
mc.setBlock(inside_end_position.x, inside_start_position.y, inside_start_position.z, block.CRAFTING_TABLE.id)

# furnace
mc.setBlock(inside_start_position.x, inside_start_position.y, inside_end_position.z, block.FURNACE_ACTIVE.id)

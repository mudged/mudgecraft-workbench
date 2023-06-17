import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import math
import common


class Arena:

    height_to_clear = 100

    def __init__(self, width:int=30, length:int=75, height:int=6, position:vec3.Vec3=vec3.Vec3(0, 0, 0), floor_brick_id:int=common.CONCRETE, floor_brick_colour:int=common.ORANGE, wall_brick_id:int=common.CONCRETE, wall_brick_colour:int=common.WHITE, lights:bool=False):
        self.width: int = width
        self.length: int = length
        self.height: int = height
        self.position: vec3.Vec3 = position
        self.floor_brick_id: int = floor_brick_id
        self.floor_brick_colour: int = floor_brick_colour
        self.wall_brick_id: int = wall_brick_id
        self.wall_brick_colour: int = wall_brick_colour
        self.lights: bool = lights

    def getArenaBoxStartPosition(self):
        return vec3.Vec3(self.position.x - (self.width / 2), self.position.y, self.position.z - (self.length / 2))


    def getArenaBoxEndPosition(self):
        return self.getArenaBoxStartPosition() + vec3.Vec3(self.width, self.height, self.length)


    def getArenaStartArea(self):
        middle_of_startof_arena = self.getArenaBoxStartPosition() + vec3.Vec3(self.width / 2, 0, 2)

        area = []
        area.append(middle_of_startof_arena)
        area.append(middle_of_startof_arena + common.EAST)
        area.append(middle_of_startof_arena + common.WEST)

        return area


    def build(self, mc: minecraft.Minecraft):

        # position will be the middle of the arean, so start position is half the width and length
        start_pos = self.getArenaBoxStartPosition()
        end_pos = self.getArenaBoxEndPosition()

        # clear the area
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, start_pos.y + self.height_to_clear, end_pos.z, block.AIR.id)

        # build the floor
        print(f"Building arena floor at { start_pos.x }, { start_pos.y - 1 }, { start_pos.z }, { end_pos.x }, { start_pos.y - 1 }, { end_pos.z }")
        mc.setBlocks(start_pos.x, start_pos.y - 1, start_pos.z, end_pos.x, start_pos.y - 1, end_pos.z, self.floor_brick_id, self.floor_brick_colour)

        # build the walls
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, end_pos.y, start_pos.z, self.wall_brick_id, self.wall_brick_colour)
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, start_pos.x, end_pos.y, end_pos.z, self.wall_brick_id, self.wall_brick_colour)
        mc.setBlocks(end_pos.x, start_pos.y, start_pos.z, end_pos.x, end_pos.y, end_pos.z, self.wall_brick_id, self.wall_brick_colour)
        mc.setBlocks(start_pos.x, start_pos.y, end_pos.z, end_pos.x, end_pos.y, end_pos.z, self.wall_brick_id, self.wall_brick_colour)

        # stripe the wall
        stripe_y = end_pos.y - 1
        mc.setBlocks(start_pos.x, stripe_y, start_pos.z, end_pos.x, stripe_y, start_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(start_pos.x, stripe_y, start_pos.z, start_pos.x, stripe_y, end_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(end_pos.x, stripe_y, start_pos.z, end_pos.x, stripe_y, end_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(start_pos.x, stripe_y, end_pos.z, end_pos.x, stripe_y, end_pos.z, self.floor_brick_id, self.floor_brick_colour)
        
        # start area highlight
        middle_of_startof_arena = start_pos + vec3.Vec3((self.width / 2) - 2, 0, 0)
        mc.setBlocks(middle_of_startof_arena.x, start_pos.y, start_pos.z, middle_of_startof_arena.x, start_pos.y + 1, start_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(middle_of_startof_arena.x + 4, start_pos.y, start_pos.z, middle_of_startof_arena.x + 4, start_pos.y + 1, start_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(middle_of_startof_arena.x, start_pos.y + 2, start_pos.z, middle_of_startof_arena.x + 4, start_pos.y + 2, start_pos.z, self.floor_brick_id, self.floor_brick_colour)
       
        # stop area highlight
        middle_of_startof_arena = start_pos + vec3.Vec3((self.width / 2) - 2, 0, 0)
        mc.setBlocks(middle_of_startof_arena.x, start_pos.y, end_pos.z, middle_of_startof_arena.x, start_pos.y + 1, end_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(middle_of_startof_arena.x + 4, start_pos.y, end_pos.z, middle_of_startof_arena.x + 4, start_pos.y + 1, end_pos.z, self.floor_brick_id, self.floor_brick_colour)
        mc.setBlocks(middle_of_startof_arena.x, start_pos.y + 2, end_pos.z, middle_of_startof_arena.x + 4, start_pos.y + 2, end_pos.z, self.floor_brick_id, self.floor_brick_colour)

        # lights
        if self.lights:
            lights_y = end_pos.y - 1
            for x in range(math.floor(start_pos.x), math.floor(end_pos.x)):
                if x % 3 == 0:
                    mc.setBlock(x, lights_y, start_pos.z, block.GLOWSTONE_BLOCK.id)
                    mc.setBlock(x, lights_y, end_pos.z, block.GLOWSTONE_BLOCK.id)
            for z in range(math.floor(start_pos.z), math.floor(end_pos.z)):
                if z % 3 == 0:
                    mc.setBlock(start_pos.x, lights_y, z, block.GLOWSTONE_BLOCK.id)
                    mc.setBlock(end_pos.x, lights_y, z, block.GLOWSTONE_BLOCK.id)


class PittedArena(Arena):

    def __init__(self, width:int=30, length:int=75, height:int=6, position:vec3.Vec3=vec3.Vec3(0, 0, 0), floor_brick_id:int=common.CONCRETE, floor_brick_colour:int=common.ORANGE, wall_brick_id:int=common.CONCRETE, wall_brick_colour:int=common.WHITE, lights:bool=False, pit_depth:int=4, pit_sides_length:int=4, pit_fill_depth:int=1, pit_fill_block_id:int=block.AIR.id):
        super().__init__(width, length, height, position, floor_brick_id, floor_brick_colour, wall_brick_id, wall_brick_colour, lights)
        self.pit_depth: int = pit_depth
        self.pit_sides_length: int = pit_sides_length
        self.pit_fill_depth: int = pit_fill_depth
        self.pit_fill_block_id: int = pit_fill_block_id


    def getPitBoxStartPosition(self):
        return self.getArenaBoxStartPosition() + vec3.Vec3(1, self.pit_depth * -1 , self.pit_sides_length + 1)

 
    def getPitBoxEndPosition(self):
        return self.getArenaBoxEndPosition() - vec3.Vec3(1, self.height + 1 , self.pit_sides_length + 1)


    def build(self, mc: minecraft.Minecraft):

        # pit frame - create a box under the arena
        start_pos = self.getArenaBoxStartPosition()
        end_pos = start_pos - vec3.Vec3(self.width * -1, self.pit_depth + 1, self.length * -1)
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, end_pos.y, end_pos.z, self.wall_brick_id, self.wall_brick_colour)
        mc.setBlocks(start_pos.x, end_pos.y, start_pos.z, end_pos.x, end_pos.y, end_pos.z, self.floor_brick_id, self.floor_brick_colour)

        # draw the arena
        super().build(mc)

        start_pos = self.getPitBoxStartPosition()
        end_pos = self.getPitBoxEndPosition()

        # hollow out the pit
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, end_pos.y, end_pos.z, block.AIR.id)

        # pit fill (already full of air)
        if self.pit_fill_block_id != block.AIR.id:
            mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, start_pos.y - self.pit_fill_depth, end_pos.z, self.pit_fill_block_id)


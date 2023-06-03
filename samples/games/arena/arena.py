import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block



class Arena:

    CONCRETE = 251

    width = 30
    length = 75
    height = 6
    position = vec3.Vec3(0, 5, 0)
    floor_brick_id = CONCRETE
    floor_brick_colour = 1
    wall_brick_id = CONCRETE
    wall_brick_colour = 0
    height_to_clear = 50

    def __init__(self, width=30, length=75, height=6, position=vec3.Vec3(0, 0, 0), floor_brick_id=CONCRETE, floor_brick_colour=1, wall_brick_id=CONCRETE, wall_brick_colour=0):
        self.width = width
        self.length = length
        self.height = height
        self.position = position
        self.floor_brick_id = floor_brick_id
        self.floor_brick_colour = floor_brick_colour
        self.wall_brick_id = wall_brick_id
        self.wall_brick_colour = wall_brick_colour

    def getArenaBoxStartPosition(self):
        return vec3.Vec3(self.position.x - (self.width / 2), self.position.y, self.position.z - (self.length / 2))


    def getArenaBoxEndPosition(self):
        return self.getArenaBoxStartPosition() + vec3.Vec3(self.width, self.height, self.length)


    def build(self, mc):

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


class PittedArena(Arena):

    pit_depth = 4
    pit_sides_length = 4
    pit_fill_block_id = block.AIR.id

    def __init__(self, width=30, length=75, height=6, position=vec3.Vec3(0, 0, 0), floor_brick_id=Arena.CONCRETE, floor_brick_colour=1, wall_brick_id=Arena.CONCRETE, wall_brick_colour=0, pit_depth=4, pit_sides_length=4, pit_fill_block_id=block.AIR.id):
        super().__init__(width, length, height, position, floor_brick_id, floor_brick_colour, wall_brick_id, wall_brick_colour)
        self.pit_depth = pit_depth
        self.pit_sides_length = pit_sides_length
        self.pit_fill_block_id = pit_fill_block_id


    def getPitBoxStartPosition(self):
        return self.getArenaBoxStartPosition() + vec3.Vec3(1, self.pit_depth * -1 , self.pit_sides_length + 1)

 
    def getPitBoxEndPosition(self):
        return self.getArenaBoxEndPosition() - vec3.Vec3(1, self.height + 1 , self.pit_sides_length + 1)


    def build(self, mc):

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
            mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, end_pos.y - 1, end_pos.z, self.pit_fill_block_id)


import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.vec3 as vec3


class Skyscraper:
    
    number_of_floors = 15
    width = 15
    floor_height = 4
    structure_brick_id = 251 # concrete
    structure_brick_colour = 7 # gray
    stair_brick_id = 164 # dar oak wood stairs
    
    
    def __init__(self, number_of_floors=15, width=15, floor_height = 4, structure_brick_id=251, structure_brick_colour=7, stair_brick_id=164):
        
        self.number_of_floors = number_of_floors
        self.width = width
        self.floor_height = floor_height
        
        self.structure_brick_id = structure_brick_id
        self.structure_brick_colour = structure_brick_colour
        self.stair_brick_id = stair_brick_id
        
    
    def build(self, mc, position):

        print(f"Building { self.number_of_floors } Floor Skyscraper at { position }")

        start = vec3.Vec3(position.x, position.y, position.z)
        end = position + vec3.Vec3(self.width, 0, self.width)
        roof_y = position.y + (self.number_of_floors * self.floor_height)

        # clear area for tower
        mc.setBlocks(start.x - 1, start.y + 1, start.z - 1, start.x + self.width + 1, roof_y + 1, start.z + self.width + 1, block.AIR.id)

        # build base    
        mc.setBlocks(start.x - 1, start.y, start.z - 1, start.x + self.width + 1, start.y, start.z + self.width + 1, self.structure_brick_id, self.structure_brick_colour)

        # build floors
        for floor_number in range(1, self.number_of_floors + 1):

            # build floor at current position
            self._build_floor(mc, start, floor_number)
            self._build_stairs(mc, start, floor_number)

            # move pointer to the next floor
            start = start + vec3.Vec3(0, self.floor_height, 0)


        # build roof
        mc.setBlocks(start.x, roof_y, start.z, start.x + self.width, roof_y, start.z + self.width, self.structure_brick_id, self.structure_brick_colour)

        

    def _build_floor(self, mc, start_pos, floor_number):

        end_pos = start_pos + vec3.Vec3(self.width, self.floor_height, self.width)

        # floor
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, end_pos.x, start_pos.y, end_pos.z, self.structure_brick_id, self.structure_brick_colour)

        # pillars
        mc.setBlocks(start_pos.x, start_pos.y, start_pos.z, start_pos.x, end_pos.y - 1, start_pos.z, self.structure_brick_id, self.structure_brick_colour)
        mc.setBlocks(end_pos.x, start_pos.y, start_pos.z, end_pos.x, end_pos.y - 1, start_pos.z, self.structure_brick_id, self.structure_brick_colour)
        mc.setBlocks(start_pos.x, start_pos.y, end_pos.z, start_pos.x, end_pos.y - 1, end_pos.z, self.structure_brick_id, self.structure_brick_colour)
        mc.setBlocks(end_pos.x, start_pos.y, end_pos.z, end_pos.x, end_pos.y - 1, end_pos.z, self.structure_brick_id, self.structure_brick_colour)

        # glass
        mc.setBlocks(start_pos.x + 1, start_pos.y + 1, start_pos.z, end_pos.x - 1, end_pos.y - 1, start_pos.z, block.GLASS.id)
        mc.setBlocks(start_pos.x + 1, start_pos.y + 1, end_pos.z, end_pos.x - 1, end_pos.y - 1, end_pos.z, block.GLASS.id)
        mc.setBlocks(start_pos.x, start_pos.y + 1, start_pos.z + 1, start_pos.x, end_pos.y - 1, end_pos.z - 1, block.GLASS.id)
        mc.setBlocks(end_pos.x, start_pos.y + 1, start_pos.z + 1, end_pos.x, end_pos.y - 1, end_pos.z - 1, block.GLASS.id)

        # build entrances on the ground floor (one on each side)
        if floor_number == 1:
            mc.setBlock(start_pos.x + (self.width / 2), start_pos.y + 1, start_pos.z, block.AIR.id)
            mc.setBlock(start_pos.x + (self.width / 2), start_pos.y + 2, start_pos.z, block.AIR.id)

            mc.setBlock(start_pos.x + (self.width / 2), start_pos.y + 1, end_pos.z, block.AIR.id)
            mc.setBlock(start_pos.x + (self.width / 2), start_pos.y + 2, end_pos.z, block.AIR.id)

            mc.setBlock(start_pos.x, start_pos.y + 1, start_pos.z + (self.width / 2), block.AIR.id)
            mc.setBlock(start_pos.x, start_pos.y + 2, start_pos.z + (self.width / 2), block.AIR.id)

            mc.setBlock(end_pos.x, start_pos.y + 1, start_pos.z + (self.width / 2), block.AIR.id)
            mc.setBlock(end_pos.x, start_pos.y + 2, start_pos.z + (self.width / 2), block.AIR.id)


    def _build_stairs(self, mc, start_pos, floor_number):

        x = start_pos.x + (self.width / 2) - (self.floor_height / 2)
        y = start_pos.y + 1
        z = start_pos.z + self.width / 2

        # you don't need a hole on the ground floor
        if floor_number > 1:

            # create the stair hole
            for stair_number in range(self.floor_height - 1):    
                mc.setBlock(x + stair_number, y - 1, z, block.AIR.id)
                mc.setBlock(x + stair_number, y - 1, z + 1, block.AIR.id)

            # restore the stair removed by floor/roof
            mc.setBlock(x + self.floor_height - 1, y - 1, z, self.stair_brick_id)
            mc.setBlock(x + self.floor_height - 1, y - 1, z + 1, self.stair_brick_id)

        # create stair
        for stair_number in range(self.floor_height):
            mc.setBlock(x + stair_number, y + stair_number, z, self.stair_brick_id)
            mc.setBlock(x + stair_number, y + stair_number, z + 1, self.stair_brick_id)

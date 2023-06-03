import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
import mcpi.entity as entity
from dataclasses import dataclass
import time
from threading import Thread

@dataclass
class UnSafeBlock:
    position: vec3.Vec3
    brick_id: int
    brick_colour: int
    time_triggered: float
    current_transition: int

@dataclass
class UnSafeBlockTransition:
    time_after_trigger: int
    brick_id: int
    brick_colour: int


class UnSafeBlockController:

    blocks = []
    transitions = []
    entity_ids_to_monitor = []
    is_running = False
    use_large_area = True

    def __init__(self, blocks=[], entity_ids_to_monitor=[], transitions=[], use_large_area=True):
        self.blocks = blocks
        self.entity_ids_to_monitor = entity_ids_to_monitor
        self.transitions = transitions
        self.use_large_area = use_large_area

    def addBlock(self, block):
        self.blocks.append(block)

    def addTransition(self, transition):
        self.transitions.append(transition)

    def start(self, mc):
        pass

        # draw the blocks
        for block in self.blocks:
            mc.setBlock(block.position.x, block.position.y, block.position.z, block.brick_id, block.brick_colour)

        self.is_running = True

        # start monitoring the entity ids
        Thread(target=self._monitor_entities, args=(mc,)).start()

        # start monitoring the blocks
        Thread(target=self._monitor_blocks, args=(mc,)).start()


    def stop(self):
        self.is_running = False

    def _monitor_entities(self, mc):

        while self.is_running:

            positions_to_check = []

            for entity_id in self.entity_ids_to_monitor:
                block_below_entity_position = mc.entity.getTilePos(entity_id) - vec3.Vec3(0, 1, 0);
                positions_to_check.append(block_below_entity_position)

                # trigger around the block
                if self.use_large_area:
                    positions_to_check.append(block_below_entity_position + vec3.Vec3(1, 0, 0))
                    positions_to_check.append(block_below_entity_position - vec3.Vec3(1, 0, 0))
                    positions_to_check.append(block_below_entity_position + vec3.Vec3(0, 0, 1))
                    positions_to_check.append(block_below_entity_position - vec3.Vec3(0, 0, 1))

            # is the entity on a block?
            for block in self.blocks:
                if block.position in positions_to_check:

                    # has the block been triggered already?
                    if block.time_triggered == None:
                        block.time_triggered = round(time.time() * 1000)

            time.sleep(0.5)


    def _monitor_blocks(self, mc: minecraft.Minecraft):
        while self.is_running:

            current_millis = round(time.time() * 1000)
            
            # find trigged blocks
            for block in self.blocks:
                if block.time_triggered != None:

                    # start the transition sequence
                    if block.current_transition == None:
                        block.current_transition = 0

                    transition = self.transitions[block.current_transition]
                    if current_millis >= block.time_triggered + transition.time_after_trigger:
                        if transition.brick_id == -1 and transition.brick_colour == -1:
                            mc.setBlock(block.position.x, block.position.y, block.position.z, block.brick_id, block.brick_colour)    
                        else:
                            mc.setBlock(block.position.x, block.position.y, block.position.z, transition.brick_id, transition.brick_colour)

                        # move to the next transition?
                        if block.current_transition + 1 >= len(self.transitions):
                            # finished
                            block.time_triggered = None
                            block.current_transition = None
                        else:
                            block.current_transition = block.current_transition + 1 



            time.sleep(0.5)
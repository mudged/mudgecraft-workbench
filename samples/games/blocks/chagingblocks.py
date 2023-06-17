import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as block
from dataclasses import dataclass
from typing import List
import time
from threading import Thread
from games.players.player import PlayerMonitor
import common

@dataclass
class ChangingBlock:
    position: vec3.Vec3
    block_id: int
    block_colour: int
    time_triggered: float = None
    current_transition: int = None
    group: int = None


@dataclass
class ChangingBlockTransition:
    time_after_trigger: int
    block_id: int
    block_colour: int = common.NONE


class YellowBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=common.CONCRETE, block_colour=common.YELLOW)


class OrangeBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=common.CONCRETE, block_colour=common.ORANGE)
        

class RedBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=common.CONCRETE, block_colour=common.RED)

class GlassBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=block.STAINED_GLASS.id, block_colour=None)

class RedGlassBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=block.STAINED_GLASS.id, block_colour=common.RED)


class GreenGlassBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=block.STAINED_GLASS.id, block_colour=common.GREEN)


class ThinAirBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int = 0):
        super().__init__(time_after_trigger=time_after_trigger, block_id=block.AIR.id, block_colour=common.NONE)


class ResetBlockTransition(ChangingBlockTransition):
    
    def __init__(self, time_after_trigger: int):
        super().__init__(time_after_trigger=time_after_trigger, block_id=-1, block_colour=-1)



class ChangingBlockController:
      
    def __init__(self, player_monitor:PlayerMonitor, blocks:List[ChangingBlock]=[], transitions:List[ChangingBlockTransition]=[], interval: float=0.5, use_large_area:bool=True):
        self.player_monitor: PlayerMonitor = player_monitor
        self.blocks: List[ChangingBlock] = blocks
        self.transitions: List[ChangingBlockTransition] = transitions
        self.use_large_area: bool = use_large_area
        self.interval: float = interval
        self.running: bool = False


    def addBlock(self, block: ChangingBlock):
        self.blocks.append(block)


    def addTransition(self, transition: ChangingBlockTransition):
        self.transitions.append(transition)


    def start(self, mc: minecraft.Minecraft = None):

        if mc is None:
            mc = minecraft.Minecraft.create(address="minecraft")

        # draw the blocks
        for block in self.blocks:
            mc.setBlock(block.position.x, block.position.y, block.position.z, block.block_id, block.block_colour)

        self.running = True

        # start monitoring the entity ids
        Thread(target=self._monitor_entities).start()

        # start monitoring the blocks
        Thread(target=self._monitor_blocks, args=(mc,)).start()


    def stop(self):
        self.running = False


    def _monitor_entities(self):

        while self.running:

            positions_to_check: List[vec3.Vec3] = []
            
            for player in self.player_monitor.getPlayers():
                block_below_player_position = player.position + common.BELOW
                positions_to_check.append(block_below_player_position)

                # trigger around the block
                if self.use_large_area:

                    positions_to_check.append(block_below_player_position + common.NORTH)
                    positions_to_check.append(block_below_player_position + common.NORTH_EAST)
                    positions_to_check.append(block_below_player_position + common.EAST)
                    positions_to_check.append(block_below_player_position + common.SOUTH_EAST)
                    positions_to_check.append(block_below_player_position + common.SOUTH)
                    positions_to_check.append(block_below_player_position + common.SOUTH_WEST)
                    positions_to_check.append(block_below_player_position + common.WEST)
                    positions_to_check.append(block_below_player_position + common.NORTH_WEST)
                   
            groups_to_trigger: List[int] = []
            trigger_time = round(time.time() * 1000)

            # is the entity on a chaing block?
            for block in self.blocks:
                if block.position in positions_to_check:

                    # has the block been triggered already?
                    if block.time_triggered == None:
                        block.time_triggered = trigger_time
                        
                        # is the block part of a group?
                        if block.group is not None:
                            groups_to_trigger.append(block.group)
                        
            # any ralated groups to trigger?
            for group_id in groups_to_trigger:
                for block in self.blocks:
                    if block.time_triggered == None and block.group == group_id:
                        block.time_triggered = trigger_time
            

            time.sleep(self.interval)


    def _monitor_blocks(self, mc: minecraft.Minecraft):
        while self.running:

            current_millis = round(time.time() * 1000)
            
            # find trigged blocks
            for block in self.blocks:
                if block.time_triggered != None:

                    # start the transition sequence
                    if block.current_transition == None:
                        block.current_transition = 0

                    transition = self.transitions[block.current_transition]
                    if current_millis >= block.time_triggered + transition.time_after_trigger:
                        
                        # work out the block type
                        transistion_block_id = transition.block_id
                        if transition.block_id is None or transition.block_id < 0:
                            transistion_block_id = block.block_id
                        
                        # work out the block colour
                        transistion_block_colour = transition.block_colour
                        if transition.block_colour is None or transition.block_colour < 0:
                            transistion_block_colour = block.block_colour
                        
                        # set the block
                        mc.setBlock(block.position.x, block.position.y, block.position.z, transistion_block_id, transistion_block_colour)
                        
                        # move to the next transition?
                        if block.current_transition + 1 >= len(self.transitions):
                            # finished
                            block.time_triggered = None
                            block.current_transition = None
                        else:
                            block.current_transition = block.current_transition + 1 

            time.sleep(self.interval)
import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
from dataclasses import dataclass
from typing import List
import time
from threading import Thread
from games.players.player import PlayerMonitor

class TeleporterSourceArea:
    
    def isInArea(self, position:vec3.Vec3):
        return False


class BelowLevelSourceArea(TeleporterSourceArea):
    
    def __init__(self, level: int = 0):
        self.level: int = level
        print(f"Teleporting Players that go below { self.level }")
        
    def isInArea(self, position:vec3.Vec3):
        return position.y < self.level


class AreaSourceArea(TeleporterSourceArea):
    
    def __init__(self, start_position: vec3.Vec3, end_position: vec3.Vec3):
        self.start_position: vec3.Vec3 = start_position
        self.end_position: vec3.Vec3 = end_position
        
    def isInArea(self, position:vec3.Vec3):
        if position.x >= self.start_position.x and position.x <= self.end_position.x:
            if position.y >= self.start_position.y and position.y <= self.end_position.y:
                if position.z >= self.start_position.z and position.z <= self.end_position.z:
                    return True
        return False


class AnywhereExceptSourceArea(TeleporterSourceArea):
    
    def __init__(self, positions: List[vec3.Vec3] = []):
        self.positions: List[vec3.Vec3] = positions
        
    def isInArea(self, position:vec3.Vec3):
        for allowwed_position in self.positions:
            if allowwed_position == position:
                return False
            
        return True


class PlayerTeleporter:

    def __init__(self, player_monitor:PlayerMonitor):
        self.player_monitor: PlayerMonitor = player_monitor
        self.running: bool = False
        self.source_areas: List[TeleporterSourceArea] = []
        self.target_positions: List[vec3.Vec3] = []
        self.current_target_position_index: int = 0
        self.interval:float = 0.5
        
        
    def addSourceArea(self, source: TeleporterSourceArea):
        self.source_areas.append(source)
        
        
    def addTargetPosition(self, target: vec3.Vec3):
        self.target_positions.append(target)
        

    def addTargetPositions(self, targets: List[vec3.Vec3]):
        for target in targets:
            self.addTargetPosition(target)

        
    def start(self, mc: minecraft.Minecraft = None):
    
        if mc is None:
            mc = minecraft.Minecraft.create(address="minecraft")

        self.running = True

        # start monitoring the player positions
        Thread(target=self._monitor_players, args=(mc,)).start()


    def stop(self):
        self.running = False
        
        
    def _monitor_players(self, mc: minecraft.Minecraft):
        while self.running:
            # check the player positions
            for player in self.player_monitor.getPlayers():
                
                finished_with_player = False

                # ignore if the player is in the target position
                for target_position in self.target_positions:
                    if player.position == target_position:
                        finished_with_player = True
                        print(f"Player { player.id } is already in the target area")
                        break


                # search the sources
                for source in self.source_areas:
                    if finished_with_player == False and source.isInArea(player.position):

                        # teleport player
                        if self.current_target_position_index + 1 >= len(self.target_positions):
                            self.current_target_position_index = 0
                        else:
                            self.current_target_position_index = self.current_target_position_index + 1
                            
                        target_position: vec3.Vec3 = self.target_positions[self.current_target_position_index]
                        print(f"Teleporting Player { player.id } to { target_position }")
                        mc.entity.setPos(player.id, target_position.x, target_position.y, target_position.z)

                        finished_with_player = True
                        break
            
            time.sleep(self.interval)
        
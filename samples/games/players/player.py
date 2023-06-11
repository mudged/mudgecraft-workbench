
import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.entity as entity
from threading import Thread
from dataclasses import dataclass
import time
from typing import List

@dataclass
class Player:
    id: int
    position: vec3.Vec3


class PlayerMonitor:

    def __init__(self, players: List[Player] = []):
        self.players: List[Player] = players
        self.running: bool = False
        self.interval: float = 0.2


    def addPlayerEntityId(self, id: int):
        self.players.append(Player(id=id, position=vec3.Vec3(0,0,0)))


    def start(self, mc: minecraft.Minecraft = None):

        if mc is None:
            mc = minecraft.Minecraft.create(address="minecraft")

        if self.running == False:
            self.running = True
            Thread(target=self._monitor, args=(mc,)).start()


    def _monitor(self, mc: minecraft.Minecraft):
        while self.running:
            for player in self.players:
                player.position = mc.entity.getTilePos(player.id)
            time.sleep(self.interval)


    def stop(self):
        self.running = False


    def getPlayers(self):
        return self.players


    def getPlayer(self, id: int):
        for player in self.players:
            if player.id == id:
                return player
        return None

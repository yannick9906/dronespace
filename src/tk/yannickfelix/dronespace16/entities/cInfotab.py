# coding=utf-8
"""
@license
This work is licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/4.0/.

@author Yannick Félix
"""
import random

from tk.yannickfelix.dronespace16.entities.cEntity import Entity
from tk.yannickfelix.jsonNetCode import Filesystem


class Infotab(Entity):
    CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜäöü.,:;-_<>|1234567890!\"$%&/(=){[]}\\?ß+*#'^é"

    stages = []
    cleared = 1

    def __init__(self, stages, cleared, name, commands, globalvars):
        super().__init__(name, -1, commands, globalvars)
        self.stages = stages
        self.cleared = cleared

    @staticmethod
    def fromDict(globalvars, dict):
        types = Filesystem.loadFile(globalvars["res_folder"]+"/entities/infotabs.json")
        thistype = types[dict["information"]]
        return Infotab(thistype["stages"], dict["cleared"], dict["name"], thistype["commands"], globalvars)

    def getTextObfuscated(self):
        text = ""
        for i, stage in enumerate(self.stages):
            if self.cleared >= i+1:
                text += stage
            else:
                for char in stage:
                    if char != "\n":
                        char = self.CHARS[random.randint(0, len(self.CHARS)-1)]
                    text += char
        return text

    def detailedInfo(self):
        return self.getTextObfuscated()
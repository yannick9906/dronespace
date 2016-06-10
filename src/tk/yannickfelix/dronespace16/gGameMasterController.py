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
import time

from tk.yannickfelix.dronespace16.gui import *
from tk.yannickfelix.dronespace16 import *
from tk.yannickfelix.dronespace16.cEntitiesController import *
from tk.yannickfelix.dronespace16.cStdCommands import *


class GameMasterController(object):

    globalvars = None

    def __init__(self):
        """
        Creates nearly every class needed
        """
        # Init globalvars
        self.globalvars = {
            "res_folder": "../../../res/",
            "running": True,
            "autoreload": False,
            "fullscreen": False,
            "frametime": 1,
            "fps": 2000,
            "class_gui": None,
            "class_gconsole": None,
            "class_ginput": None,
            "class_stdcommmands": None,
            "cb_destroyed": None,
            "cb_damaged": None,
            "cb_noenergy": None
        }

        # Init UI and save the references to globalvars
        self.globalvars['class_gui'] = GWindow(self.globalvars)
        self.globalvars['class_gconsole'] = self.globalvars['class_gui'].gameConsole
        self.globalvars['class_ginput'] = self.globalvars['class_gui'].gameInput
        self.globalvars['class_stdcommands'] = StdCommands(self.globalvars)
        self.globalvars['class_entity'] = EntitiesController(self.globalvars)

        # Callbacks
        self.globalvars['cb_destroyed'] = self.cb_droneDestroyed
        self.globalvars['cb_damaged'] = self.cb_droneDamaged
        self.globalvars['cb_noenergy'] = self.cb_droneNoEnergy

        # Welcome / Startup messages -> TODO Auslagern
        self.globalvars['class_gconsole'].printMessage("B.E.N.'s Dronecontroller v2.3b", "left")
        self.globalvars['class_gconsole'].printMessage("Starting Services...", "left")
        self.globalvars['class_gconsole'].printMessage("We're searching for files...", "left")
        text = """
                                         ,
                  ,-.       _,---._ __  / \\
                 /  )    .-'       `./ /   \\
                (  (   ,'            `/    /|
                 \  `-"             \\'\   / |
                  `.              ,  \ \ /  |
                   /`.          ,'-`----Y   |
                  (            ;        |   '
                  |  ,-.    ,-'         |  /
                  |  | (   |    Files?  | /
                  )  |  \  `.___________|/
                  `--'   `--'
            """
        """self.globalvars['class_gconsole'].printMessage(text, "left", "", False)
        self.globalvars['class_gconsole'].printMessage("Ready.", "left")
        self.globalvars['class_gconsole'].waitAndWrite()"""

        # The "Main" Gameloop
        while self.globalvars['running']:
            self.update()
            time.sleep(0.02)

        # When the game is stopped
        self.globalvars['class_gui'].destroy()
        self.globalvars['class_gui'].quit()

    def load(self):
        """
        @deprecated
        """
        pass
        """json = Filesystem.loadFile("../../savegame.json")
        i = 0
        for elem in json:
            if json[elem]['class'] == "drone":
                self.entities.append(Drone.fromDict(i, json[elem], self.textoutput.printMessage))
            i += 1"""

    def update(self):
        """
        This method is called by the constructor of this class every 20ms.
        It ensures that every "update()"-Method is called and makes some other magic
        """
        self.globalvars['class_entity'].update()
        # Get the current command, if there's one
        cmd = self.globalvars['class_ginput'].getUserText()
        # Update the command display
        self.globalvars['class_gconsole'].updateInputting(self.globalvars['class_ginput'].get())
        # Handle cmds
        self.handleCmd(cmd)
        # Next writing step
        self.globalvars['class_gconsole'].writeTick()
        # Update UI
        self.globalvars['class_gui'].update()
        self.globalvars['class_ginput'].focus()

    def handleCmd(self, cmd):
        """
        This method is part of the update method, but for better
        readability it is an extra method.
        @param cmd: The cmd typed in by the user
        @type cmd: str
        """
        # Some simple checks
        if cmd != "" and cmd != " ":
            # Print the cmd onto the screen
            self.globalvars['class_gconsole'].printMessage(cmd, "right", "", True, False)

            # This actually handles the cmds
            if not self.globalvars['class_stdcommands'].handleCommands(cmd.lower()):
                if not self.globalvars['class_entity'].handleCommands(cmd.lower()):
                    self.globalvars['class_gconsole'].printMessage(
                        "Sorry, I think you misspelled this command... Maybe a cookie would help...", "left", "")

    def cb_droneDestroyed(self, drone, amount, x):
        self.globalvars['class_gconsole'].printMessage("**Drone {0}<{1}> has been destroyed(-{2}HP)**".format(drone.droneID, drone.name, amount), "center", newline=False, markup=True)
        self.globalvars['class_gconsole'].waitAndWrite()

    def cb_droneDamaged(self, drone, amount, x):
        print(x)
        self.globalvars['class_gconsole'].printMessage("**Drone {0}<{1}> has been damaged(-{2}HP)**".format(drone.droneID, drone.name, amount), "center", newline=False, markup=True)
        self.globalvars['class_gconsole'].waitAndWrite()

    def cb_droneNoEnergy(self, drone):
        self.globalvars['class_gconsole'].printMessage("**Drone {0}<{1}> has run out of energy. That's sad.**".format(drone.droneID, drone.name), "center", newline=False, markup=True)
        self.globalvars['class_gconsole'].waitAndWrite()
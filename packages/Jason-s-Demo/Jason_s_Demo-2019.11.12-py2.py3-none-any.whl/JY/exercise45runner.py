from exercise45class import *

class runner(object):
    scene = {
            'Kingdom_Start': kingomstart(),
            'Armory_House': armory(),
            'Lake_Wizzard': lake(),
            'Forest_Monster': forest(),
            'Cave_Dragon': cave(),
            'Kingdom_End': kingdomend(),
            'Game_Over': fail(),
    }

    def __init__(self, name):
        self.name = name
    def next_scene(self,next_name):
        return runner.scene.get(next_name)
        #this is how to open a scene.
        #the scene have to return to an engine that can re-run the program.
    def open_scene(self):
        return self.next_scene(self.name)
        #here we need open_scene and next_scene because they use two different names.
        #we need two names, one is for opening the original scene to start the program. the other is used for opening the subsequent scenes.
        #So open_scene is onlu used once for kicking the program. next_scene is used multiply times to open any new scenes.

class engine(object):
    def __init__(self, run_name):
        self.run_name = run_name
    def start(self):
        the_scene = self.run_name.open_scene()
        the_last = self.run_name.next_scene('Kingdom_End')

        while the_scene != the_last:
            the_next = the_scene.enter()
            the_scene = self.run_name.next_scene(the_next)
        the_scene.enter()




start = runner('Kingdom_Start')
open = engine(start)
open.start()

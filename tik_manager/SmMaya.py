import os
import SmRoot
reload(SmRoot)
from SmRoot import RootManager

import maya.cmds as cmds
import maya.mel as mel

class MayaManager(RootManager):
    def __init__(self):
        super(MayaManager, self).__init__()
        self.init_paths()
        self.init_database()
        self.backwardcompatibility()

    def getProjectDir(self):
        p_path = cmds.workspace(q=1, rd=1)
        norm_p_path = os.path.normpath(p_path)
        return norm_p_path
    def getSceneFile(self):
        s_path = cmds.file(q=True, sn=True)
        norm_s_path = os.path.normpath(s_path)
        return norm_s_path

    def set_project(self, path):
        # totally software specific or N/A
        melCompPath = path.replace("\\", "/") # mel is picky
        command = 'setProject "%s";' %melCompPath
        mel.eval(command)
        self.projectDir = cmds.workspace(q=1, rd=1)



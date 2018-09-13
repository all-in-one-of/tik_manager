import json
import os

import datetime

def folderCheck(folder):
    if not os.path.isdir(os.path.normpath(folder)):
        os.makedirs(os.path.normpath(folder))

class SmDatabase(object):
    def __init__(self):
        super(SmDatabase, self).__init__()
        self.userSettings_Path = os.path.join(os.path.expanduser("~"),"SceneManager")
        # self.project_Path =  os.path.normpath(pm.workspace(q=1, rd=1))
        self.generalSettings_Path = os.path.dirname(os.path.abspath(__file__))



    def loadJson(self, file):
        """
        Loads the given json file
        Args:
            file: (String) Path to the json file

        Returns: JsonData

        """
        if os.path.isfile(file):
            with open(file, 'r') as f:
                # The JSON module will read our file, and convert it to a python dictionary
                data = json.load(f)
                return data
        else:
            return None

    def dumpJson(self, data, file):
        """
        Saves the data to the json file
        Args:
            data: Data to save
            file: (String) Path to the json file

        Returns: None

        """

        with open(file, "w") as f:
            json.dump(data, f, indent=4)


    def loadVersionNotes(self, jsonFile, version=None):
        # oldname getVersionNotes
        """
        Returns: [versionNotes, playBlastDictionary]
        """
        jsonInfo = self.loadJson(jsonFile)
        return jsonInfo["Versions"][version][1], jsonInfo["Versions"][version][4]

    def addVersionNotes(self, additionalNote, jsonFile, version, user):
        jsonInfo = self.loadJson(jsonFile)
        currentNotes = jsonInfo["Versions"][version][1]
        ## add username and date to the beginning of the note:
        now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M")
        completeNote = "%s\n[%s] on %s\n%s\n" % (currentNotes, user, now, additionalNote)
        jsonInfo["Versions"][version][1] = completeNote
        ##
        self.dumpJson(jsonInfo, jsonFile)

    def initUsers(self, dbfilePath):
        # old Name
        if not os.path.isfile(dbfilePath):
            userDB = {"Generic": "gn"}
            self.dumpJson(userDB, dbfilePath)
            return userDB
        else:
            userDB = self.loadJson(dbfilePath)
            return userDB

    def addUser(self, fullName, initials):
        # old Name
        currentDB, dbFile = self.initUsers()
        initialsList = currentDB.values()
        if initials in initialsList:
            msg="Initials are in use"
            print msg
            return -1, msg
        currentDB[fullName] = initials
        self.dumpJson(currentDB, dbFile)
        self.userList = currentDB
        return None, None

    def removeUser(self, fullName):
        # old Name removeUser
        currentDB, dbFile = self.initUsers()
        del currentDB[fullName]
        self.dumpJson(currentDB, dbFile)
        self.userList = currentDB

    def loadPBSettings(self, pbSettingsFile):
        # old Name getPBsettings

        # pbSettingsFile = os.path.normpath(os.path.join(self.project_Path, "Playblasts", "PBsettings.json"))

        if not os.path.isfile(pbSettingsFile):
            defaultSettings = {"Resolution": (1280, 720),  ## done
                               "Format": 'avi',  ## done
                               "Codec": 'IYUV',  ## done
                               "Percent": 100,  ## done
                               "Quality": 100,  ## done
                               "ShowFrameNumber": True,
                               "ShowSceneName": False,
                               "ShowCategory": False,
                               "ShowFrameRange": True,
                               "ShowFPS": True,
                               "PolygonOnly": True,  ## done
                               "ShowGrid": False,  ## done
                               "ClearSelection": True,  ## done
                               "DisplayTextures": True,  ## done
                               "WireOnShaded": False,
                               "UseDefaultMaterial": False,
                               }
            self.dumpJson(defaultSettings, pbSettingsFile)
            return defaultSettings
        else:
            pbSettings = self.loadJson(pbSettingsFile)
            return pbSettings

    def savePBSettings(self, pbSettingsDict):
        # old Name setPBsettings
        pbSettingsFolder = os.path.normpath(os.path.join(self.project_Path, "Playblasts"))
        folderCheck(pbSettingsFolder)
        pbSettingsFile = os.path.join(pbSettingsFolder, "PBsettings.json")
        self.dumpJson(pbSettingsDict, pbSettingsFile)
        return

    def loadUserPrefs(self):
        # old Name userPrefLoad

        settingsFilePath = os.path.join(self.userSettings_Path, "smSettings.json")
        if os.path.isfile(settingsFilePath):
            settingsData = self.loadJson(settingsFilePath)
        else:
            settingsData = {"currentTabIndex": 0, "currentSubIndex": 0, "currentUser": "", "currentMode": 0}
            folderCheck(self.userSettings_Path)
            self.dumpJson(settingsData, settingsFilePath)
        return settingsData

    def saveUserPrefs(self, tabIndex, subIndex, user, mode):
        # old Name userPrefSave
        settingsFilePath = os.path.normpath(os.path.join(self.userSettings_Path, "smSettings.json"))

        settingsData = {"currentTabIndex": tabIndex,
                        "currentSubIndex": subIndex,
                        "currentUser": user,
                        "currentMode": mode}
        self.dumpJson(settingsData, settingsFilePath)

    def loadFavorites(self):
        # old Name userFavoritesLoad
        bookmarksFilePath = os.path.join(self.userSettings_Path, "smBookmarks.json")
        if os.path.isfile(bookmarksFilePath):
            bookmarksData = self.loadJson(bookmarksFilePath)
        else:
            bookmarksData = []
            self.dumpJson(bookmarksData, bookmarksFilePath)
        return bookmarksData, bookmarksFilePath

    def addToFavorites(self, shortName, absPath):
        # old Name userFavoritesAdd
        data, filePath = self.loadFavorites()
        data.append([shortName, absPath])
        self.dumpJson(data, filePath)
        return data

    def removeFromFavorites(self, index):
        # old Name userFavoritesRemove
        data, filePath = self.loadFavorites()
        del data[index]
        self.dumpJson(data, filePath)
        return data
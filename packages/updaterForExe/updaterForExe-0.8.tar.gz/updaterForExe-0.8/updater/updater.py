import firebasePort, json, sys, os, urllib.request, subprocess, requests, zipfile, shutil
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtGui
from PyQt5.Qt import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyle

'''Main class for updater'''
class Update(object):
    '''Initialise (optional-)arguments and make them self'''
    def __init__(self, config, webAppUrl, appName, path, debugPath = None, displayErrorMessages = True, autoUpdate = False, assetsFolder = False, assetsFolderUrl = None, updateAssetsArg=1):
        self.config = config
        self.serverDomain = config['authDomain']
        self.webAppUrl = webAppUrl
        self.appName = appName
        self.displayErrorMessages = displayErrorMessages
        self.autoUpdate = autoUpdate
        self.path = path
        self.debugPath = debugPath
    
        #Check if program is in exe; if true deactivate debugPath for library
        if getattr(sys, 'frozen', False):
            dir_ = os.path.dirname(sys.executable)
        else:
            dir_ = self.debugPath
        
        if assetsFolder is True:
            self.applicationDir = f'{dir_}/assets'
            self.assetsFolderUrl = assetsFolderUrl
        else:
            self.applicationDir = dir_

        #Sets when the assets folder should be updated
        self.updateAssetsArg = updateAssetsArg

    '''Function to check for Updates'''
    def checkUpdate(self):
        #Check internet connection
        if not self.internet_connection(self.serverDomain):
            if self.displayErrorMessages:
                MessageBox.newMessageBox(error='server_timeout')
            return
        
        #Get application version from firebase database
        self.firebase = firebasePort.Database(self.config)
        cloudVersion = self.firebase.getData(self.path)
        
        #Check if version.json existst and read current application version
        if os.path.exists(f'{self.applicationDir}/version.json'):
            with open(f'{self.applicationDir}/version.json', 'r') as json_file:
                data = json.load(json_file)
                localVersion = data['program']['version']
                skipVersion = data['program']['skipversion']
        else:
            os.mkdir(self.applicationDir)
            data = {'program': {'version': '0.0.1', 'skipversion': '0.0.0'}}
            localVersion = data['program']['version']
            skipVersion = data['program']['skipversion']
            with open(f'{self.applicationDir}/version.json', 'w') as f:
                json.dump(data, f)

        #Check if the user decided to skip the version earlier        
        if cloudVersion == skipVersion:
            return

        localVersion = localVersion.split('.')
        cloudVersion = cloudVersion.split('.')      

        #Check what type of update it is
        if cloudVersion[0] > localVersion[0]:
            type_ =  3
        elif cloudVersion[1] > localVersion[1]:
            type_ = 2
        elif cloudVersion[2] > localVersion[2]:
            type_ = 1 
        else:
            return 'No update'

        #Check if autoupdate is enabled; if not: display message
        if not self.autoUpdate:
            retval = MessageBox.newMessageBox(type_, '.'.join(localVersion), '.'.join(cloudVersion))
        else:
            retval = 0

        if retval == 0:
            self.updateApplication('.'.join(cloudVersion), type_)
        elif retval == 1:
            data['program']['skipversion'] = '.'.join(cloudVersion)
            with open('version.json', 'w') as g:
                json.dump(data, g)
        elif retval == 2:
            return

    '''Function to check the internet connection'''
    def internet_connection(self, domain):
        try:
            requests.get(f'https://{domain}', timeout=5)
            return True
        except requests.ConnectionError: 
            return False

    '''Function to update the assets folder'''
    def updateAssetsFolder(self, nv):
        #Checks if program is in exe and gets the application path
        if getattr(sys, 'frozen', False):
            dir_path = os.path.dirname(sys.executable)            
        else:
            dir_path = self.debugPath

        #Deletes the old assets folder
        shutil.rmtree(f'{dir_path}/assets')

        #Dowloading the new assets folder as .zip
        urllib.request.urlretrieve(self.assetsFolderUrl, f'{dir_path}/new_assets.zip')

        #Unpacks the zip
        with zipfile.ZipFile(f'{dir_path}/new_assets.zip', 'r') as zip_ref:
            zip_ref.extractall()

        #Removes the old zip file
        os.remove(f'{dir_path}/new_assets.zip')

    '''Function to update the application'''
    def updateApplication(self, nv, type_):
        #Check if the assets folder should be updated
        if type_ =< self.updateAssetsArg  and self.assetsFolderUrl is not None:
            self.updateAssetsFolder(nv)

        #Check if program is exe and download new version of the app
        if getattr(sys, 'frozen', False):
            dir_path = os.path.dirname(sys.executable)
            urllib.request.urlretrieve(self.webAppUrl, f'{dir_path}/new_version.exe')
        else:
            urllib.request.urlretrieve(self.webAppUrl, f'{self.debugPath}/new_version.exe')

        #Updates the version in the version.json file
        with open(f'{self.applicationDir}/version.json', 'r') as json_file:
            data = json.load(json_file)
            data['program']['version'] = nv
            with open(f'{self.applicationDir}/version.json', 'w') as g:
                json.dump(data, g)

        #Creates a .bat file to rename the old version and delete the old one
        if getattr(sys, 'frozen', False):
            with open('rename.bat', 'w') as rn:
                rn.write(f'''
                    timeout 1
                    del /f {self.appName}.exe
                    ren new_version*.exe {self.appName}.exe
                    {self.appName}.exe
                ''')
            subprocess.Popen(['rename.bat'], shell=False)
        else:
            with open(f'{self.debugPath}/rename.bat', 'w') as rn:
                rn.write(f'''
                    timeout 1
                    del /f {self.appName}.exe
                    ren new_version*.exe {self.appName}.exe
                    {self.appName}.exe
                    del /f rename.bat
                ''')
            subprocess.Popen([f'{self.debugPath}/rename.bat'], shell=False)

        #Exit the process
        sys.exit()

'''Class to display the message box'''
class MessageBox(QMessageBox):
    def __init__(self, type_, lv, cv, error):
        super(MessageBox, self).__init__() 
        if error is None:
            self.setIcon(QMessageBox.Information)
            self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_BrowserReload')))
            self.setWindowTitle('Update application')
            self.addButton("Update", QMessageBox.NoRole)
            self.addButton("Skip version", QMessageBox.NoRole)
            self.addButton("Ask later", QMessageBox.NoRole)
            
            self.setText('Would you like to update the application to a newer version?')
            self.setInformativeText(f"<b>{lv} >>> {cv}</b>")
        else:
            if error == 'version_not_found':
                self.setIcon(QMessageBox.Information)
                self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxCritical')))
                self.setWindowTitle('File not found!')
                self.setText('<b>version.json</b> file not found. Can\'t check for updates!')
            elif error == 'server_timeout':
                self.setIcon(QMessageBox.Information)
                self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxWarning')))
                self.setWindowTitle('Server timeout!')
                self.setText('Couldn\'t connect with the server! Unable to check for updates!')

    @staticmethod
    def newMessageBox(type_ = None, lv = None, cv = None, error = None):
        app = QApplication(sys.argv)
        app.exec_
        MessageBoxInstance = MessageBox(type_, lv, cv, error)
        retval = MessageBoxInstance.exec_()
        return retval
    
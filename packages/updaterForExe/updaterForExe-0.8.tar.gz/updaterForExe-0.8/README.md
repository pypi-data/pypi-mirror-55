## **Updater for exe with firebase**

## **Use**

```python
import updater

myUpdater = updater.Update(config, webAppUrl, appName, path, optional: debugPath, displayErrorMessages, autoUpdate, assetsFolder, assetsFolderUrl, updateAssetsArg)

myUpdater.checkUpdate()

#Rest of your code
```

##### config:
This is your standard config to use when you're working with firebase.

##### webAppUrl:
Your URL to your new version of the appliecation (example.com/new_version.exe).

##### appName:
The name of your application or exe name.

##### path:
The path in your realtime database to check for a new version.


##### debugPath:
The path to your project when you are still developing in python console.

##### displayErrorMessages:
If set to True: Messages like 'No internet connection' will appear.

##### autoUpdate:
If set to True, the user won't be asked to update or not.

##### assetsFolder:
Set this to true if the assets folder should be updated too. Also the version.json file will be saved there.

##### assetsFolderUrl:
If 'assetsFolder' is true, you have to specify the URL to your assets folder online (example.com/new_assets.zip)

##### updateAssetsArg:
If set to 1: The assets folder will be updated at X.X.X
If set to 2: The assets folder will only be updated at X.X.0
If set to 3: The assets folder will only be updated at X.0.0


### **Example**
```python
import updater

config = {
    "apiKey": "YOUR-API-KEY",
    "authDomain": "YOU-PROJECT-NAME.firebaseapp.com",
    "databaseURL": "https://YOU-PROJECT-NAME.firebaseio.com",
    "storageBucket": "YOU-PROJECT-NAME.appspot.com",
    "tls": {
        "rejectUnauthorized": False
        }
    }

url = 'example.com/index.exe'
assetsUrl = 'example.com/assets.zip'

myUpdater = updater.Update(config, url, 'index', '/program/version', debugPath='C:/Users/user/Documents/Python/Updater', displayErrorMessages=True, autoUpdate=False, assetsFolder=True, assetsFolderUrl=assestUrl, updateAssetsArg=2)

myUpdater.checkUpdate()

#Rest of your code
```

## **Use with pyinstaller**
When you want to convert the python file to an executable using py installer, you need additional hooks to use firebase and gcloud. For that you need to create a new python file at some directory NAMED 'hook-gcloud.py' with the following code:

```python
from PyInstaller.utils.hooks import copy_metadata
datas = copy_metadata('gcloud')
```

When you want to convert the file into an executable you have to add the argument '--additional-hooks-dir _the directory to the hook-gcloud.py file_'. 

Example:

```
pyinstaller --onfeile --additional-hooks-dir C:\Users\user\hooks index.py
```




![](/assets/logo.ico)

DreadHungerServerGUI is a python application created with Dear Pygui to give the user a GUI for hosting Dread Hunger servers on their machine.

## Getting started

To start a server using DreadHungerServerGUI, you will need to have port 7777 open / port forwarded, this is different for each isp (internet service provider). 
Here is a [general guide](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide) to help you get started.

### Loading Javascript Mods
DreadHungerServerGUI now has support for loading js mods with frida. Just place frida.dll, frida.config and the Patches folder into your server files (In the same folder as DreadHungerServer.exe). *If you dont know where to get frida, you can download them [here](https://github.com/Zentifyyy/DreadHungerServerMods) along with some javascript patches translated into English*. Then when launching the server, you can tick the mod loader checkbox. Make sure you only have the patches you want in the Patches directory.

### Downloading and running using python
- Firstly, make sure you have python installed, if not, [go here](https://www.python.org/downloads/)
- Then install dependencies using ```pip install dearpygui```,```pip install psutil``` and ```pip install DLL-Injector``` - [DLL Injector](https://pypi.org/project/DLL-Injector/) is only needed for mod loading.
- Clone this repository by pressing the blue <> CODE button on github and pressing Download ZIP, or by running ```git clone https://github.com/Zentifyyy/DreadHungerServerGUI.git``` in your desired terminal / command prompt.
- Then you can run the GUI by opening the file using python or running ```python3 script.py``` in your desired terminal / command prompt.

### Using releases
- Go to [the releases tab](https://github.com/Zentifyyy/DreadHungerServerGUI/releases) and download the latest release.


## Notes
- DreadHungerServerGUI uses [Dear Pygui](https://github.com/hoffstadt/dearpygui) for the gui
- DreadHungerServerGUI uses the [Roboto](https://fonts.google.com/specimen/Roboto) font, under the [Open Font License](https://openfontlicense.org/open-font-license-official-text/).

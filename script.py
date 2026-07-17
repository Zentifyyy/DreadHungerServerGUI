import dearpygui.dearpygui as dpg
import asyncio
import os

class Globals():
    ServerProc = asyncio.subprocess.Process
    ServerPath = ""
    ModLoader = False
    LogPath = ""
    HasOpenedBefore = False
    ConsoleText = ""
    MapCode = "Expanse_Persistent"
    DaysUntilBlizzard = 3
    DayMinutes = 8
    MaxPlayers = 8
    ThrallCount = 3
    PredatorDamage = 1
    CoalBurnRate = 1
    ColdIntensity = 1
    HungerRate = 1
    ConsoleUpdateRate = 0.1
    InjectDelay = 0.1

def save_prefs():
    Globals.HasOpenedBefore = True
    with open("prefs.ini", 'w') as f:
        f.write(f"{Globals.ServerPath}\n{Globals.LogPath}\n{Globals.HasOpenedBefore}")
        f.close()

if not os.path.exists("prefs.ini"):
    with open("prefs.ini",mode='w') as f:
        f.close()

with open("prefs.ini",mode='r') as f:
    content = f.read().splitlines()
    try:
        if os.path.exists(content[0]):
            Globals.ServerPath = content[0]
        if os.path.exists(content[1]):
            Globals.LogPath = content[1]
        Globals.HasOpenedBefore = content[2] == "True"
    except: f.close()
    f.close()

def set_server_path():
    try:
        from tkinter import filedialog
        Globals.ServerPath = filedialog.askopenfile().name
        set_console_text(f"Server path set to: {Globals.ServerPath}")
    except: 
        set_console_text("User canceled file selection")
    
    Globals.LogPath = Globals.ServerPath.removesuffix("Server.exe") + "/Saved/Logs/OverlayLog.txt"

def set_console_text(text:str,append = False):
    if append:
        Globals.ConsoleText += text
    else:
        Globals.ConsoleText = text
    dpg.set_value("console_text", Globals.ConsoleText)


WindowWidth = 775
WindowHeight = 365

dpg.create_context()
dpg.create_viewport(title="Dread Hunger Server", width=WindowWidth, height=WindowHeight,large_icon="assets/logo.ico",small_icon="assets/logo.ico")
dpg.set_exit_callback(save_prefs)
dpg.configure_app( docking=True, docking_space=True, init_file="windows.ini")

with dpg.font_registry():
    default_font = dpg.add_font("assets/Roboto-Regular.ttf", 13)
    dpg.bind_font(font=default_font)

def server_starter():
    asyncio.run(start_server())

def kill_server():
    import psutil
    if Globals.ServerProc is None:
        return
    
    if Globals.ServerProc.pid:
        for child in psutil.Process(Globals.ServerProc.pid).children(recursive=True):
                child.kill()
    
        Globals.ServerProc.kill()

async def start_server():

    if Globals.ServerPath == "": 
        set_server_path()

    try:
        args = f"{Globals.MapCode}?maxplayers={Globals.MaxPlayers}?daysbeforeblizzard={Globals.DaysUntilBlizzard}?dayminutes={Globals.DayMinutes}?predatordamage={Globals.PredatorDamage}?coldintensity={Globals.ColdIntensity}?hungerrate={Globals.HungerRate}?coalburnrate={Globals.CoalBurnRate}?thralls={Globals.ThrallCount} -LOG=OverlayLog.txt nouniques"
        Globals.ServerProc = await asyncio.subprocess.create_subprocess_shell(
            f"{'"'}{Globals.ServerPath}{'"'} {args}"
        )
        dpg.configure_viewport("Dread Hunger Server",disable_close=True)
    except: 
        Globals.ServerPath = ""
        set_console_text("Server could not be started")

    try:
        await asyncio.sleep(Globals.InjectDelay)
        import dll_injector
        import psutil
        dll_injector.inject(Globals.ServerPath.removesuffix("DreadHungerServer.exe") + "frida.dll",process_pid=psutil.Process(Globals.ServerProc.pid).children(recursive=True)[1].pid)
    except:
        set_console_text("Frida could not be injected")              

    while not Globals.ServerProc.returncode:

        await asyncio.sleep(Globals.ConsoleUpdateRate)
        
        try:
            with open(Globals.LogPath,'r') as f: s = f.read()
            set_console_text(s,append=True)
        except:
            set_console_text("Log file not found")
            break

        dpg.set_y_scroll(item="console_window",value=dpg.get_y_scroll_max(item="console_window"))

        if dpg.is_key_pressed(dpg.mvKey_Escape):
            set_console_text("Server Interupted")
            break

    dpg.configure_viewport("Dread Hunger Server",disable_close=False)
    kill_server()

def set_settings(sender,app_data):
    match sender:
        case "map":
            if app_data == "Approach": 
                Globals.MapCode = "Approach_Persistent"
            elif app_data == "The Summit":
                Globals.MapCode = "Departure_Persistent"
            else: Globals.MapCode = "Expanse_Persistent"
        case "blizzdays":
            Globals.DaysUntilBlizzard = app_data
        case "daymins":
            Globals.DayMinutes = app_data
        case "maxplayers":
            Globals.MaxPlayers = app_data
        case "thralls":
            Globals.ThrallCount = app_data
        case "preddamage":
            Globals.PredatorDamage = round(app_data,3)
        case "coalburn":
            Globals.CoalBurnRate = round(app_data,3)
        case "coldintens":
            Globals.ColdIntensity= round(app_data,3)
        case "hunger":
            Globals.HungerRate = round(app_data,3)
        case "mods":
            Globals.ModLoader = app_data

def set_console_delay(sender,app_data):
    Globals.ConsoleUpdateRate = round(app_data,2)

def set_inject_delay(sender,app_data):
    Globals.InjectDelay = round(app_data,2)


with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="Set Server Path", callback=set_server_path)
        dpg.add_menu_item(label="Save Prefs",callback=save_prefs)
        dpg.add_slider_float(label="Console Update Delay" ,format='%.1f', callback=set_console_delay,default_value=0.1,min_value=0.1,max_value=2,width=100)
        dpg.add_slider_float(label="Frida Inject Delay" ,format='%.1f', callback=set_inject_delay,default_value=0.1,min_value=0.1,max_value=2,width=100)
        dpg.add_text("If experiencing high cpu usage, increase Console Update Delay\nIf experiencing frida inject errors, increase Frida Inject Delay", wrap=250)
        
    with dpg.menu(label="About"):
        dpg.add_menu_item(label="About",callback=lambda:dpg.configure_item("about", show=True))

with dpg.window(label="Console",width=WindowHeight,height=WindowWidth,no_close=True,tag="console_window",on_close=save_prefs):
    dpg.add_text(label="",tag="console_text",wrap=WindowWidth)

with dpg.window(label="Start Server",width=WindowWidth,height=WindowHeight,no_close=True):

    dpg.add_combo(items=("Approach","The Expanse","The Summit"),label="Select A Map",width=150,callback=set_settings,tag="map",default_value="Approach")
    dpg.add_slider_int(label="Days Until Blizzard",default_value=3,min_value=1,max_value=10,width=150, callback=set_settings ,tag="blizzdays")
    dpg.add_slider_int(label="Day Minutes",default_value=8,min_value=1,max_value=50,width=150,callback=set_settings ,tag="daymins")
    dpg.add_text("Player Settings")
    dpg.add_slider_int(label="Max Players",default_value=8,min_value=1,max_value=8,width=150, callback=set_settings ,tag="maxplayers")
    dpg.add_slider_int(label="Thrall Count",default_value=3,min_value=1,max_value=8,width=150, callback=set_settings ,tag="thralls")
    
    dpg.add_text("Difficulty Settings")

    dpg.add_slider_float(label="Predator Damage",default_value=1,min_value=0,max_value=2,format='%.1f',width=150, callback=set_settings ,tag="preddamage")
    dpg.add_slider_float(label="Coal Burn Rate",default_value=1,min_value=0,max_value=2,format='%.1f',width=150, callback=set_settings ,tag="coalburn")
    dpg.add_slider_float(label="Cold Intensity",default_value=1,min_value=0,max_value=2,format='%.1f',width=150, callback=set_settings ,tag="coldintens")
    dpg.add_slider_float(label="Hunger Rate",default_value=1,min_value=0,max_value=2,format='%.1f',width=150, callback=set_settings ,tag="hunger")

    with dpg.group(horizontal=True):
        dpg.add_button(label="Start Server", callback=server_starter)
        dpg.add_checkbox(label="Frida Mod Loader", callback=set_settings, tag="mods")

with dpg.window(label="About",tag="about",no_docking=True,no_collapse=True,autosize=True, show=not Globals.HasOpenedBefore):
    dpg.add_text("To get started, select the settings you would like then press start server and select your DreadHungerServer exectutable.\nTo stop the server, hold the esc key.", wrap=500)
    dpg.add_button(label="Close", callback=lambda: dpg.configure_item("about", show=False))

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding,5)
        
dpg.bind_theme(global_theme)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
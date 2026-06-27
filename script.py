import dearpygui.dearpygui as dpg
from tkinter import filedialog
import asyncio
import os
import psutil
import time

WindowWidth = 775
WindowHeight = 347

class Globals():
    ServerProc = asyncio.subprocess.Process
    ServerPath = ""
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

dpg.create_context()
dpg.create_viewport(title='Dread Hunger Server', width=WindowWidth, height=WindowHeight,large_icon="assets/logo.ico",small_icon="assets/logo.ico")
dpg.set_exit_callback(save_prefs)
dpg.configure_app( docking=True, docking_space=True, init_file="windows.ini")

with dpg.font_registry():
    default_font = dpg.add_font("assets/Roboto-Regular.ttf", 13)
    dpg.bind_font(font=default_font)

def server_starter():
    asyncio.run(start_server())

def kill_process():
    for child in psutil.Process(Globals.ServerProc.pid).children(recursive=True):
            child.kill()
    
    Globals.ServerProc.kill()

async def start_server():

    try:
        if Globals.ServerPath == "": Globals.ServerPath = filedialog.askopenfile().name
    except: 
        Globals.ConsoleText += "User canceled file selection\n"
        dpg.set_value("console_text", Globals.ConsoleText)

    Globals.LogPath = Globals.ServerPath.removesuffix("Server.exe") + "/Saved/Logs/OverlayLog.txt"

    try:
        Globals.ServerProc = await asyncio.subprocess.create_subprocess_shell(
            f"{Globals.ServerPath} {Globals.MapCode}?maxplayers={Globals.MaxPlayers}?daysbeforeblizzard={Globals.DaysUntilBlizzard}?dayminutes={Globals.DayMinutes}?predatordamage={Globals.PredatorDamage}?coldintensity={Globals.ColdIntensity}?hungerrate={Globals.HungerRate}?coalburnrate={Globals.CoalBurnRate}?thralls={Globals.ThrallCount} -LOG=OverlayLog.txt nouniques"
        )
    except: 
        Globals.ServerPath = ""
        Globals.ConsoleText += "Server could not be started\n"
        dpg.set_value("console_text", Globals.ConsoleText)

    while not Globals.ServerProc.returncode:

        time.sleep(0.05)
        try:
            with open(Globals.LogPath) as f: s = f.read()
            Globals.ConsoleText = s
            dpg.set_value("console_text", Globals.ConsoleText)
        except:
            Globals.ConsoleText = "Log file not found"
            dpg.set_value("console_text", Globals.ConsoleText)
            break

        dpg.set_y_scroll(item="console_window",value=dpg.get_y_scroll_max(item="console_window"))

        if dpg.is_key_pressed(dpg.mvKey_Escape):
            Globals.ConsoleText = "Server Interupted"
            dpg.set_value("console_text", Globals.ConsoleText)
            break

    kill_process()
    
    

def set_map(map: str):
    if map == "Approach": 
        Globals.MapCode = "Approach_Persistent"
    elif map == "The Summit":
        Globals.MapCode = "Departure_Persistent"
    else: map = "Expanse_Persistent"

def set_days_until_blizz(days:int):
    Globals.DaysUntilBlizzard = days

def set_day_mins(mins:int):
    Globals.DayMinutes = mins

def set_max_players(players:int):
    Globals.MaxPlayers = players

def set_thralls(thralls:int):
    Globals.ThrallCount = thralls

def set_pred_damage(preddamage:int):
    Globals.PredatorDamage = preddamage

def set_coal_burn_rate(burnrate:int):
    Globals.CoalBurnRate = burnrate

def set_cold_intensity(cold:int):
    Globals.ColdIntensity= cold

def set_hunger(hunger:int):
    Globals.HungerRate = hunger

with dpg.window(label="Console",width=WindowHeight,height=WindowWidth,no_close=True,tag="console_window"):
    dpg.add_text(label="",tag="console_text",wrap=WindowWidth)

with dpg.window(label="Start Server",width=WindowWidth,height=WindowHeight,no_close=True, on_close=save_prefs):
    dpg.add_combo(items=("Approach","The Expanse","The Summit"),label="Select A Map",width=150,callback=set_map,default_value="Approach")
    dpg.add_slider_int(label="Days Until Blizzard",default_value=3,min_value=1,max_value=10,width=150, callback=set_days_until_blizz)
    dpg.add_slider_int(label="Day Minutes",default_value=8,min_value=1,max_value=50,width=150,callback=set_day_mins)
    dpg.add_text("Player Settings")
    dpg.add_slider_int(label="Max Players",default_value=8,min_value=1,max_value=8,width=150, callback=set_max_players)
    dpg.add_slider_int(label="Thrall Count",default_value=3,min_value=1,max_value=8,width=150, callback=set_thralls)
    
    dpg.add_text("Difficulty Settings")

    dpg.add_slider_float(label="Predator Damage",default_value=1,min_value=0,max_value=2,format='%.2f',width=150, callback=set_pred_damage)
    dpg.add_slider_float(label="Coal Burn Rate",default_value=1,min_value=0,max_value=2,format='%.2f',width=150, callback=set_coal_burn_rate)
    dpg.add_slider_float(label="Cold Intensity",default_value=1,min_value=0,max_value=2,format='%.2f',width=150, callback=set_cold_intensity)
    dpg.add_slider_float(label="Hunger Rate",default_value=1,min_value=0,max_value=2,format='%.2f',width=150, callback=set_hunger)

    dpg.add_button(label="Start Server", callback=server_starter)

if not Globals.HasOpenedBefore:
    with dpg.window(label="Getting Started",tag="getting_started",no_docking=True,no_collapse=True,autosize=True):
        dpg.add_text("To get started, select the settings you would like then press start server and select your DreadHungerServer exectutable.\nTo stop the server, press the esc key.", wrap=500)
        dpg.add_button(label="Close", callback=lambda: dpg.configure_item("getting_started", show=False))

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):

        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding,5)
        

dpg.bind_theme(global_theme)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
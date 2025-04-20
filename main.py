import keyboard
import screen
import time
import uos
import machine
import sdcard
import json
import network
import programRun




kb = keyboard.KeyBoard()
scr = screen.Screen()
nic = network.WLAN(network.WLAN.IF_STA)

scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
scr.txt("Welcome to", 0, 0, 255, 255, 255, 0, 0, 0)
scr.txt("CardOS by Noah", 0, 33, 255, 255, 255, 0, 0, 0)
scr.txt("Scarborough.", 0, 66, 255, 255, 255, 0, 0, 0)
scr.txt("o to continue.", 0, 99, 255, 255, 255, 0, 0, 0)

while True:
    if "o" in kb.get_pressed_keys():
        break
    time.sleep(0.02)

scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
scr.txt("Press y when SD", 0, 0, 255, 255, 255, 0, 0, 0)
scr.txt("card is", 0, 33, 255, 255, 255, 0, 0, 0)
scr.txt("inserted.", 0, 66, 255, 255, 255, 0, 0, 0)

while True:
    if "y" in kb.get_pressed_keys():
        break
    time.sleep(0.02)

try:
    sd = sdcard.SDCard(machine.SoftSPI(sck=40, miso=39, mosi=14), machine.Pin(12))
    vfs = uos.VfsFat(sd)
except OSError:
    scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
    scr.txt("No SD card.", 0, 0, 255, 255, 255, 0, 0, 0)
    scr.txt("Please restart.", 0, 33, 255, 255, 255, 0, 0, 0)
    exit()
programList = []

def makeProgramList():
    global programList
    uos.mount(vfs, '/sd')
    programList = uos.listdir("/sd")
    uos.umount('/sd')
    if "preferences.txt" in programList:
        programList.remove("preferences.txt")


makeProgramList()


def drawMenuScreen(title, options, selected, margin=2, marginText1=""):
    scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
    marginText = marginText1 + ""
    while len(marginText) < margin * 4:
        marginText += " "
    scr.txt(title, 0, 0, 255, 255, 255, 0, 0, 0)
    try:
        scr.txt(options[0], 0, 33, 255, 255, 255, 0, 0, 0)
        scr.txt(options[1], 0, 66, 255, 255, 255, 0, 0, 0)
        scr.txt(options[2], 0, 99, 255, 255, 255, 0, 0, 0)
    except IndexError:
        pass
    scr.txt(marginText[0:2], 240-32, 00, 255, 255, 255, 0, 0, 0)
    scr.txt(marginText[2:4], 240-32, 33, 255, 255, 255, 0, 0, 0)
    scr.txt(marginText[4:6], 240-32, 66, 255, 255, 255, 0, 0, 0)
    scr.txt(marginText[6:], 240-32, 99, 255, 255, 255, 0, 0, 0)
    
    scr.txt(options[selected], 0, 33*(selected+1), 0, 0, 0, 255, 255, 255)


def getKey():
    while True:
        pressed = kb.get_pressed_keys()
        if len(pressed) > 0:
            return pressed
        time.sleep(0.02)


def pad2Digits(x):
    y = x + ""
    while len(y) < 2:
        y = "0" + y
    return y

class Cardos:
    def __init__(self, scr, slct, gk, edt, entry, keyb):
        self.scr = scr
        self.select = slct
        self.getKey = gk
        self.editText = edt
        self.textEntry = entry
        self.kb = keyb


def runProgram(prg):
    uos.mount(vfs, "/sd")
    with open("/sd/" + prg, "rt") as f:
        result = programRun.run(f.read(), Cardos(scr, select, getKey, editText, textEntry, kb))
    uos.umount("/sd")
    if result:
        editText("Error", "Escape to exit\n" + result.replace("<string>", prg))


def mainMenu():
    cursor = 0
    while True:
        if len(programList) > 0:
            drawMenuScreen("o for options", programList[cursor:], 0, 2, "")
        else:
            scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
            scr.txt("No programs.", 0, 0, 255, 255, 255, 0, 0, 0)
            scr.txt("Press o for", 0, 33, 255, 255, 255, 0, 0, 0)
            scr.txt("options.", 0, 66, 255, 255, 255, 0, 0, 0)
        k = getKey()[0]
        if k == "o":
            options()
        if k == ".":
            cursor += 1
        if k == ";":
            cursor -= 1
        if k == "ENT":
            runProgram(programList[cursor])
        if len(programList) > 0:
            cursor %= len(programList)


def select(title, items):
    cursor = 0
    while True:
        drawMenuScreen(title, items[cursor:], 0, 0, "")
        k = getKey()[0]
        if k == ".":
            cursor += 1
        elif k == ";":
            cursor -= 1
        elif k == "ENT":
            return cursor
        time.sleep(0.1)
        cursor %= len(items)


def options():
    while True:
        o = select("Options", ["Exit", "Connect to WiFi", "Settings", "Create Program", "Edit Program", "Delete Program", "Disconnect WiFi"])
        if o == 0: # Exit
            break
        if o == 1: # connect to WiFi
            if preferences.data["WiFi"][0] == "":
                time.sleep(0.3)
                select("Invalid Setting", ["OK"])
                time.sleep(0.3)
            scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
            scr.txt("Connecting", 0, 0, 255, 255, 255, 0, 0, 0)
            nic.active(True)
            nic.connect(preferences.data["WiFi"][0], preferences.data["WiFi"][1])
            time.sleep(0.3)
        if o == 2: # Settings
            settings()
        if o == 3: # Create Program
            time.sleep(0.3)
            name = textEntry("Name w/o .py")
            for x in "/`\"',. ":
                name = name.replace(x, "")
            if name == "":
                select("Invalid name", ["OK"])
                time.sleep(0.3)
                return
            uos.mount(vfs, "/sd")
            filename = "/sd/" + name + ".py"
            with open(filename, "wt") as f:
                f.write("")
            uos.umount("/sd")
            makeProgramList()
            time.sleep(0.3)
        if o == 4: # Edit Program
            editor()
        if o == 5: # Delete Program
            time.sleep(0.3)
            prg = select("What to delete?", ["Cancel Deletion"] + programList)
            time.sleep(0.3)
            if prg == 0:
                continue
            confirm = select(programList[prg-1], ["Keep", "Delete"])
            time.sleep(0.3)
            if confirm > 0:
                uos.mount(vfs, "/sd")
                uos.remove("/sd/" + programList[prg-1])
                uos.umount("/sd")
                makeProgramList()
        if o == 6:
            time.sleep(0.3)
            scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
            scr.txt("Disconnecting", 0, 0, 255, 255, 255, 0, 0, 0)
            nic.disconnect()
            nic.active(False)
            time.sleep(0.3)


def editText(title, txt1):
    shift = ""
    txt = txt1 + ""
    cursor = 0
    while True:
        scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
        scr.txt(title, 0, 0, 255, 255, 255, 0, 0, 0)
        txtLines = txt.split("\n")
        currentLine = txt[:cursor].count("\n")
        cursorX = 0
        for c in txt[:cursor]:
            if c == "\n":
                cursorX = 0
            else:
                cursorX += 1
        try:
            if currentLine == 0:
                scr.txt(txtLines[currentLine][max([cursorX-6, 0]):], 0, 33, 255, 255, 255, 0, 0, 0)
                scr.txt(txtLines[currentLine+1][max([cursorX-6, 0]):], 0, 66, 255, 255, 255, 0, 0, 0)
                scr.txt(txtLines[currentLine+2][max([cursorX-6, 0]):], 0, 99, 255, 255, 255, 0, 0, 0)
            else:
                scr.txt(txtLines[currentLine-1][max([cursorX-6, 0]):], 0, 33, 255, 255, 255, 0, 0, 0)
                scr.txt(txtLines[currentLine][max([cursorX-6, 0]):], 0, 66, 255, 255, 255, 0, 0, 0)
                scr.txt(txtLines[currentLine+1][max([cursorX-6, 0]):], 0, 99, 255, 255, 255, 0, 0, 0)
        except IndexError:
            pass
        if currentLine == 0:
            scr.fillRect(16*min([6, cursorX]), 64, 16, 2, 255, 255, 255)
        else:
            scr.fillRect(16*min([6, cursorX]), 97, 16, 2, 255, 255, 255)
        if shift == "shift":
            scr.txt("^", 224, 0, 255, 255, 255, 0, 0, 0)
        if shift == "function":
            scr.txt("F", 224, 0, 255, 255, 255, 0, 0, 0)
        k = getKey()[0]
        if len(k) == 1:
            if shift != "function":
                if cursor > len(txt):
                    if shift == "shift":
                        txt += keyboard.shifted(k)
                    else:
                        txt += k
                else:
                    if shift == "shift":
                        txt = txt[:cursor] + keyboard.shifted(k) + txt[cursor:]
                    else:
                        txt = txt[:cursor] + k + txt[cursor:]
                cursor += 1
            else:
                if k == ",":
                    cursor -= 1
                elif k == "/":
                    cursor += 1
                elif k == ".":
                    cursor += len(txtLines[currentLine]) + 1
                elif k == ";":
                    cursor -= len(txtLines[currentLine]) + 1
                elif k == "`":
                    time.sleep(0.2)
                    return txt
        elif k == "SHIFT":
            if shift != "shift":
                shift = "shift"
            else:
                shift = ""
        elif k == "FN":
            if shift != "function":
                shift = "function"
            else:
                shift = ""
        elif k == "BSPC":
            if len(txt) > 0 and cursor > 0:
                txt = txt[:cursor-1] + txt[cursor:]
                cursor -= 1
        elif k == "ENT":
            txt = txt[:cursor] + "\n" + txt[cursor:]
            cursor += 1
        elif k == "SPC":
            txt = txt[:cursor] + " " + txt[cursor:]
            cursor += 1
        cursor %= len(txt) + 1
        time.sleep(0.1)


def editor():
    filename = programList[select("Choose File", programList)]
    uos.mount(vfs, "/sd")
    with open("/sd/" + filename, "rt") as f:
        content = f.read()
    uos.umount("/sd")
    newContent = editText(filename, content)
    time.sleep(0.3)
    if select("Unsaved Changes", ["Keep Changes", "Discard Changes"]) < 1:
        uos.mount(vfs, "/sd")
        with open("/sd/" + filename, "wt") as f:
            f.write(newContent)
        uos.umount("/sd")
    time.sleep(0.3)


def textEntry(prompt):
    text = ""
    shift = False
    while True:
        scr.fillRect(0, 0, scr.width, scr.height, 0, 0, 0)
        scr.txt(prompt, 0, 0, 255, 255, 255, 0, 0, 0)
        scr.txt(text+"_", 0, 33, 255, 255, 255, 0, 0, 0)
        if shift:
            scr.txt("^", 0, 66, 255, 255, 255, 0, 0, 0)
        k = getKey()[0]
        if len(k) == 1:
            if shift:
                k = keyboard.shifted(k)
            text += k
        else:
            if k == "ENT":
                time.sleep(0.3)
                return text
            if k == "BSPC":
                text = text[:-1]
            if k == "SPC":
                text += " "
            if k == "SHIFT":
                shift = not shift
        time.sleep(0.1)


class Preferences:
    def __init__(self):
        uos.mount(vfs, "/sd")
        try:
            with open("/sd/preferences.txt", "rt") as f:
                self.data = json.loads(f.read())
        except:
            with open("/sd/preferences.txt", "wt") as f:
                f.write("{}")
        uos.umount("/sd")
    def save(self):
        uos.mount(vfs, "/sd")
        with open("/sd/preferences.txt", "wt") as f:
            f.write(json.dumps(self.data))
        uos.umount("/sd")


def UTCTime(add=0):
    second = 1
    minute = 60 * second
    hour = 60 * minute
    return time.gmtime(time.time()-hour*7+hour*add)


def settings():
    while True:
        s = select("Settings", ["Exit", "WiFi"])
        if s == 0: # Exit
            break
        if s == 1: # Set WiFi
            time.sleep(0.3)
            WiFiCreds = []
            WiFiCreds.append(textEntry("SSID"))
            WiFiCreds.append(textEntry("Password"))
            preferences.data["WiFi"] = WiFiCreds
            preferences.save()


preferences = Preferences()
try:
    preferences.data["WiFi"]
except KeyError:
    preferences.data["WiFi"] = ["", ""]

try:
    preferences.data["Timezone"]
except KeyError:
    preferences.data["Timezone"] = 0
mainMenu()




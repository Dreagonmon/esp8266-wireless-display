import sys, os, time
from PIL import Image, ImageDraw, ImageFont
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(CURRENT_PATH, "..", "lib")))
from LCD12864Remote import LCD12864

import truck_telemetry

def hige_priority():
    """ Set the priority of the process to real-time."""
    import sys
    try:
        sys.getwindowsversion()
    except AttributeError:
        isWindows = False
    else:
        isWindows = True
    if isWindows:
        # Based on:
        #   "Recipe 496767: Set Process Priority In Windows" on ActiveState
        #   http://code.activestate.com/recipes/496767/
        import win32api,win32process,win32con
        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)
    else:
        import os
        os.nice(-10)

def pasteImage(img: Image, frame: LCD12864, invert=False):
    px = img.load()
    _pixel = frame.pixel
    for y in range(64):
        for x in range(128):
            color = 0 if (px[x,y]==0)!=invert else 1
            _pixel(x, y, color)

def parseInGameTime(time_in_minutes):
    min = time_in_minutes % 60
    hour = (time_in_minutes // 60) % 24
    day = (time_in_minutes // 60) // 24
    day_in_week = day // 7 # [0,6], Mon. to Sun.
    return day, day_in_week, hour, min

def mps_to_kmph(mps):
    return mps * 3.6

if __name__ == '__main__':
    hige_priority()
    # var
    screen = LCD12864(("192.168.31.203", 10086))
    screen.backlight(5)
    img = Image.new("1", (128, 64), 0)
    draw = ImageDraw.Draw(img)
    font8 = ImageFont.truetype(os.path.join(CURRENT_PATH, "guanzhi.ttf"), 8)
    font16 = ImageFont.truetype(os.path.join(CURRENT_PATH, "unifont-13.0.04.ttf"), 16)
    # resource
    icon_water_temperature = Image.open(os.path.join(CURRENT_PATH, "waterTemperature.bmp")).convert("1")
    icon_water_temperature.load()
    icon_cruise_control_speed = Image.open(os.path.join(CURRENT_PATH, "cruiseControlSpeed.bmp")).convert("1")
    icon_cruise_control_speed.load()
    # loop parameter
    _last = time.time_ns()
    try:
        truck_telemetry.init()
        _not_inited = False
    except:
        _not_inited = True
    while True:
        # limit fps about 20 fps (50ms/f), save CPU
        _now = time.time_ns()
        if (_now - _last) < 50_000_000:
            time.sleep(0.01)
            continue
        _last = _now
        if _not_inited:
            try:
                truck_telemetry.init()
                _not_inited = False
            except:
                # wait game to start
                continue
        data:dict = truck_telemetry.get_data()
        # draw image
        engineRpmMax = data["engineRpmMax"]
        engineRpm = data["engineRpm"]
        speed = mps_to_kmph(data["speed"])
        speedLimit = mps_to_kmph(data["speedLimit"])
        cruiseControlSpeed = mps_to_kmph(data["cruiseControlSpeed"])
        fuelCapacity = data["fuelCapacity"]
        fuel = data["fuel"]
        fuelAvgConsumption = data["fuelAvgConsumption"] # per km
        _, _, hour, minu = parseInGameTime(data["time_abs"])
        gear = data["gearDashboard"]
        waterTemperature = data["waterTemperature"]
        draw.rectangle((0,0,128,64), fill=0, width=0)
        # > time
        game_time = "{: >2}:{:0>2}".format(hour, minu)
        draw.text((64, 8), game_time, 1, font16, anchor="mm")
        # > gear
        gear_text = [
            "R6", "R5", "R4", "R3", "R2", "R1", "N",
            "1", "2", "3", "4", "5", "6", "7", "8",
            "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"][gear+6]
        draw.text((120, 8), gear_text, 1, font16, anchor="mm")
        # > rpm and speed
        draw.text((0, 0), "Rpm km/h", 1, font8, anchor="lt")
        draw.text((0, 8), "{:01.1f}".format(engineRpm/1000), 1, font8, anchor="lt")
        draw.text((24, 8), "{:.0f}".format(speed), 1, font8, anchor="mt")
        draw.line((30,16,34,16), fill=1, width=1)
        draw.text((42, 16), "120", 1, font8, anchor="mt")
        draw.line((30,40,34,40), fill=1, width=1)
        draw.text((42, 40), "60", 1, font8, anchor="mm")
        draw.line((30,63,34,63), fill=1, width=1)
        draw.text((42, 64), "0", 1, font8, anchor="mb")
        rpm_heoght = 0 if engineRpmMax == 0 else int(48 * engineRpm / engineRpmMax)
        draw.rectangle((0,64-rpm_heoght,14,64), fill=1, width=0)
        speed_height = int(48 * speed / 120)
        speed_height = 48 if speed_height > 48 else speed_height
        draw.rectangle((16,64-speed_height,30,64), fill=1, width=0)
        draw.arc((32,0,48,16), 135, 405, fill=1, width=1)
        draw.text((41, 8), "{:.0f}".format(speedLimit), 1, font8, anchor="mm")
        # > devided line
        draw.line((50,16,128,16), fill=1, width=1)
        # > water temperature
        draw.bitmap((48, 20), icon_water_temperature, fill=1)
        draw.text((92, 32), "{:.1f}".format(waterTemperature), 1, font16, anchor="mm")
        draw.text((120, 32), "°C", 1, font8, anchor="mm")
        # > cruise control speed
        draw.bitmap((48, 44), icon_cruise_control_speed, fill=1)
        draw.text((92, 56), "{:.0f}".format(cruiseControlSpeed), 1, font16, anchor="mm")
        draw.text((120, 56), "km/h", 1, font8, anchor="mm")
        # refresh screen
        pasteImage(img, screen)
        screen.show()
        print("refresh")
        # break

import asyncio
from pybooklid import LidSensor
from pywizlight import wizlight, PilotBuilder
import os

WIZ_LIGHT_IP = os.getenv("WIZ_LIGHT_IP")
if not WIZ_LIGHT_IP:
    raise ValueError("WIZ_LIGHT_IP is not set")

ANGLE_RANGE = [10, 110]

def map_angle_to_brightness(angle):
    angle_close, angle_open = ANGLE_RANGE
    angle = max(angle_close, min(angle_open, angle))        
    brightness = int((angle - angle_close) / (angle_open - angle_close) * (255 - 0) + 0)
    return brightness

async def main():
    print("macbook-lid-to-wiz: close the lid to dim the light. fun stuff!")

    light = wizlight(WIZ_LIGHT_IP)

    with LidSensor() as sensor:
        for angle in sensor.monitor(interval=0.5):
            if angle < 10:  # Nearly closed
                break
            
            brightness = map_angle_to_brightness(angle)
            angle_close = ANGLE_RANGE[0]

            print(f"  angle: {angle:.1f}°, brightness: {brightness}")
            if brightness > angle_close:
                await light.turn_on(PilotBuilder(brightness = brightness))
            else:
                await light.turn_off()

if __name__ == "__main__":
    asyncio.run(main())

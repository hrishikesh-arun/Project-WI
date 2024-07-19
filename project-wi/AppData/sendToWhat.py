import pywhatkit
from datetime import datetime


def send_to_group(number,animal,image_dir,location):
    # Configure Chrome options for headless mode
    pywhatkit.sendwhats_image(number,image_dir,
                              f"*ALERT!!!* Animal Trespassing DETECTED!!!\n\n*DETAILS*\n\nAnimal: {animal.capitalize()}\nLocation: Sector {location}\nTime: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}",tab_close = True, close_time = 3)

import random
import masterlist

def camera_versus_text():
    # Painotettu lista random pickeihin

    camera_list = masterlist.cameras

    weighted_camera_list = camera_list["Common"] * 10 + camera_list["Medium"] * 3 + camera_list["Rare"]
            
    return "{} vai {}?".format(random.choice(weighted_camera_list), random.choice(weighted_camera_list))

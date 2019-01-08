import random
import masterlist

def camera_versus_text():
    # Painotettu lista random pickeihin

    camera_list = masterlist.cameras

    weighted_camera_list = camera_list["Common"] * 20 + camera_list["Medium"] * 5 + camera_list["Rare"]

    camera1 = random.choice(weighted_camera_list)

    # Poistetaan ensimmäinen valinta listasta ettei tule tuplia
    weighted_camera_list = [x for x in weighted_camera_list if x != camera1]

    camera2 = random.choice(weighted_camera_list)
            
    return "{} vai {}?".format(camera1, camera2)

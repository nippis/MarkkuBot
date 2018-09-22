import random
#TODO masterlist

def camera_versus_text():
    # Painotettu lista random pickeihin

    global camera_list
    weighted_camera_list = camera_list["Common"] * 10 + camera_list["Medium"] * 3 + camera_list["Rare"]
            
    return "{} vai {}?".format(random.choice(weighted_camera_list), random.choice(weighted_camera_list))

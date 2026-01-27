from utils.adb_helper import auto_setup_adb, get_project_path
import time

region_pvp_finish = (484, 999, 531, 1028)
pvp_finish_image_path = get_project_path("img/pvp-finsh.png")
def test():
    # Configuration automatique de ADB
    adb = auto_setup_adb(verbose=False)
    while True:
        pvp_finish, similarity = adb.compare_region_with_image(
            reference_image_path=pvp_finish_image_path,
            region=region_pvp_finish,
            threshold=0.9,
        )

        if pvp_finish:
            print("found")
            time.sleep(0.5)
            break
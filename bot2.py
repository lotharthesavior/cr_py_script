import time
import cv2
import numpy as np
import psutil
import pywinauto
import random
from pywinauto.application import Application
from pprint import pprint

# WARNING - On multiple screen configuration, pywinauto window.capture_as_image() doesn't work on every screen.

CHEST_REMAINING_TIME_AREA_WIDTH = 75
HOURGLASS_VALUE_THRESHOLD = 0.725
OPEN_VALUE_THRESHOLD = 0.98
TOUCH_TO_OPEN_VALUE_THRESHOLD = 0.7
UNLOCK_BUTTON_VALUE_THRESHOLD = 0.7

finding_mana = False
mana_status = 0

class ClashRoyaleBot:
    pid = 0         # bluestacks process id
    window = None   # bluestacks window

    def __init__(self):
        self.get_bluestacks()

    def get_bluestacks(self):
        print('[i] Looking for bluestacks in processes')
        for proc in psutil.process_iter():
            if proc.name() == "Bluestacks.exe":
                bluestacks = Application(backend='uia').connect(process=proc.pid)
                try:
                    # bluestacks spawns two process, only one has a window
                    self.window = bluestacks.windows()[0]
                    self.pid = proc.pid
                    print(f'[+] Bluestacks process and window found - pid: {proc.pid}')
                    return
                except IndexError as e:
                    pass

    def get_screenshot(self):
        self.window.set_focus()
        return self.window.capture_as_image()     

    def __find_in_screen(self, searched_image_name, threshold):
        screen = self.get_screenshot() 
        
        # Convert screen to gray
        np_screen = np.array(screen, dtype = np.uint8)
        gray_screen = cv2.cvtColor(np_screen, cv2.COLOR_BGR2GRAY)

        # Convert searched image to gray and get its width / height
        np_image = cv2.imread(searched_image_name)
        gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        w, h = gray_image.shape[::-1] 

        # Look for searched image in screen
        matches = cv2.matchTemplate(gray_screen, gray_image, cv2.TM_CCOEFF_NORMED)
        
        # Get best match coordinates, check if it's below the threshold
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matches)
        print(f'[i] Search value : {max_val} for object : {searched_image_name}')
        if max_val < threshold:
            return False
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return (top_left, bottom_right)

    def start_battle(self):
        try:
            top_left, bottom_right = self.__find_in_screen('battle.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 10, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            time.sleep(3)
            self.confirm_battle()
        except TypeError as e:
            print('[!] No battle to start!')
        return True

    def confirm_battle(self):
        try:
            top_left, bottom_right = self.__find_in_screen('confirm_battle.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 10, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No confirmation!')
        return True

    def check_battle(self):
        try:
            top_left, bottom_right = self.__find_in_screen('in_battle.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            print('[!] in battle!')
        except TypeError as e:
            print('[!] not in battle!')
            self.check_in_after_battle()
            return False
        return True

    def check_in_after_battle(self):
        try:
            top_left, bottom_right = self.__find_in_screen('confirm_after_battle.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 10, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            time.sleep(2)
            print('[!] in after battle!')
        except TypeError as e:
            print('[!] not in after battle!')
            return False
        return True

    def battle(self):

        #card archer
        # try:
        #     top_left, bottom_right = self.__find_in_screen('card_archer.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        # except TypeError as e:
        #     print('[!] No archer to use!')

        # card arrows
        try:
            top_left, bottom_right = self.__find_in_screen('card_arrows.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No arrow to use!')

        # card gargule
        try:
            top_left, bottom_right = self.__find_in_screen('card_gargule.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No gargule to use!')

        # card giant
        try:
            top_left, bottom_right = self.__find_in_screen('card_giant.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No giant to use!')

        # card goblin
        # try:
        #     top_left, bottom_right = self.__find_in_screen('card_goblin.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        # except TypeError as e:
        #     print('[!] No goblin to use!')

        # card knight
        try:
            top_left, bottom_right = self.__find_in_screen('card_knight.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No knight to use!')

        # card meteor
        try:
            top_left, bottom_right = self.__find_in_screen('card_meteor.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No meteor to use!')
        
        # card musketer
        try:
            top_left, bottom_right = self.__find_in_screen('card_musketer.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No musketer to use!')

        # card goblin hunt
        try:
            top_left, bottom_right = self.__find_in_screen('card_goblin_hunt.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No goblin hunt to use!')

        # card spear goblins
        try:
            top_left, bottom_right = self.__find_in_screen('card_spear_goblins.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] + 10
            ))
            #click batleground
            pywinauto.mouse.click(button='left', coords=(
                self.window.rectangle().left + bottom_right[0] - 5, 
                self.window.rectangle().top  + bottom_right[1] - 500
            ))
            # time.sleep(1)
        except TypeError as e:
            print('[!] No spear goblins to use!')

        # card spear hog rider
        # try:
        #     top_left, bottom_right = self.__find_in_screen('card_hog_rider.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        # except TypeError as e:
        #     print('[!] No hog rider to use!')

        return True;

    def random_battle(self):

        # random_integer = 4
        random_integer = random.randint(1,4)
        # print("------------ random integer: " + str(random_integer))

        if random_integer == 1:
            # no matches!
            try:
                #click card 1
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 230,
                    self.window.rectangle().top  + 1202
                ))
                #click batleground
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 230, 
                    self.window.rectangle().top  + 800
                ))
                time.sleep(1)
            except TypeError as e:
                print('[!] No matches, random taken!')

        elif random_integer == 2:
            try:
                #click card 2
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 280, 
                    self.window.rectangle().top  + 1202
                ))
                #click batleground
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 280, 
                    self.window.rectangle().top  + 800
                ))
                time.sleep(1)
            except TypeError as e:
                print('[!] No matches, random taken!')

        elif random_integer == 3:
            try:
                #click card 3
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 465, 
                    self.window.rectangle().top  + 1202
                ))
                #click batleground
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 465, 
                    self.window.rectangle().top  + 800
                ))
                time.sleep(1)
            except TypeError as e:
                print('[!] No matches, random taken!')

        elif random_integer == 4:
            try:
                #click card 4
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 610, 
                    self.window.rectangle().top  + 1202
                ))
                #click batleground
                pywinauto.mouse.click(button='left', coords=(
                    self.window.rectangle().left + 610, 
                    self.window.rectangle().top  + 800
                ))
                time.sleep(1)
            except TypeError as e:
                print('[!] No matches, random taken!')

        return True

    def get_mana_status(self):

        finding_mana = True
        
        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_1.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 1
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_2.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 2
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        try:
            top_left, bottom_right = self.__find_in_screen('mana_3.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            # pywinauto.mouse.click(button='left', coords=(
            #     self.window.rectangle().left + bottom_right[0] - 5, 
            #     self.window.rectangle().top  + bottom_right[1] + 10
            # ))
            # #click batleground
            # pywinauto.mouse.click(button='left', coords=(
            #     self.window.rectangle().left + bottom_right[0] - 5, 
            #     self.window.rectangle().top  + bottom_right[1] - 500
            # ))
            # time.sleep(1)
            finding_mana = False;
            return 3
        except TypeError as e:
            print('[!] No spear goblins to use!')

        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_4.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 4
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        try:
            top_left, bottom_right = self.__find_in_screen('mana_5.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            # pywinauto.mouse.click(button='left', coords=(
            #     self.window.rectangle().left + bottom_right[0] - 5, 
            #     self.window.rectangle().top  + bottom_right[1] + 10
            # ))
            # #click batleground
            # pywinauto.mouse.click(button='left', coords=(
            #     self.window.rectangle().left + bottom_right[0] - 5, 
            #     self.window.rectangle().top  + bottom_right[1] - 500
            # ))
            # time.sleep(1)
            finding_mana = False;
            return 5
        except TypeError as e:
            print('[!] No spear goblins to use!')

        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_6.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 6
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_7.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 7
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_8.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 8
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        # try:
        #     top_left, bottom_right = self.__find_in_screen('mana_9.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
        #     #click card
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] + 10
        #     ))
        #     #click batleground
        #     pywinauto.mouse.click(button='left', coords=(
        #         self.window.rectangle().left + bottom_right[0] - 5, 
        #         self.window.rectangle().top  + bottom_right[1] - 500
        #     ))
        #     # time.sleep(1)
        #     finding_mana = False;
        #     return 9
        # except TypeError as e:
        #     print('[!] No spear goblins to use!')

        try:
            top_left, bottom_right = self.__find_in_screen('mana_10.PNG', TOUCH_TO_OPEN_VALUE_THRESHOLD)
            #click card
            # pywinauto.mouse.click(button='left', coords=(
            #     self.window.rectangle().left + bottom_right[0] - 5, 
            #     self.window.rectangle().top  + bottom_right[1] + 10
            # ))
            # #click batleground
            # pywinauto.mouse.click(button='left', coords=(
            #     self.window.rectangle().left + bottom_right[0] - 5, 
            #     self.window.rectangle().top  + bottom_right[1] - 500
            # ))
            # time.sleep(1)
            finding_mana = False;
            return 10
        except TypeError as e:
            print('[!] No spear goblins to use!')

        finding_mana = False;
        return 0

if __name__=='__main__':
    crb = ClashRoyaleBot()

    # game analysis
    in_battle = False

    while 1:
        in_battle = crb.check_battle()

        if in_battle:
            crb.random_battle()
            current_mana = 0
                
            #time.sleep(60 * 1) # sleep 1 min
            time.sleep(3 * 1) # sleep 1 min
        elif in_battle == False:
            crb.start_battle()


# References

# card 1
# 230, 1202

# card 2
# 280, 1202

# card 3
# 465, 1202

# card 4
# 610, 1202
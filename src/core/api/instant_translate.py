import logging
import threading
import time
from multiprocessing import Process

from pynput import mouse, keyboard
from pynput.keyboard import Key

import container
from ..utils import log

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class InstantTranslate:
    def __init__(self):
        self.k = keyboard.Controller()
        self.last_touch_position = None
        self.last_touch_time = time.time()
        self.click_time_duration = None
        self.lock = threading.Lock()
        self.mt = mouse.Listener(on_click=self.on_click)
        self.clipboard = container.get_container().clipboard

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if not pressed:
                if self.last_touch_position != (x, y) or time.time() - self.last_touch_time < 0.25:
                    self.press_copy()
                else:
                    self.last_touch_time = time.time()
            else:
                self.last_touch_position = (x, y)
        elif button == mouse.Button.middle:
            return False

    def press_copy(self):
        self.lock.acquire()
        try:
            self.k.press(Key.ctrl)
            self.k.press("c")
            self.k.release(Key.ctrl)
            self.k.release("c")
            logging.debug("press thread instant translate press copy")
        except Exception as e:
            logging.error("press thread instant translate press copy error: %s" % e)
            self.k.release(Key.ctrl)
            self.k.release("c")
        self.lock.release()

    def release_key(self):
        try:
            self.k.release(Key.ctrl)
            self.k.release("c")
            logging.debug("instant translate release key")
        except Exception as e:
            logging.debug("instant translate release key error: %s" % e)
            pass

    def run(self):
        self.mt.start()
        self.mt.join()


if __name__ == '__main__':
    it = InstantTranslate()
    p = Process(target=it.run)
    p.start()
    p.join()

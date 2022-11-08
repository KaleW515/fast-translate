import logging
import threading
import time
from multiprocessing import Process

from pynput import mouse, keyboard

import container
from core.utils import log

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class InstantTranslate:
    def __init__(self):
        self.k = keyboard.Controller()
        self.last_touch_position = None
        self.last_touch_time = time.time()
        self.click_time_duration = None
        self.lock = threading.Lock()
        self.mt = mouse.Listener(on_click=self.__on_click)
        self.clipboard = container.get_container().clipboard
        self.copykey = container.get_container().config.get_copykey()

    def __on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if not pressed:
                logging.info("mouse button left pressed")
                if self.last_touch_position != (x, y) or time.time() - self.last_touch_time < 0.25:
                    self.__press_copy()
                else:
                    self.last_touch_time = time.time()
            else:
                logging.info("mouse button left unpressed")
                self.last_touch_position = (x, y)
        elif button == mouse.Button.middle:
            return False

    def __press_copy(self):
        self.lock.acquire()
        try:
            for i in range(len(self.copykey)):
                self.k.press(self.copykey[i])
            for i in range(len(self.copykey)):
                self.k.release(self.copykey[i])
            logging.debug("press thread instant translate press copy")
        except Exception as e:
            logging.error("press thread instant translate press copy error: %s" % e)
            for i in range(len(self.copykey)):
                self.k.release(self.copykey[i])
        self.lock.release()

    def release_key(self):
        try:
            for i in range(len(self.copykey)):
                self.k.release(self.copykey[i])
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

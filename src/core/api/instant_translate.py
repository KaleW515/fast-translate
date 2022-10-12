import logging
import threading
import time
from multiprocessing import Process

from pynput import mouse, keyboard
from pynput.keyboard import Key

from ..utils import log

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class InstantTranslate:
    def __init__(self):
        self.k = keyboard.Controller()
        self.sync = 1
        self.have_copy = False
        self.lock = threading.Lock()
        self.mt = mouse.Listener(on_move=self.on_move)
        self.sync_desc_thread = threading.Thread(target=self.sync_desc)
        self.press_copy_thread = threading.Thread(target=self.press_copy)

    def on_move(self, x, y):
        self.sync = 1
        self.have_copy = False
        # print(x, y)

    def sync_desc(self):
        logging.debug("sync desc thread start")
        while 1:
            time.sleep(0.6)
            self.lock.acquire()
            if self.sync >= 1:
                self.sync -= 1
            self.lock.release()

    def press_copy(self):
        logging.debug("press copy thread start")
        while 1:
            time.sleep(1)
            self.lock.acquire()
            if self.sync == 0:
                if not self.have_copy:
                    try:
                        self.k.press(Key.ctrl)
                        self.k.press("c")
                        self.k.release(Key.ctrl)
                        self.k.release("c")
                        self.have_copy = True
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
        self.sync = 1
        self.mt.start()
        self.sync_desc_thread.start()
        self.press_copy_thread.start()
        self.sync_desc_thread.join()
        self.press_copy_thread.join()


if __name__ == '__main__':
    it = InstantTranslate()
    p = Process(target=it.run)
    p.start()
    p.join()

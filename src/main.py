import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu

import container


class SystemTray:
    def __init__(self, app, window):
        self.app = app
        self.window = window
        self.window.show()
        self.tp = QSystemTrayIcon(self.window)
        self.init_icon()
        self.run()

    def init_icon(self):
        self.tp.setIcon(QIcon('config/icon/logo.svg.png'))

    def act(self, reason):
        if reason == 2 or reason == 3:
            self.window.show()

    def quitApp(self):
        self.tp.setVisible(False)
        self.window.stop_thread()
        self.window.stop_process()
        self.app.quit()

    def run(self):
        a1 = QAction("显示Fast-Translate", triggered=self.window.show)
        a2 = QAction("退出Fast-Translate", triggered=self.quitApp)

        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        self.tp.setContextMenu(tpMenu)
        self.tp.show()
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    container = container.get_container()
    container.invoke_init()
    main_window = container.main_window
    main_window.show()
    main_window.thread.start()
    ti = SystemTray(container.app, main_window)

#!python

from logging import getLogger
import sys

sys.path.append(".")

from PyQt5 import QtWidgets

from ui.authDialog import AuthDialog
from ui.mainWindow import MainWindow

import jim.logger
from jim.classes import Client
from jim.utils import parse_arguments


if __name__ == "__main__":
    opts = parse_arguments()
    username = opts.username
    password = opts.password

    app = QtWidgets.QApplication(sys.argv)
    if not username or not password:
        auth_gialog = AuthDialog()
        app.exec_()

        username = auth_gialog.get_username() or sys.exit()
        password = auth_gialog.get_password() or sys.exit()

    client = Client(
        opts.address,
        opts.port,
        username,
        password,
        logger=getLogger("messenger.client"),
    )
    main_window = MainWindow(client)
    main_window.bind_signals()

    client.start()
    app.exec_()

    try:
        client.stop()
        client.join()
    except Exception:
        pass

import sys
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QTableView, QMainWindow, \
    QAction, QLabel, QGridLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from gui_server.gui_settings_window import SettingsWindow
from gui_server.gui_registration_user import RegistrationDialog


class MainWindow(QMainWindow):
    """Class main window for user. Contains contacts list, text edit and history messages"""
    def __init__(self, app, database, server):
        self.app = app
        self.database = database
        self.server = server
        super().__init__()

    def init_ui(self):
        self.resize(700, 600)
        self.move(500, 300)

        self.setWindowTitle('Server')

        self.statusBar()

        exit_action = QAction('Close', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.app.quit)

        update_connected_users_action = QAction('Update connected users', self)
        update_connected_users_action.triggered.connect(self.update_connected_users_list)

        self.settings_window = SettingsWindow()
        server_settings_action = QAction('Settings', self)
        server_settings_action.triggered.connect(self.settings_window.init_ui)

        self.regiastration_dialog = RegistrationDialog(self.database, self.server)
        add_user = QAction('Registration user', self)
        add_user.triggered.connect(self.regiastration_dialog.init_ui)

        rm_user = QAction('Remove user', self)
        # rm_user.triggered.connect(self.user_remove)

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.setFont(QtGui.QFont('Montserrat', 10))
        self.toolbar.addAction(update_connected_users_action)
        self.toolbar.addAction(server_settings_action)
        self.toolbar.addAction(add_user)
        self.toolbar.addAction(rm_user)
        self.toolbar.addAction(exit_action)

        self.central_widget = QWidget(self)
        self.layout = QGridLayout(self.central_widget)

        self.connected_users_label = QLabel('Connected users:')
        self.connected_users_label.setFont(QtGui.QFont('Montserrat', 10))
        self.connected_users_table = QTableView(self)

        self.connected_users_table.setFont(QtGui.QFont('Montserrat', 10))

        self.connected_users_list = QStandardItemModel(self)
        self.connected_users_table.setModel(self.connected_users_list)

        self.layout.addWidget(self.connected_users_label, 0, 0)
        self.layout.addWidget(self.connected_users_table, 1, 0)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.statusBar().showMessage("Server Working")

        self.update_connected_users_list()

        self.show()

    def add_connected_user(self, user_name, ip_address, port, connection_time):
        user_name = QStandardItem(user_name)
        user_name.setEditable(False)  # forbidden to enter text
        ip_address = QStandardItem(ip_address)
        ip_address.setEditable(False)
        port = QStandardItem(port)
        port.setEditable(False)
        connection_time = QStandardItem(connection_time)
        connection_time.setEditable(False)
        self.connected_users_list.appendRow([user_name, ip_address, port, connection_time])

    def update_connected_users_list(self):
        users = self.database.users_active_list()
        self.connected_users_list.clear()
        self.connected_users_list.setHorizontalHeaderLabels(['Name', 'IP', 'Port', 'Connection time'])

        for name, ip, port, time in users:
            self.add_connected_user(name, ip, str(port), time.strftime("%m/%d/%Y, %H:%M:%S"))

        #  Align Date Column
        self.connected_users_table.resizeColumnToContents(3)

    @pyqtSlot()
    def update_connected_users_slot(self):
        """Slot update connected users list on main window"""
        self.update_connected_users_list()

    def make_connection_signals(self, transport_server_obj):
        """Signal connection method."""
        transport_server_obj.new_connected_client.connect(self.update_connected_users_slot)
        transport_server_obj.disconnected_client.connect(self.update_connected_users_slot)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.init_ui()
    # main_window.update_connected_users_list()
    sys.exit(app.exec_())

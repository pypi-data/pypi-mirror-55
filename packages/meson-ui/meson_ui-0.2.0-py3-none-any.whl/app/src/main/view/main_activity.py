#!/user/bin/env python3
###################################################################################
#                                                                                 #
# AUTHOR: Michael Brockus.                                                        #
#                                                                                 #
# CONTACT: <mailto:michaelbrockus@gmail.com>                                      #
#                                                                                 #
# LICENSE: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0                 #
#                                                                                 #
###################################################################################
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDir
from ..mesonuilib.component.console import MesonUiConsole
from ..mesonuilib.component.targetview import MesonUiTargetList
from ..mesonuilib.meson.meson import Meson
from ..model.mesonuimodel import MesonUiModule
from ..controller.mesonuicontroller import MesonUiController
from .setup_activity import SetupActivity
from .data_activity import IntroActivity
from .info_activity import InfoActivity
from ..ui.activity_main import Ui_MainWindow

from os.path import join as join_paths

EMPTY_STRING = ''


class MainActivity(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(800, 600)

        self._model = MesonUiModule(context=self)
        self._controller = MesonUiController(self._model)

        # This is used to perform Meson build actions
        self.meson = Meson(self)
        self.console = MesonUiConsole(self)
        self.tableview = MesonUiTargetList(self)

        self._model.get_project().set_sourcedir(self.get_sourcedir())
        self._model.get_project().set_builddir(self.get_builddir())
        self.on_create()
    # end of method

    @pyqtSlot()
    def on_create(self) -> None:
        # Meson-ui help.
        self.actionAbout_Meson_ui.triggered.connect(lambda: self.onclick_info())
        self.actionMeson_docs.triggered.connect(lambda: self.onclick_docs())
        self.actionMeson_QnA.triggered.connect(lambda: self.onclick_faqs())
        self.actionMeson_ui_issue.triggered.connect(lambda: self.onclick_mesonui_issue())
        self.actionMeson_issue.triggered.connect(lambda: self.onclick_meson_issue())

        # Mesnu-ui main view buttons.
        self.push_setup.clicked.connect(lambda: self.onclick_setup())
        self.push_build.clicked.connect(lambda: self.onclick_build())
        self.push_install.clicked.connect(lambda: self.onclick_install())
        self.push_intro.clicked.connect(lambda: self.onclick_data())

        self.push_test.clicked.connect(lambda: self.onclick_tests())
        self.push_dist.clicked.connect(lambda: self.onclick_dist())
        self.push_open.clicked.connect(lambda: self.onclick_open())
        self.push_clear.clicked.connect(lambda: self.onclick_clear())

        self.push_clean.clicked.connect(lambda: self.onclick_clean())
        self.push_docs.clicked.connect(lambda: self.onclick_docs())
    # end of method

    @pyqtSlot()
    def onclick_setup(self) -> None:
        self._model.get_project().set_sourcedir(self.get_sourcedir())
        self._model.get_project().set_scriptdir(self.get_scriptdir())
        self._model.get_project().set_builddir(self.get_builddir())
        self.intent_setup = SetupActivity(self, model=self._model, controller=self._controller)
        self.intent_setup.show()
    # end of method

    @pyqtSlot()
    def onclick_data(self) -> None:
        self.intent_data = IntroActivity(self, model=self._model, controller=self._controller)
        self.intent_data.show()

    @pyqtSlot()
    def onclick_info(self) -> None:
        self.intent_info = InfoActivity(self)
        self.intent_info.show()
    # end of method

    @pyqtSlot()
    def onclick_quit(self) -> None:
        QApplication.quit()
    # end of method

    @pyqtSlot()
    def onclick_build(self) -> None:
        self.meson.build()
        self.tableview.update_table()
    # end of method

    @pyqtSlot()
    def onclick_dist(self) -> None:
        self.meson.dist()
    # end of method

    @pyqtSlot()
    def onclick_clean(self) -> None:
        self.meson.clean()
        self.tableview.update_table()
    # end of method

    @pyqtSlot()
    def onclick_tests(self) -> None:
        self.meson.tests()
    # end of method

    @pyqtSlot()
    def onclick_install(self) -> None:
        self.meson.install()
    # end of method

    @pyqtSlot()
    def onclick_clear(self) -> None:
        self.source_dir.setText(EMPTY_STRING)
        self.build_dir.setText(EMPTY_STRING)
    # end of method

    @pyqtSlot()
    def onclick_open(self) -> None:
        project_path = str(QFileDialog.getExistingDirectory(self, 'Open project directory', QDir.homePath()))
        if project_path != EMPTY_STRING:
            self._model.get_project().set_sourcedir(project_path)
            self._model.get_project().set_scriptdir(join_paths(project_path, 'meson.build'))
            self._model.get_project().set_builddir(join_paths(project_path, 'builddir'))

        self.source_dir.setText(self._model.get_project().get_sourcedir())
        self.build_dir.setText(self._model.get_project().get_builddir())
        self.tableview.update_table()
    # end of method

    @pyqtSlot()
    def onclick_docs(self):
        self.open_url(url_link=QUrl('https://mesonbuild.com'))
    # end of method

    @pyqtSlot()
    def onclick_faqs(self):
        self.open_url(url_link=QUrl('https://mesonbuild.com/FAQ.html'))
    # end of method

    @pyqtSlot()
    def onclick_mesonui_issue(self):
        self.open_url(url_link=QUrl('https://github.com/michaelbadcrumble/meson-ui/issues'))
    # end of method

    @pyqtSlot()
    def onclick_meson_issue(self):
        self.open_url(url_link=QUrl('https://github.com/mesonbuild/meson/issues'))
    # end of method

    def open_url(self, url_link: QUrl):
        QDesktopServices.openUrl(url=url_link)
    # end of method

    def get_scriptdir(self) -> str:
        return join_paths(self.source_dir.text(), 'meson.build')

    def get_sourcedir(self) -> str:
        return self.source_dir.text()

    def get_builddir(self) -> str:
        return self.build_dir.text()

    def process(self):
        return self.meson.process()

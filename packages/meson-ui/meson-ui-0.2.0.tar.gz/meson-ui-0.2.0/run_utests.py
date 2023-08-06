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
from PyQt5.QtCore import QObject, QProcess
# from app.src.main.model.mesonuimodel import MesonUiModule
from app.src.main.mesonuilib.meson.meson import Meson
from os import path
from time import sleep


#
# This class is faking the apps projetc data
#
class FakeProg(QObject):
    def __init__(self):
        super().__init__()
        self._process = QProcess(self)
        self.dir_src = ''
        self.dir_build = path.join(self.dir_src, 'builddir')
        self.dir_script = path.join(self.dir_src, 'meson.build')

    def process(self):
        return self._process

    def set_sourcedir(self, value: str) -> str:
        self.dir_src = value

    def set_builddir(self, value: str) -> str:
        self.dir_build = value

    def set_scriptdir(self, value: str) -> str:
        self.dir_script = value

    def get_scriptdir(self) -> str:
        return self.dir_script

    def get_sourcedir(self) -> str:
        return self.dir_src

    def get_builddir(self) -> str:
        return self.dir_build


def test_meson_setup():
    prog = FakeProg()
    prog.set_sourcedir('test-cases/meson/01-meson-setup')
    prog.set_builddir('test-cases/meson/01-meson-setup/builddir')

    meson = Meson(prog)
    meson.setup()

    # Let test case sleep so intro repo can find the dir when it's
    # generated
    sleep(5)

    assert path.exists('test-cases/meson/01-meson-setup')
    assert path.exists('test-cases/meson/01-meson-setup/builddir')


def test_meson_build():
    prog = FakeProg()
    prog.set_sourcedir('test-cases/meson/02-meson-build')
    prog.set_builddir('test-cases/meson/02-meson-build/builddir')

    meson = Meson(prog)
    meson.setup()
    meson.build()

    assert path.exists('test-cases/meson/02-meson-build')
    assert path.exists('test-cases/meson/02-meson-build/builddir')


def test_meson_clean():
    prog = FakeProg()
    prog.set_sourcedir('test-cases/meson/03-meson-clean')
    prog.set_builddir('test-cases/meson/03-meson-clean/builddir')

    meson = Meson(prog)
    meson.setup()
    meson.build()
    meson.clean()

    assert path.exists('test-cases/meson/03-meson-clean')
    assert path.exists('test-cases/meson/03-meson-clean/builddir')


def test_meson_tests():
    prog = FakeProg()
    prog.set_sourcedir('test-cases/meson/04-meson-test')
    prog.set_builddir('test-cases/meson/04-meson-test/builddir')

    meson = Meson(prog)
    meson.setup()
    meson.build()
    meson.tests()

    assert path.exists('test-cases/meson/04-meson-test')
    assert path.exists('test-cases/meson/04-meson-test/builddir')


def test_meson_dist():
    prog = FakeProg()
    prog.set_sourcedir('test-cases/meson/05-meson-dist')
    prog.set_builddir('test-cases/meson/05-meson-dist/builddir')

    meson = Meson(prog)
    meson.setup()
    meson.build()
    meson.dist()

    assert path.exists('test-cases/meson/05-meson-dist')
    assert path.exists('test-cases/meson/05-meson-dist/builddir')


# def test_meson_introspection():
#     intro_prog = FakeProg()
#     intro_prog.set_sourcedir('test-cases/meson/06-introspection')
#     intro_prog.set_builddir('test-cases/meson/06-introspection/builddir')

#     meson_data: MesonUiModule = MesonUiModule(intro_prog)
#     intex: int = 0

#     # Let test case sleep so intro repo can find the dir when it's
#     # generated
#     time.sleep(5)

#     # Testing project info
#     assert meson_data.get_projectinfo().get_name() == 'c-exe'
#     assert meson_data.get_projectinfo().get_version() == 'undefined'
#     assert meson_data.get_projectinfo().get_subproject_dir() == 'subprojects'
#     assert meson_data.get_projectinfo().get_subprojects() == []

#     # Testing targets info
#     assert meson_data.get_targets().get_build_by_default() is True
#     assert meson_data.get_targets().get_type() == 'executable'
#     assert meson_data.get_targets().get_subproject() is None
#     assert meson_data.get_targets().get_name() == 'exe'

#     # Testing targets sources info
#     assert meson_data.get_targets_sources().get_compiler() == ['cc']
#     assert meson_data.get_targets_sources().get_language() == 'c'

#     # Testing test info
#     assert meson_data.get_tests().get_environment(index=intex) == {}
#     assert meson_data.get_tests().get_is_parallel(index=intex) is True
#     assert meson_data.get_tests().get_name(index=intex) == 'Run test exe'
#     assert meson_data.get_tests().get_priority(index=intex) == 0
#     assert meson_data.get_tests().get_suite(index=intex) == ['c-exe']
#     assert meson_data.get_tests().get_timeout(index=intex) == 30
#     assert meson_data.get_tests().get_workdir(index=intex) is None

#     # Testing benchmark info
#     assert meson_data.get_benchmark().get_environment(index=intex) == {}
#     assert meson_data.get_benchmark().get_is_parallel(index=intex) is True
#     assert meson_data.get_benchmark().get_name(index=intex) == 'Run benchmark exe'
#     assert meson_data.get_benchmark().get_priority(index=intex) == 0
#     assert meson_data.get_benchmark().get_suite(index=intex) == ['c-exe']
#     assert meson_data.get_benchmark().get_timeout(index=intex) == 30
#     assert meson_data.get_benchmark().get_workdir(index=intex) is None

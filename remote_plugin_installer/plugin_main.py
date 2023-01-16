#! python3  # noqa: E265

"""
    Main plugin module.
"""

# PyQGIS
from tempfile import NamedTemporaryFile

from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, QFile
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import showPluginHelp

# project
from remote_plugin_installer.__about__ import __title__
from remote_plugin_installer.gui.dlg_settings import PlgOptionsFactory
from remote_plugin_installer.toolbelt import PlgLogger, PlgOptionsManager, PlgTranslator
from remote_plugin_installer.toolbelt.http import AddressInUseException, ServerThread
from remote_plugin_installer.toolbelt.plugin_install import install

# ############################################################################
# ########## Classes ###############
# ##################################


class PostPluginPlugin:
    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class which \
        provides the hook by which you can manipulate the QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.log = PlgLogger().log
        self.server_thread = None
        self.port = PlgOptionsManager().get_plg_settings().port

        # translation
        plg_translation_mngr = PlgTranslator()
        translator = plg_translation_mngr.get_translator()
        if translator:
            QCoreApplication.installTranslator(translator)
        self.tr = plg_translation_mngr.tr

    def initGui(self):
        """Set up plugin UI elements."""

        # settings page within the QGIS preferences menu
        self.options_factory = PlgOptionsFactory()
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        # -- Actions
        self.action_run = QAction(
            QIcon(":/images/themes/default/mActionArrowRight.svg"),
            self.tr("Start Development Server", context="PostPluginPlugin"),
            self.iface.mainWindow(),
        )
        self.action_run.triggered.connect(self.run)

        self.action_help = QAction(
            QIcon(":/images/themes/default/mActionHelpContents.svg"),
            self.tr("Help", context="PostPluginPlugin"),
            self.iface.mainWindow(),
        )
        self.action_help.triggered.connect(
            lambda: showPluginHelp(filename="resources/help/index")
        )

        self.action_settings = QAction(
            QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
            self.tr("Settings"),
            self.iface.mainWindow(),
        )
        self.action_settings.triggered.connect(
            lambda: self.iface.showOptionsDialog(
                currentPage="mOptionsPage{}".format(__title__)
            )
        )

        # -- Menu
        self.iface.addPluginToMenu(__title__, self.action_run)
        self.iface.addPluginToMenu(__title__, self.action_settings)
        self.iface.addPluginToMenu(__title__, self.action_help)

        # -- Toolbar
        self.toolbar = self.iface.addToolBar("dev server")
        self.toolbar.addAction(self.action_run)

    def unload(self):
        """Cleans up when plugin is disabled/uninstalled."""
        # -- Clean up menu
        self.iface.removePluginMenu(__title__, self.action_help)
        self.iface.removePluginMenu(__title__, self.action_settings)
        self.iface.removePluginMenu(__title__, self.action_run)

        # -- Clean up preferences panel in QGIS settings
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

        # remove actions
        del self.action_settings
        del self.action_help
        del self.action_run
        del self.toolbar

        if self.server_thread:
            self.server_thread.terminate()
            self.server_thread.httpd.server_close()
            self.server_thread.wait()
            del self.server_thread

    def run(self):
        # stop if started
        if self.server_thread:
            self.action_run.setIcon(
                QIcon(":/images/themes/default/mActionArrowRight.svg")
            )
            self.action_run.setText("Start Development Server")

            self.server_thread.terminate()
            self.server_thread.httpd.server_close()
            self.server_thread.wait()
            del self.server_thread
            self.server_thread = None
            self.iface.messageBar().pushSuccess(
                "Stopped server", "The server was stopped successfully."
            )
        # else: start server
        else:
            print("starting server..")
            self.port = PlgOptionsManager().get_plg_settings().port
            self.tempfile = NamedTemporaryFile()
            try:
                self.server_thread = ServerThread(
                    tempfile=self.tempfile, port=self.port
                )
            except AddressInUseException:
                self.server_thread = None

            if self.server_thread:
                self.server_thread.output.connect(self.on_server_output)
                self.server_thread.start()

                self.action_run.setIcon(
                    QIcon(":/images/themes/default/mActionStop.svg")
                )
                self.action_run.setText("Stop Development Server")
                self.iface.messageBar().pushSuccess(
                    "Server running", f"The server is running on port {self.port}."
                )
            else:
                self.iface.messageBar().pushWarning(
                    "Address already in use", f"the port {self.port} is already in use!"
                )

    def on_server_output(self):
        name, duration = install(self.tempfile.name)
        self.iface.messageBar().pushSuccess(
            "Plugin installed", f"Plugin {name} installed after {duration}ms"
        )

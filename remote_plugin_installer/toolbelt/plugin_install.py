import os
import zipfile
from time import time

import pyplugin_installer
from qgis.core import QgsSettings
from qgis.utils import loadPlugin, startPlugin, unloadPlugin


def install(filename):
    """Install a plugin from zip file path"""
    plugin_name = get_plugin_name(filename)

    installer = pyplugin_installer.instance()
    installer.installFromZipFile(filename)

    start_time = time()
    unloadPlugin(plugin_name)
    loadPlugin(plugin_name)
    plugin_started = startPlugin(plugin_name)
    end_time = time()

    duration = int(round((end_time - start_time) * 1000))

    print(plugin_started)
    print(f"Plugin {plugin_name} reloaded after {duration} ms")


def get_plugin_name(filename):
    plugin_name = None
    with zipfile.ZipFile(filename, "r") as zf:
        # search for metadata.txt. In case of multiple files, we can assume that
        # the shortest path relates <pluginname>/metadata.txt
        metadatafiles = sorted(f for f in zf.namelist() if f.endswith("metadata.txt"))
        if len(metadatafiles) > 0:
            plugin_name = os.path.split(metadatafiles[0])[0]
    return plugin_name

import pyplugin_install


def install(filename):
    """Install a plugin from zip file path"""
    installer = pyplugin_install.instance()
    installer.installFromZipFile(filename)

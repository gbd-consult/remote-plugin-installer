# Remote Plugin Installer - QGIS Plugin

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[![pylint](https://gitlab.com/Company/remote_plugin_installer/lint/pylint.svg)](https://gitlab.com/Company/remote_plugin_installer/lint/)
[![flake8](https://img.shields.io/badge/linter-flake8-green)](https://flake8.pycqa.org/)

QGIS Plugin to install QGIS Plugins via POST Requests.

Download the plugin here: https://plugins.gbd-consult.de/plugin/7

Once you have started the Plugin you can send Requests via POST.
An Example using CURL:

```(bash)
curl -F "archive=path/to/plugin.zip" localhost:6789
```

The development server does then install the plugin in qgis and reloads it.

The Port can be set in the settings.

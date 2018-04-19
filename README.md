# CARTO/CartoDB plugin for QGIS

https://github.com/GreenInfo-Network/qgis-cartodb


## History

Initial 2014-2017 edition, was sponsored by [CARTO / CartoDB](https://carto.com/) and developed by [Kudos Ltda](http://gkudos.com/)

In 2018, CARTO terminated the old v1 API, causing the plugin to cease functioning. GreenInfo forked the repository, and updated various components to new V2 API functionality. This meant a few losses, e.g. the plugin reporting quota status in its panels, but did at least get layer loading and editing working again.

## Developer Notes

### Compiling it

While this could in theory be compiled on Windows systems, using Cygwin or Unix-like utilities, I found it impractical and recommend using a Unix-like system such as Ubuntu or Mac OSX.

To clean and recompile:
```
make clean transclean && make transcompile && make
```

This uses `pyuic4` and requires *PyQt* to be installed. On a fresh-off-the-disk install of Ubuntu 16, the following installed the required Python components:
```
sudo apt-get install pyqt4-dev-tools qt4-designer
```

### Testing It

Copy the development into the QGIS plugins directory, overwriting existing files. Yes, the whole repository including the build output.
* On Windows, the QGIS plugin folder would be `C:\Users\YOUR_USER_NAME\.qgis2\python\plugins\QgisCartoDB`
* On Mac OSX, the QGIS plugin folder would be `~/.qgis2/python/plugins/QgisCartoDB`

Then reload the plugin, by closing QGIS and starting it again. Or, I recommend the *Plugin Reloader* plugin for QGIS. This adds a button to your toolbar, which will unload a plugin and reload it again. This saves a lot of time closing and re-opening QGIS. *Note that during development, the reloader may be less than perfect, particularly when debugging errors in CRUD operations. You may need to reload the CartoDB layer, or even quit QGIS entirely.*

### Deploying It

Have the client install the existing *CartoDB* plugin in QGIS.

Then, send them the ZIP file of the updated version. Have them unpack it and move the files into place, overwriting the version they have in place. They should then restart QGIS.

An immediately-obvious sign that the plugin is our version asnd not the non-functional stock version, is the CARTO message (their username) or en error message (instead of just "error" in red).

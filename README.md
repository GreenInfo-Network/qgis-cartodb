![Logo](images/logo.jpg?raw=true "QGis CartoDB")
================================================

CartoDB Plugin for QGis.  It allows to view,  create, edit or delete data from  your CartoDB account using your favorite opensource desktop GIS: QGIS.  


## Features

![QGis CartoDB](images/screenshot.png?raw=true "QGis CartoDB")

* Manage CartoDB connections.
* Add CartoDB layers to QGIS projects.
* Create QGIS layers from SQL Queries.
* Add features to CartoDB tables.
* Edit data and update CartoDB tables.
* Edit data and update geometries.
* Delete features.
* Upload vector layers to CartoDB.
* Create maps, supported:
    * Styles: (single symbol, categorized and graduated).
    * Simple fill.
    * Borders style: (solid line, no pen, dash line, dot line, dash dot line and dash dot dot line).
    * Simple lines.
    * Line and border join styles: (bevel, miter and round).
    * Line and border line width.
    * Simple markers: (fill, size, outline width).
    * Layer transparency.
    * Feature blending mode.

## Limitations

* Add new attributes.
* Get visualizations or CartoCSS styles.

## Supported Versions

Minimum QGIS version:  2.4

## Install

### From QGIS repositories

* Go to "Plugins -> Manage and Install Plugins"
* Search for "CartoDB Plugin" in "Search"

### From git repository

#### Downloading release code
* Download the code from [here](https://github.com/gkudos/qgis-cartodb/releases/latest)
* Extract from zip file.
* Rename folder to QgisCartoDB
* Copy the plugin folder to $HOME/.qgis2/python/plugins/

#### Cloning repo (for Linux/Mac users)

* Open a terminal.
* Execute:
    * `git clone https://github.com/gkudos/qgis-cartodb.git`
    * `cd qgis-cartodb`
    * `make install`

#### Enabling plugin

* Open QGIS
* Go to "Plugins"=>"Manage and install plugins"
* Click on "Installed" and enable "CartoDB Plugin"

## Quick Use

After enabled plugin, click on CartoDB username: ![Connections](images/open_connections.png?raw=true "Connections")

This open dialog:

![Dialog 1](images/dialog1.png?raw=true "Connection Manager")

#### Creating new connection

Click on "New" button.

![Dialog 2](images/dialog2.png?raw=true "New Connection")

Add your CartoDB account. Your api key is in:

    https://[youraccount].cartodb.com/your_apps

Click on "Save" button.


#### Adding layers

Click on the icon: ![Icon](images/icons/add.png?raw=true "Icon") or on the web menu item "CartoDB Plugin" => "Add CartoDB Layer"

This open dialog:

![Dialog 3](images/dialog3.png?raw=true "Adding layer")

Select any table and click on "OK" button.

Voilá !!!!

![Voilá](images/layer.png?raw=true "Voilá !!!")

#### Adding SQL CartoDB layer

Click on the icon: ![Icon](images/icons/sql.png?raw=true "Icon") or on the web menu item "CartoDB Plugin" => "Add SQL CartoDB Layer"

![Dialog 3](images/sql_dialog.png?raw=true "Adding SQL layer")

## Dependencies

* [CartoDB](https://github.com/Vizzuality/cartodb-python)
* oauth2
* simplejson
* certifi

## Help Wanted

Any idea, issue or comment?, Please open an issue with related label.
Do You want to contribute? Fork this project and get to work. Your time and help is greatly appreciated.

Please check our [Contributing Guide](CONTRIBUTING.md)

### Translate

* Please go to [QGISCartoDB transiflex project](https://www.transifex.com/kudos/qgis-cartodb/).
* Click on 'HELP TRANSLATE "qgis-cartodb"'.

## Licence

This plugin is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

#### Icons designed by:

**From the [Noun Project](http://www.thenounproject.com):**

Calculator by [Ricardo Augusto Cherem](http://www.thenounproject.com/ricardo.cherem) <br />
Accounting by [Scott Lewis](http://www.thenounproject.com/iconify)

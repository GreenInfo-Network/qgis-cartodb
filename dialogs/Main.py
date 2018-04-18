"""
/***************************************************************************
CartoDB Plugin
A QGIS plugin

----------------------------------------------------------------------------
begin                : 2014-09-08
copyright            : (C) 2015 by Michael Salgado, Kudos Ltda.
email                : michaelsalgado@gkudos.com, info@gkudos.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QUrl, QEventLoop, pyqtSignal, pyqtSlot, Qt, qDebug
from PyQt4.QtGui import QApplication, QDialog, QMessageBox, QListWidgetItem, QIcon

from qgis.core import QgsMessageLog

from QgisCartoDB.cartodb import CartoDBAPIKey, CartoDBException, CartoDBApi
from QgisCartoDB.dialogs.UserData import CartoDBUserDataDialog
from QgisCartoDB.ui.UI_CartoDBPlugin import Ui_CartoDBPlugin
from QgisCartoDB.utils import CartoDBPluginWorker
from QgisCartoDB.widgets import CartoDBDatasetsListItem

import QgisCartoDB.resources

from qgis.core import QgsMessageLog

import copy
import json


# Create the dialog for CartoDBPlugin
class CartoDBPluginDialog(CartoDBUserDataDialog):
    def __init__(self, toolbar, parent=None):
        CartoDBUserDataDialog.__init__(self, toolbar, parent)

        # Set up the user interface from Designer.
        self.ui = Ui_CartoDBPlugin()
        self.ui.setupUi(self)
        self.ui.searchTX.textChanged.connect(self.filterTables)
        self.ui.sqlBT.clicked.connect(self.onSQL)
        # self.ui.tablesList.verticalScrollBar().valueChanged.connect(self.onScroll)

        self.isLoadingTables = False
        self.noLoadTables = False

        self.initUserConnection()
        self.loadSQL = False

    def getTablesListSelectedItems(self):
        return self.ui.tablesList.selectedItems()

    def getItemWidget(self, item):
        return self.ui.tablesList.itemWidget(item)

    def filterByExtent(self):
        return self.ui.extentCH.isChecked()

    def onSQL(self):
        self.loadSQL = True
        self.reject()

    @pyqtSlot()
    def connect(self):
        # Get tables from CartoDB.
        QgsMessageLog.logMessage('Main.py connect() entered', 'CartoDB Plugin', QgsMessageLog.INFO)
        self.tablesPage = 1
        self.noLoadTables = False
        self.ui.searchTX.setText('')
        self.getTables(self.currentUser, self.currentApiKey, self.currentMultiuser)

    def filterTables(self):
        text = self.ui.searchTX.text()
        if text == '':
            newVisualizations = self.visualizations
        else:
            newVisualizations = [t for t in self.visualizations if text in t['name']]
        self.updateList(newVisualizations)

    def updateList(self, visualizations):
        self.ui.tablesList.clear()
        for visualization in visualizations:
            item = QListWidgetItem(self.ui.tablesList)

            widget = CartoDBDatasetsListItem(visualization['name'])
            # item.setText(visualization['name'])
            readonly = False
            """
            # qDebug('Vis:' + json.dumps(visualization, sort_keys=True, indent=2, separators=(',', ': ')))
            if visualization['permission'] is not None and owner != self.currentUser and \
               visualization['permission']['acl'] is not None:
                for acl in visualization['permission']['acl']:
                    if acl['type'] == 'user' and 'username' in acl['entity'] and acl['entity']['username'] == self.currentUser and \
                       acl['access'] == 'r':
                        readonly = True
                        break
            """

            widget.readonly = readonly
            if readonly:
                widget.setTextColor('#999999')

            item.setSizeHint(widget.sizeHint())
            # item.setIcon(QIcon(":/plugins/qgis-cartodb/images/icons/layers.png"))
            self.ui.tablesList.setItemWidget(item, widget)

    def getTables(self, cartodbUser, apiKey, multiuser=False):
        QgsMessageLog.logMessage('Main.py getTables() entered', 'CartoDB Plugin', QgsMessageLog.INFO)
        cartoDBApi = CartoDBApi(cartodbUser, apiKey, multiuser)
        cartoDBApi.fetchContent.connect(self.cbTables)
        cartoDBApi.error.connect(self.error)
        self.isLoadingTables = True
        cartoDBApi.getUserTables(1, 100000)

    @pyqtSlot(dict)
    def cbTables(self, data):
        QgsMessageLog.logMessage('Main.py cbTables() '  + str(data), 'CartoDB Plugin', QgsMessageLog.INFO)
        if 'error' in data:
            return

        data['visualizations'] = [ { 'name': r['tablename'] } for r in data['rows'] ]

        self.totalTables = len(data['visualizations'])
        self.totalShared = 0

        if len(data['visualizations']) == 0:
            self.noLoadTables = True

        if self.tablesPage == 1:
            self.visualizations = data['visualizations']
        else:
            self.visualizations.extend(data['visualizations'])

        self.visualizations.reverse()

        self.updateList(self.visualizations)
        self.ui.searchTX.setEnabled(True)
        self.isLoadingTables = False
        self.setUpUserData()

    def onScroll(self, val):
        maximum = self.ui.tablesList.verticalScrollBar().maximum()
        if val >= maximum - 4 and not self.isLoadingTables and not self.noLoadTables:
            self.tablesPage = self.tablesPage + 1
            self.getTables(self.currentUser, self.currentApiKey, self.currentMultiuser)

    def showEvent(self, event):
        worker = CartoDBPluginWorker(self, 'connect')
        worker.start()

    def error(self):
        QMessageBox.warning(self, QApplication.translate('CartoDBPlugin', 'Error'),
                            QApplication.translate('CartoDBPlugin', 'Error loading data from CartoDB'))

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
from PyQt4.QtGui import QWidget, QHBoxLayout, QLayout, QComboBox, QSizePolicy, QLabel
from PyQt4.QtGui import QImage, QPixmap, QImageReader, QCursor
from PyQt4.QtCore import Qt, QSize, QSettings, QUrl, QEventLoop, pyqtSignal, pyqtSlot, qDebug
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from QgisCartoDB.cartodb import CartoDBApi
from QgisCartoDB.utils import CartoDBPluginWorker

from qgis.core import QgsMessageLog


class CartoDBToolbar(QWidget):
    error = pyqtSignal(object)

    def __init__(self, parent=None, flags=Qt.WindowFlags(0)):
        QWidget.__init__(self, parent, flags)
        self.settings = QSettings()
        self.setupUi()
        self.currentUser = self.settings.value('/CartoDBPlugin/selected')

        if self.currentUser:
            self.currentApiKey = self.settings.value('/CartoDBPlugin/%s/api' % self.currentUser)
            self.currentMultiuser = self.settings.value('/CartoDBPlugin/%s/multiuser' % self.currentUser, False)
            self.currentMultiuser = self.currentMultiuser in ['True', 'true', True]
        else:
            self.currentApiKey = None
            self.currentMultiuser = None

        self.click = None

    def setupUi(self):
        self.connectLayout = QHBoxLayout(self)
        self.connectLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.avatarLB = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avatarLB.sizePolicy().hasHeightForWidth())
        self.avatarLB.setSizePolicy(sizePolicy)
        self.avatarLB.setFixedSize(24, 24)
        self.avatarLB.hide()

        self.nameLB = QLabel(self)
        self.nameLB.setFocusPolicy(Qt.ClickFocus)
        self.nameLB.setTextFormat(Qt.RichText)
        self.nameLB.setText("<html><head/><body><p><span style=\"text-decoration: underline; color:#00557f;\">Add Connection</span></p></body></html>")

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.connectLayout.addWidget(self.avatarLB)
        self.connectLayout.addWidget(self.nameLB)

    def getUserData(self, cartodbUser, apiKey, multiuser=False):
        cartoDBApi = CartoDBApi(cartodbUser, apiKey, multiuser)
        cartoDBApi.fetchContent.connect(self.cbUserData)
        cartoDBApi.getUserDetails()

    @pyqtSlot(dict)
    def cbUserData(self, data):
        # QgsMessageLog.logMessage('CartoDBToolbar.py cbUserData'  + str(data) )
        if 'error' in data:
            # TODO Create image for error
            self.nameLB.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:red;\">CARTO: error, check settings</span></p></body></html>")
            self.error.emit(data['error'])
            return

        # save our user info
        self.currentUserData = data['rows'][0]

        # fill in the toolbar to confirm our username
        self.nameLB.setText("<html><head/><body><p>CARTO: {}</p></body></html>".format(self.currentUserData['username']))

    @pyqtSlot()
    def connectCartoDB(self):
        if self.isCurrentUserValid():
            self.getUserData(self.currentUser, self.currentApiKey, self.currentMultiuser)

    def setUserCredentials(self, user, apiKey, multiuser=False):
        self.currentUser = user
        self.currentApiKey = apiKey
        self.currentMultiuser = multiuser
        worker = CartoDBPluginWorker(self, 'connectCartoDB')
        worker.start()

    def isCurrentUserValid(self):
        return self.currentUser is not None and self.currentApiKey is not None

    def mousePressEvent(self, event):
        if self.click is not None:
            self.click()

    def setClick(self, click):
        self.click = click

    def setConnectText(self):
        # TODO Create image for connect text
        self.avatarLB.hide()
        self.nameLB.setText("<html><head/><body><p><span style=\"text-decoration: underline; color:#00557f;\">Connect</span></p></body></html>")

    def reset(self):
        # TODO Create image for add connection
        self.avatarLB.hide()
        self.nameLB.setText("<html><head/><body><p><span style=\"text-decoration: underline; color:#00557f;\">Add Connection</span></p></body></html>")

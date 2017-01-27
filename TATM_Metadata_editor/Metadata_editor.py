# -*- coding: utf-8 -*-
"""
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from Editor import Editor
import resources
import sys
import os
from metadata_provider import MetadataProvider
from standard import MetaInfoStandard

currentPath = os.path.abspath(os.path.dirname(__file__))
class MainPlugin(object):
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.IsRunning=False
    def initGui(self):
         # Create action that will start plugin configuration
        self.action_Editor = QAction(QIcon(":/plugins/Metadata_editor/icons/icon.png"),"TATM_Metadata Editor", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action_Editor, SIGNAL("activated()"), self.run_Editor)

        # Add toolbar button and menu item
        self.iface.addPluginToMenu("TATM_Metadata_Editor", self.action_Editor)
        self.iface.addToolBarIcon(self.action_Editor)

        # track layer changing
        self.iface.currentLayerChanged.connect(self.layerChanged)

        # disable some actions when there is no active layer
        self.layer = None
        self.disableLayerActions()

        # check already selected layers
        self.layerChanged()

    def layerChanged(self):
        if self.IsRunning:
           legend = self.iface.legendInterface()
           if self.iface.activeLayer()!=self.layer:
              legend.setLayerVisible(self.iface.activeLayer(), False)
              self.iface.setActiveLayer(self.layer)
           return
               
        self.layer = self.iface.activeLayer()

        # check layer type - return (True/False, Desc)
        res = MetadataProvider.IsLayerSupport(self.layer)
        if not res[0]:
          self.disableLayerActions()
          self.layer = None
          self.metaProvider = None
        else:
          self.enableLayerActions()
          self.metaProvider = MetadataProvider.getProvider(self.layer)
          self.metaFilePath=self.metaProvider.metaFilePath
          
    def disableLayerActions(self):
        self.action_Editor.setEnabled(False)

    def enableLayerActions(self):
        self.action_Editor.setEnabled(True)

    def checkMetadata(self):
      if not self.metaProvider.checkExists():
        result = QMessageBox.question(self.iface.mainWindow(), u"Μεταδεδομένα",u"Το επιλεγμένο layer δεν έχει μεταδεδομένα! Δημιουργία μεταδεδομένων;", QDialogButtonBox.Yes, QDialogButtonBox.No)

        if result == QDialogButtonBox.Yes:
          try:
            profile ="profile.xml"
            if profile == "":
              QMessageBox.warning(self.iface.mainWindow(),u"Μεταδεδομένα",u"Δεν βρέθηκε το προκαθορισμένο αρχείο προφιλ στη διαδρομή του προσθέτου")
              return False

            profilePath = unicode(QDir.toNativeSeparators(os.path.join(currentPath, "xml_profiles", unicode(profile))))
            self.metaProvider.ImportFromFile(profilePath)
          except:
            QMessageBox.warning(self.iface.mainWindow(),u"Μεταδεδομένα",u"Το αρχείο των μεταδεδομένων δεν ήταν δυνατόν να δημιουργηθεί: " + unicode(sys.exc_info()[1]))
            return False
          return True
        else:
          return False
      else:
        return True

    def unload(self):
    # disconnect signals
        self.iface.currentLayerChanged.disconnect(self.layerChanged)
# Remove the plugin menu item and icon
        self.iface.removePluginMenu("TATM_Metadata_Editor",self.action_Editor)
        self.iface.removeToolBarIcon(self.action_Editor)

    # run
    def run_Editor(self):
        # check if metadata file exists
        if not self.checkMetadata():
          return
        standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)
        if standard != MetaInfoStandard.ISO19115:
          QMessageBox.critical(self.iface.mainWindow(),u"Μεταδεδομένα",u"Τα μεταδεδομένα δεν είναι συμβατά με Inspire!")
          return
   
        self.IsRunning=True
        dlg = Editor(self.iface,self.metaFilePath)
        dlg.setContent(self.metaProvider)
        dlg.exec_()
        self.IsRunning=False
        dlg.removetemplayer()

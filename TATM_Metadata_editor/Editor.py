# -*- coding: utf-8 -*-
# Import the PyQt and QGIS libraries
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys
import os
from xmlISOparser import *
import urllib
from datetime import date
import xml.etree.ElementTree as ET
from xml_writer import *
from random_code_generator import random_code

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

from Ui_Editor import Ui_Editor 

class Editor(QDialog, Ui_Editor):
  def __init__(self,iface,metaFilePath):
    QDialog.__init__(self)
    
    self.setupUi(self)
    self.iface=iface
    self.metaFilePath=metaFilePath
    self.languages={"greek":"gre","english":"eng"}
    self.roles={u"Αρμόδιος για επικοινωνία":"pointOfContact",u"Δημιουργός":"originator",u"Διανομέας":"distributor",u"Εκδότης":"publisher",u"Επεξεργαστής":"processor",u"Κάτοχος":"owner",u"Πάροχος των δεδομένων":"resourceProvider",u"Πρωτεύων διερευνητής":"principalInvestigator",u"Συντάκτης":"author",u"Υπόλογος":"custodian",u"Χρήστης":"user"}
    self.categories={u"":u"",u"Βιόκοσμος":"biota", u"Γεωγραφική θέση":"location", u"Γεωεπιστημονικές πληροφορίες":"geoscientificInformation", u"Γεωργία":"farming", u"Επιχειρήσεις κοινής ωφελείας/Επικοινωνία":"utilitiesCommunication", u"Εσωτερικά ύδατα":"inlandWaters",  u"Θάλασσες":"oceans",  u"Κατασκευές":"structure",  u"Κλιματολογία/Μετεωρολογία/Ατμόσφαιρα":"climatologyMeteorologyAtmosphere",  u"Κοινωνία":"society",  u"Μεταφορές":"transportation",  u"Οικονομία":"economy",  u"Ορθοεικόνες/Βασικοί χάρτες/Κάλυψη γης":"imageryBaseMapsEarthCover",  u"Περιβάλλον":"environment",  u"Στρατιωτικές πληροφορίες":"intelligenceMilitary",  u"Υγεία":"health",  u"Υψομετρία":"elevation",  u"Χωροταξία/Κτηματολόγιο":"planningCadastre",  u"Όρια":"boundaries"}
    self.inspirekeys=[u"",u"Έδαφος",u"Ανθρώπινη υγεία και ασφάλεια",u"Ατμοσφαιρικές συνθήκες",u"Βιογεωγραφικές περιοχές",u"Γεωλογία",u"Γεωργικές εγκαταστάσεις και εγκαταστάσεις υδατοκαλλιέργειας",u"Γεωτεμάχια κτηματολογίου",u"Δίκτυα μεταφορών",u"Διευθύνσεις",u"Διοικητικές ενότητες",u"Εγκαταστάσεις παραγωγής και βιομηχανικές εγκαταστάσεις",u"Εγκαταστάσεις παρακολούθησης του περιβάλλοντος",u"Ενδιαιτήματα και βιότοποι",u"Ενεργειακοί πόροι",u"Επιχειρήσεις κοινής ωφελείας και κρατικές υπηρεσίες",u"Ζώνες διαχείρισης/περιορισμού/ρύθμισης εκτάσεων και μονάδες αναφοράς    ",u"Ζώνες φυσικών κινδύνων",u"Θαλάσσιες περιοχές",u"Κάλυψη γης",u"Κατανομή ειδών",u"Κατανομή πληθυσμού — δημογραφία",u"Κτίρια",u"Μετεωρολογικά γεωγραφικά χαρακτηριστικά",u"Ορθοφωτογραφία",u"Ορυκτοί πόροι",u"Προστατευόμενες τοποθεσίες",u"Στατιστικές μονάδες",u"Συστήματα γεωγραφικού καννάβου",u"Συστήματα συντεταγμένων",u"Τοπωνύμια",u"Υδρογραφία",u"Υψομετρία",u"Χρήσεις γης",u"Ωκεανογραφικά γεωγραφικά χαρακτηριστικά"]
    self.uselim=[u"",u"δεν ισχύουν όροι",u"άγνωστοι όροι"]
    self.otherconstraints=[u"",u"no limitation"]
    self.datetype={u"Ημερομηνία δημιουργίας":"creation",u"Ημερομηνία δημοσίευσης":"publication",u"Ημερομηνία τελευταίας αναθεώρησης":"revision"}
    self.completer()
    self.makeHelp()
  
    self.simorfosi={u"Κανονισμός (ΕΚ) αριθ. 1205/2008 της Επιτροπής της 3ης Δεκεμβρίου 2008 για εφαρμογή της οδηγίας 2007/2/ΕΚ του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου όσον αφορά τα μεταδεδομένα":"2008-12-04",\
    u"Διορθωτικό στον κανονισμό (ΕΚ) αριθ. 1205/2008 της Επιτροπής, της 3ης Δεκεμβρίου 2008, για εφαρμογή της οδηγίας 2007/2/ΕΚ του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου όσον αφορά τα μεταδεδομένα":"2009-12-15",\
    u"Κανονισμός (ΕΕ) αριθ. 1089/2010 της Επιτροπής της 23ης Νοεμβρίου 2010 σχετικά με την εφαρμογή της οδηγίας 2007/2/ΕΚ του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου όσον αφορά τη διαλειτουργικότητα των συνόλων και των υπηρεσιών χωρικών δεδομένων":"2010-12-08",\
    u"Κανονισμός (ΕΕ) αριθ. 1088/2010 της Επιτροπής, της 23ης Νοεμβρίου 2010, για τροποποίηση του κανονισμού (ΕΚ) αριθ. 976/2009 όσον αφορά στις υπηρεσίες τηλεφόρτωσης και τις υπηρεσίες μετασχηματισμού":"2010-12-08",\
    u"Κανονισμός (ΕΚ) αριθ. 976/2009 της Επιτροπής της 19ης Οκτωβρίου 2009 για την υλοποίηση της οδηγίας 2007/2/ΕΚ του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου όσον αφορά τις δικτυακές υπηρεσίες":"2009-10-20",\
    u"Κανονισμός (ΕΕ) αριθ. 268/2010 της Επιτροπής της 29ης Μαρτίου 2010 για την εφαρμογή της οδηγίας 2007/2/ΕΚ του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου όσον αφορά την πρόσβαση των θεσμικών οργάνων και οργανισμών της Κοινότητας σε σύνολα και υπηρεσίες χωρικών δεδομένων των κρατών μελών υπό εναρμονισμένους όρους":"2010-03-30",\
    u"Απόφαση της Επιτροπής της 5ης Ιουνίου 2009 για την εφαρμογή της οδηγίας 2007/2/ΕΚ του Ευρωπαϊκού Κοινοβουλίου και του Συμβουλίου όσον αφορά την παρακολούθηση και την υποβολή εκθέσεων [κοινοποιηθείσα υπό τον αριθμό Ε(2009) 4199] (2009/442/ΕΚ)":"2009-06-11"}
    self.doubleSpinBox_7_1.setEnabled(False)
    self.comboBox_7_1.setEnabled(False)
    self.hascalledlist=None
    
    self.dateEdit.setDate(date.today())
    self.dateEdit_6_1.setDate(date.today())
    self.dateEdit_6_2.setDate(date.today())
    self.dateEdit_6_3.setDate(date.today())
    self.dateEdit_6_4.setDate(date.today())
    self.dateEdit_6.setDate(date.today())
    self.dateEdit_8_1.setDate(date.today())
    self.radioButton.setChecked(True)  
    
    QtCore.QObject.connect(self.lineEdit_5_1, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onCoordChanged)
    QtCore.QObject.connect(self.lineEdit_5_2, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onCoordChanged)
    QtCore.QObject.connect(self.lineEdit_5_3, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onCoordChanged)
    QtCore.QObject.connect(self.lineEdit_5_4, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.onCoordChanged)
    QtCore.QObject.connect(self.toolButton_5_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.zoomIn) #zoomin
    QtCore.QObject.connect(self.toolButton_5_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.zoomOut) #zoomout
    
    QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.complete1)
    QtCore.QObject.connect(self.listWidget_2, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.complete2)
    QtCore.QObject.connect(self.checkBox_10, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.complete2)
    QtCore.QObject.connect(self.listWidget_8_1, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.complete_simorfosi)
    self.listWidget_8_1.setVisible(False)
    
    self.mapCanvas =QgsMapCanvas()
    self.mapCanvas.useImageToRender(False)
    self.mapCanvas.setCanvasColor(Qt.white)
    QtCore.QObject.connect(self.toolButton_5_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.mapCanvas.refresh) #refresh

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.mapCanvas)
    self.widget.setLayout(layout)

    #add wms1
    urlWithParams = 'contextualWMSLegend=0&crs=EPSG:4258&dpiMode=7&featureCount=10&format=image/png&layers=eygep:oikismoi&styles=&url=http://www1.okxe.gr/geoserver/ows'
    self.templayer2 = QgsRasterLayer(urlWithParams, 'WMS-oikismoi', 'wms')
    QgsMapLayerRegistry.instance().addMapLayer(self.templayer2)
    #add wms2
    urlWithParams ='contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=KTBASEMAP&styles=&url=http://gis.ktimanet.gr/wms/wmsopen/wmsserver.aspx?'
    self.templayer = QgsRasterLayer(urlWithParams, 'WMS-THE BASEMAP OF KTIMATOLOGIO', 'wms')
    QgsMapLayerRegistry.instance().addMapLayer(self.templayer)
    
    self.mapCanvas.setLayerSet([QgsMapCanvasLayer(self.templayer2),QgsMapCanvasLayer(self.templayer)])
    self.mapCanvas.zoomToFullExtent()
    self.mapCanvas.refresh()
    self.toolPan = QgsMapToolPan(self.mapCanvas)
    self.mapCanvas.setMapTool(self.toolPan)

    for key in self.simorfosi:
       self.listWidget_8_1.addItem(key)
    
    for key in self.languages:
       self.comboBox.addItem(key)
       self.comboBox_2.addItem(key)
    for key in self.roles:
       self.comboBox_10_1.addItem(key)
    for key in self.categories:
       self.comboBox_3_1.addItem(key)
    for key in self.inspirekeys:
       self.comboBox_4_1.addItem(key)
    for key in self.uselim:
       self.comboBox_9_1.addItem(key)
    for key in self.otherconstraints:
       self.comboBox_9_2.addItem(key)
       
    self.closeButton=QtGui.QPushButton()
    self.saveButton=QtGui.QPushButton()
    self.closeButton.setText(_translate("Editor", "Κλείσιμο", None))
    self.saveButton.setText(_translate("Editor", "Αποθήκευση", None))
    self.buttonBox.addButton(self.closeButton,QtGui.QDialogButtonBox.RejectRole)
    self.buttonBox.addButton(self.saveButton,QtGui.QDialogButtonBox.AcceptRole)
        
    QObject.connect(self.closeButton,SIGNAL("clicked()"),self.close) #self.buttonBox.button(QtGui.QDialogButtonBox.AcceptRole).clicked.connect(self.close)
    QObject.connect(self.saveButton,SIGNAL("clicked()"),self.makesave)

    QObject.connect(self.pushButton_2_random,SIGNAL("clicked()"),self.random_code)

  def setContent(self, metaProvider):  #setContent
    self.metaProvider = metaProvider
##
    self.GetDataFromXML(self.metaFilePath)

  def GetDataFromXML(self, fileName):
        zIndex = self.tabWidget.currentIndex()
        try : tree = ET.parse(fileName)
        except :
           QMessageBox.warning(self.iface.mainWindow(),u"Μεταδεδομένα",u"Μη έγκυρο αρχείο μεταδεδομένων XML!")
           return
        root = tree.getroot()

        if root.tag != '{http://www.isotc211.org/2005/gmd}MD_Metadata':
           QMessageBox.warning(self.iface.mainWindow(),u"Μεταδεδομένα",u"Τα μεταδεδομένα δεν είναι συμβατά με Inspire! (δεν βρέθηκε η φράση gmd:MD_Metadata) !")
           return
        
        self.listImportCategories = []
        self.langueTR=None
        myISO = xmlISOparser(fileName, None, 'MEDDE', self.langueTR)

        zCond = myISO.getTagDictionnary()

        if not zCond :
           QMessageBox.warning(self.iface.mainWindow(),u"Μεταδεδομένα",u"Μη έγκυρο αρχείο μεταδεδομένων XML!")
           return                

        self.ReloadDataFromXML(myISO, fileName, zIndex)

  def random_code(self):
     self.lineEdit_2_3.setText(random_code())

  def ReloadDataFromXML(self, myISO, fileName, zIndex):

        myISO.createISOdataStructure(True)
        
        zorderkeys = ("intitule", "resume", "typedata", "tablelocalisator", "identificator", "tablelangues", "tableformats", "tablecarac", \
                      "tablecategories", "tablecategories:0", "tablemotsclefsf", "tablescr", "tableemprises", "tableetenduetemporelle", "groups:dates", \
                      "genealogie", "coherence", "grouperesolutionscale", "tablespecifications", "groupedroits", "licence", "tableroles:1", "tableroles:2", "tableroles:3", \
                      "datemetada", "langmetada", "otherconstraints")

        zWidgetValues = {"intitule": myISO.title , "resume" : myISO.abstract, "typedata": myISO.typedata, "tablelocalisator" : myISO.localisators, \
                         "identificator" : myISO.UUID, "tablelangues" : myISO.languesjdd, "tableformats" : myISO.formatsjdd, "tablecarac": myISO.tablecarac,  \
                         "tablecategories" : myISO.categories, "tablecategories:0" : myISO.codecategories, "tablemotsclefsf" : myISO.keywordsF, \
                         "tablescr" : myISO.scr, "tableemprises" : myISO.boundingboxcoordinates, \
                         "tableetenduetemporelle" : myISO.timeperiodes, "groups:dates" : myISO.dates, \
                         "genealogie" : myISO.genealogie, "coherence" : myISO.coherence, "grouperesolutionscale" : myISO.scalesEC, \
                         "tablespecifications": myISO.firstSpecification, "groupedroits" : myISO.accessconstraints, "licence" : myISO.legalconstraints, \
                         "tableroles:1" : myISO.pointsofcontactMDD, "tableroles:2" : myISO.pointsofcontact, "tableroles:3" : myISO.pointsofcontactCust, \
                         "datemetada" : (myISO.datemdd, myISO.datetmdd ), "langmetada" : myISO.languemdd, "otherconstraints":myISO.otherconstraints
                         }

        QObject.connect(self.toolButton_2_7,SIGNAL("clicked()"),self.addLine)
        QObject.connect(self.toolButton_2_8,SIGNAL("clicked()"),self.delLine)
        QObject.connect(self.toolButton_3_2,SIGNAL("clicked()"),self.addCombo)
        QObject.connect(self.toolButton_3_3,SIGNAL("clicked()"),self.delCombo)
        
        QObject.connect(self.pushButton,SIGNAL("clicked()"),self.addInspire)
        QObject.connect(self.toolButton_4_1,SIGNAL("clicked()"),self.delInspire)
        QObject.connect(self.pushButton_2,SIGNAL("clicked()"),self.addFree)
        QObject.connect(self.toolButton_4_2,SIGNAL("clicked()"),self.delFree)
        
        QObject.connect(self.toolButton_10_3,SIGNAL("clicked()"),self.addGroup)
        QObject.connect(self.toolButton_10_5,SIGNAL("clicked()"),self.delGroup)

        QObject.connect(self.toolButton_9_1,SIGNAL("clicked()"),self.addCombo1)
        QObject.connect(self.toolButton_9_2,SIGNAL("clicked()"),self.delCombo1)
        QObject.connect(self.toolButton_9_3,SIGNAL("clicked()"),self.addCombo2)
        QObject.connect(self.toolButton_9_4,SIGNAL("clicked()"),self.delCombo2)

        QObject.connect(self.pushButton_5_1,SIGNAL("clicked()"),self.getCoordinates)
        #self.pushButton_5_2.setCheckable(True)

        QObject.connect(self.pushButton_5_2,SIGNAL("clicked()"),self.getCoordinates2)
        
        for key in zorderkeys:
            temp=zWidgetValues[key]
                
            if key=="intitule" and temp!=[[]]:
               temp0=temp[0]
               self.lineEdit_2_1.setText(temp0[0])
            elif key=="resume" and temp!=[[]]:
                temp0=temp[0]
                self.textEdit.setText(temp0[0])
            elif key=="tablelocalisator" and temp!=[[], []]:     
                temp0=temp[0]
                try:
                   self.lineEdit_2_6.setText(temp0[0])
                except: pass
                for n in range(1,len(temp0)):
                   self.addLine()
                   line="self.lineEdit_2_A_"+str(n)+".setText(temp0["+str(n)+"])"
                   eval(line)
                        
            elif key=="identificator" and temp!=[[]]:
               temp0=temp[0]
               self.lineEdit_2_3.setText(temp0[0])
               temp2=myISO.rs_identifier2
               if temp2!=[[]]:
                  temp0=temp2[0]
                  self.lineEdit_2_2.setText(temp0[0])
            elif key=="tablelangues" and temp!=[[]]:
               temp0=temp[0]
               try:
                  index = self.comboBox_2.findText(self.languages.keys()[self.languages.values().index(temp0[0])])
                  if index >= 0:
                     self.comboBox_2.setCurrentIndex(index)
               except: pass
            elif key=="tablecategories" and temp!=[[]]:        
               temp0=temp[0]
               inspire_k=0
               free_k=0
               for k in range(len(temp0)):

                  if temp[0][k] in self.inspirekeys:
                      inspire_k+=1
                      if inspire_k==1:
                         index=self.comboBox_4_1.findText(temp[0][k])
                         if index >= 0:
                            self.comboBox_4_1.setCurrentIndex(index)
                      else:
                         self.addInspire()
                         add_combo="self.comboBox_4_A_"+str(inspire_k-1)
                         index=self.comboBox_4_1.findText(temp[0][k])
                         if index >= 0:
                             eval(add_combo+".setCurrentIndex("+str(index)+")")

                  else:

                     self.addFree()
                     add_line="self.lineEdit_4_A_"+str(free_k)+".setText(temp0["+str(k)+"])"
                     eval(add_line)
                     free_k+=1
               
            elif key=="tablecategories:0"and temp!=[[]]:         
               temp0=temp[0]
               index = self.comboBox_3_1.findText(self.categories.keys()[self.categories.values().index(temp0[0])])
               if index >= 0:
                  self.comboBox_3_1.setCurrentIndex(index)
               for n in range(1,len(temp0)):
                  self.addCombo()
                  index=self.comboBox_3_A_1.findText(self.categories.keys()[self.categories.values().index(temp0[n])])
                  if index >= 0:
                     combo="self.comboBox_3_A_"+str(n)+".setCurrentIndex("+str(index)+")"
                     eval(combo)
            elif key=="tableemprises" and temp!=[[], [], [], []]:
               temp0=temp[0]
               self.lineEdit_5_1.setText(temp0["north"])
               self.lineEdit_5_2.setText(temp0["east"])
               self.lineEdit_5_3.setText(temp0["south"])
               self.lineEdit_5_4.setText(temp0["west"])
            elif key=="tableetenduetemporelle" and temp!=[[], []]:
               self.groupBox_6_5.setChecked(True)
               temp0=temp[0]
               self.dateEdit_6_4.setDate(QDate.fromString(temp0["start"], "yyyy-MM-dd"))
               if temp0["end"]==" ":
                  self.radioButton.setChecked(True)
               else:
                  self.radioButton_2.setChecked(True)
                  self.dateEdit_6.setDate(QDate.fromString(temp0["end"], "yyyy-MM-dd"))
            elif key=="groups:dates" and temp!=[[], []]:
               for n in range(len(temp)):
                  if temp[n]["type"]=="creation":
                      self.groupBox_6_2.setChecked(True)
                      self.dateEdit_6_1.setDate(QDate.fromString(temp[n]["date"], "yyyy-MM-dd"))
                  elif temp[n]["type"]=="publication":
                      self.groupBox_6_3.setChecked(True)
                      self.dateEdit_6_2.setDate(QDate.fromString(temp[n]["date"], "yyyy-MM-dd"))
                  elif temp[n]["type"]=="revision":
                      self.groupBox_6_4.setChecked(True)
                      self.dateEdit_6_3.setDate(QDate.fromString(temp[n]["date"], "yyyy-MM-dd"))
            elif key=="genealogie" and  temp!=[[]]:
               temp0=temp[0]
               self.textEdit_7_1.setText(temp0[0])
            elif key=="grouperesolutionscale":
               if temp!=[[]]:
                  temp0=temp[0]

                  self.radioButton_7_1.setChecked(True)
                  self.spinBox_7_1.setValue(int(temp0[0]))
               else:
                  try:
                     zUnits=myISO.UnitsScalesUM[0][0]['uom']
                     zInfos = myISO.scalesUM[0]
                     #print "zUnits", zUnits,float(zInfos[0])
                     self.radioButton_7_2.setChecked(True)
                     self.doubleSpinBox_7_1.setValue(float(zInfos[0]))
                     try:
                        index = self.comboBox_7_1.findText(zUnits, Qt.MatchFixedString)
                        if index >= 0:
                           self.comboBox_7_1.setCurrentIndex(index)
                        else:
                           self.radioButton_7_1.setChecked(True)
                     except: pass
                  except: self.radioButton_7_1.setChecked(True)

            elif key=="tablespecifications" and temp!=[None,None,None,None]:
               self.groupBox_8_2.setChecked(True)
               if temp[0]!=None:self.lineEdit_8_1.setText(temp[0])

               if temp[1]!=None:self.dateEdit_8_1.setDate(QDate.fromString(temp[1], "yyyy-MM-dd"))
               if temp[2]=="publication":
                  self.comboBox_8_2.setCurrentIndex(1)
               elif temp[2]=="creation":
                  self.comboBox_8_2.setCurrentIndex(0)
               elif temp[2]=="revision":
                  self.comboBox_8_2.setCurrentIndex(2)
               if temp[3]==None:
                  self.comboBox_8_3.setCurrentIndex(0)
               elif temp[3]=="false":
                  self.comboBox_8_3.setCurrentIndex(1)
               elif temp[3]=="true":
                  self.comboBox_8_3.setCurrentIndex(2)

            elif key=="tableroles:1" and temp!=[['pointOfContact'], [], [], [], [], [], []]:

               if temp[1]!=[]:
                  self.lineEdit.setText(temp[1][0]) 
               if temp[6]!=[]:
                  self.lineEdit_2.setText(temp[6][0])
               if temp[4]!=[]:
                  self.lineEdit_3.setText(temp[4][0])
               if temp[5]!=[]:
                  self.lineEdit_4.setText(temp[5][0])
               
            elif key=="tableroles:2" and temp!=[[], [], [], [], [], [], []]:

               try:
                  index = self.comboBox_10_1.findText(self.roles.keys()[self.roles.values().index(temp[0][0])])
                  if index >= 0:
                     self.comboBox_10_1.setCurrentIndex(index)
               except: pass
               self.lineEdit_10_1.setText(temp[1][0])

               if myISO.orgfirstmail[temp[1][0]][0]!=None: self.lineEdit_10_2.setText(myISO.orgfirstmail[temp[1][0]][0])
               if myISO.orgfirstmail[temp[1][0]][2]!=None: self.lineEdit_10_3.setText(myISO.orgfirstmail[temp[1][0]][2])
               if myISO.orgfirstmail[temp[1][0]][1]!=None: self.lineEdit_10_4.setText(myISO.orgfirstmail[temp[1][0]][1])
               
               for n in range(1,len(temp[0])):
                  self.addGroup()
                  try:
                     index=self.comboBox_10_A_1.findText(self.roles.keys()[self.roles.values().index(temp[0][n])])
                     if index >= 0:
                        combo="self.comboBox_10_A_"+str(n)+".setCurrentIndex("+str(index)+")"
                        eval(combo)
                  except: pass
                  line1="self.lineEdit_10_A_"+str(n)+".setText(temp[1]["+str(n)+"])"
                  if myISO.orgfirstmail[temp[1][n]][0]!=None:
                     line2="self.lineEdit_10_B_"+str(n)+".setText(myISO.orgfirstmail[temp[1]["+str(n)+"]][0])"
                     eval(line2)
                  eval(line1)

                  if myISO.orgfirstmail[temp[1][n]][2]!=None:
                     lineurl="self.lineEdit_10_url_"+str(n)+".setText(myISO.orgfirstmail[temp[1]["+str(n)+"]][2])"
                     eval(lineurl)
                  if myISO.orgfirstmail[temp[1][n]][1]!=None:
                     linephone="self.lineEdit_10_phone_"+str(n)+".setText(myISO.orgfirstmail[temp[1]["+str(n)+"]][1])"
                     eval(linephone)
               
            elif key=="datemetada" and temp!=([[]], [[]]):
               self.dateEdit.setDate(QDate.fromString(temp[0][0][0], "yyyy-MM-dd"))
            elif key=="langmetada" and temp!=[[]]:
               temp0=temp[0]
               index = self.comboBox.findText(self.languages.keys()[self.languages.values().index(temp0[0])])
               if index >= 0:
                  self.comboBox.setCurrentIndex(index)
            elif key=="licence" and temp!=[[]]: ####
               self.comboBox_9_1.setEditText(temp[0][0])
               for n in range(1,len(temp[0])): 
                  self.addCombo1()
                  combo="self.comboBox_9_A_"+str(n)+".setEditText(temp[0][n])"
                  eval(combo)
            
            elif key=="otherconstraints" and temp!=[[]]:   ###
               self.comboBox_9_2.setEditText(temp[0][0])
               for n in range(1,len(temp[0])): 
                  self.addCombo2()
                  combo="self.comboBox_9_B_"+str(n)+".setEditText(temp[0][n])"
                  eval(combo)

  def delLine(self):
        i=self.gridLayout_30.count()
        tmp=self.gridLayout_30.itemAt(i-1)
        if tmp != None and i>4: self.gridLayout_30.itemAt(i-1).widget().setParent(None)
  def addLine(self):
        i=self.gridLayout_30.count()-3
        add_group="self.groupBox_2_A_"+str(i)
        scroll0="QtGui.QGroupBox(self.scrollAreaWidgetContents_2_3)"
        exec("%s=%s" % (add_group,scroll0))
        subgrid="self.gridLayout_2_A_"+str(i)
        temp="QtGui.QGridLayout("+add_group+")"
        exec("%s=%s" % (subgrid,temp))
        add_line="self.lineEdit_2_A_"+str(i)
        temp="QtGui.QLineEdit("+add_group+")"
        exec("%s=%s" % (add_line,temp))
        temp=subgrid+".addWidget("+add_line+", 0, 0, 1, 1)"
        eval(temp)
        temp="self.gridLayout_30.addWidget("+add_group+", "+str(i)+", 0, 1, 1)"
        eval(temp)
        temp=add_group+".setTitle(_translate(\"Editor\", \"Διεύθυνση URL γεωγραφικών δεδομένων- Link "+str(i+1)+" (*)\", None))"
        eval(temp)
        
  def addCombo(self):
        i=self.gridLayout_44.count()-4
        if i>=19: return
        add_combo="self.comboBox_3_A_"+str(i)
        exec("%s=%s" % (add_combo,"QtGui.QComboBox(self.groupBox_3_2)"))
        temp="self.gridLayout_44.addWidget("+add_combo+", "+str(i)+", 0, 1, 1)"
        eval(temp)
        for key in self.categories:
           self.gridLayout_44.itemAt(i-1+5).widget().addItem(key)
  def delCombo(self):
        i=self.gridLayout_44.count()
        tmp=self.gridLayout_44.itemAt(i-1)
        if tmp != None and i>5: self.gridLayout_44.itemAt(i-1).widget().setParent(None)
  def addFree(self):
        i=self.gridLayout_49.count()
        add_line="self.lineEdit_4_A_"+str(i)
        exec("%s=%s" % (add_line,"QtGui.QLineEdit(self.scrollAreaWidgetContents_4_2)"))
        temp="self.gridLayout_49.addWidget("+add_line+", "+str(i)+", 0, 1, 1)"
        eval(temp)
  def delFree(self):
        i=self.gridLayout_49.count()
        if i>0:
           tmp=self.gridLayout_49.itemAt(i-1)
        else:
           tmp=None
        if tmp != None and i>0: self.gridLayout_49.itemAt(i-1).widget().setParent(None)
  def addInspire(self):
        i=self.gridLayout_48.count()
        add_combo="self.comboBox_4_A_"+str(i)
        exec("%s=%s" % (add_combo,"QtGui.QComboBox(self.scrollAreaWidgetContents_4_1)"))
        temp="self.gridLayout_48.addWidget("+add_combo+", "+str(i+1)+", 0, 1, 1)"
        eval(temp)
        for key in self.inspirekeys:
           self.gridLayout_48.itemAt(i).widget().addItem(key)
  def delInspire(self):
        i=self.gridLayout_48.count()
        tmp=self.gridLayout_48.itemAt(i-1)
        if tmp != None and i>1: self.gridLayout_48.itemAt(i-1).widget().setParent(None)
  
  def addGroup(self):
        i=self.gridLayout_76.count()-3
        add_group="self.groupBox_10_A_"+str(i)
        scroll0="QtGui.QGroupBox(self.scrollAreaWidgetContents_10_1)"
        exec("%s=%s" % (add_group,scroll0))#self.groupBox_10_2 = QtGui.QGroupBox(self.scrollAreaWidgetContents_10_1)
        grid="self.gridLayout_10_A_"+str(i)
        temp="QtGui.QGridLayout("+add_group+")"
        exec("%s=%s" % (grid,temp)) #self.gridLayout_77 = QtGui.QGridLayout(self.groupBox_10_2)

        subgroup1="self.groupBox_10_B_"+str(i)
        subgroup2="self.groupBox_10_C_"+str(i)
        subgroup3="self.groupBox_10_D_"+str(i)
        subgroup_url="self.groupBox_10_url_"+str(i)
        subgroup_phone="self.groupBox_10_phone_"+str(i)

        tempG="QtGui.QGroupBox("+add_group+")"
        exec("%s=%s" % (subgroup1,tempG))#self.groupBox_10_5 = QtGui.QGroupBox(self.groupBox_10_2)
        subgrid1=grid+"_1"
        subgrid2=grid+"_2"
        subgrid3=grid+"_3"
        subgrid_url=grid+"_url"
        subgrid_phone=grid+"_phone"
        add_line_url="self.lineEdit_10_url_"+str(i)
        add_line_phone="self.lineEdit_10_phone_"+str(i)

        tempGr="QtGui.QGridLayout("+subgroup1+")"
        exec("%s=%s" % (subgrid1,tempGr))#self.gridLayout_78 = QtGui.QGridLayout(self.groupBox_10_5)

        add_combo="self.comboBox_10_A_"+str(i)
        add_line1="self.lineEdit_10_A_"+str(i)
        add_line2="self.lineEdit_10_B_"+str(i)
        add_check="self.checkBox_10_A_"+str(i) #self.checkBox_10= QtGui.QCheckBox(self.groupBox_10_3)
                                               #self.checkBox_10.setObjectName(_fromUtf8("checkBox_10"))
                                               #self.gridLayout_80.addWidget(self.checkBox_10, 2, 0, 1, 1)
        temp="QtGui.QComboBox("+subgroup1+")"
        exec("%s=%s" % (add_combo,temp))      #self.comboBox_10_1 = QtGui.QComboBox(self.groupBox_10_5)
        
        for key in self.roles:
           temp=add_combo+".addItem(key)"
           eval(temp)              #self.comboBox_10_1.addItem(u"Αρμόδιος για επικοινωνία")
        
        temp=subgrid1+".addWidget("+add_combo+", 0, 0, 1, 1)"     #self.gridLayout_78.addWidget(self.comboBox_10_1, 0, 0, 1, 1) 
        eval(temp)
        
        spacerItem41 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
        temp=subgrid1+".addItem(spacerItem41, 0, 1, 1, 1)"
        eval(temp)                       #self.gridLayout_78.addItem(spacerItem41, 0, 1, 1, 1)
     
        temp=grid+".addWidget("+subgroup1+", 2, 0, 1, 1)"
        eval(temp)                    #self.gridLayout_77.addWidget(self.groupBox_10_5, 2, 0, 1, 1)
        
        exec("%s=%s" % (subgroup2,tempG))            #self.groupBox_10_4 = QtGui.QGroupBox(self.groupBox_10_2)
        
        tempGr="QtGui.QGridLayout("+subgroup2+")"
        exec("%s=%s" % (subgrid2,tempGr))          #self.gridLayout_79 = QtGui.QGridLayout(self.groupBox_10_4)

        temp="QtGui.QLineEdit("+subgroup2+")"
        exec("%s=%s" % (add_line2,temp))          #self.lineEdit_10_2 = QtGui.QLineEdit(self.groupBox_10_4)
        
        
        temp=subgrid2+".addWidget("+add_line2+", 0, 0, 1, 1)"
        eval(temp)                                            #self.gridLayout_79.addWidget(self.lineEdit_10_2, 0, 0, 1, 1)
        
        temp=grid+".addWidget("+subgroup2+", 1, 0, 1, 1)"
        eval(temp)                                   #self.gridLayout_77.addWidget(self.groupBox_10_4, 1, 0, 1, 1)
#
        exec("%s=%s" % (subgroup_url,tempG))
        
        tempGr="QtGui.QGridLayout("+subgroup_url+")"
        exec("%s=%s" % (subgrid_url,tempGr))

        temp="QtGui.QLineEdit("+subgroup_url+")"
        exec("%s=%s" % (add_line_url,temp))   
        
        
        temp=subgrid_url+".addWidget("+add_line_url+", 0, 0, 1, 1)"
        eval(temp)                                
        
        temp=grid+".addWidget("+subgroup_url+", 3, 0, 1, 1)"
        eval(temp)

        exec("%s=%s" % (subgroup_phone,tempG))
        
        tempGr="QtGui.QGridLayout("+subgroup_phone+")"
        exec("%s=%s" % (subgrid_phone,tempGr))

        temp="QtGui.QLineEdit("+subgroup_phone+")"
        exec("%s=%s" % (add_line_phone,temp))   
        
        temp=subgrid_phone+".addWidget("+add_line_phone+", 0, 0, 1, 1)"
        eval(temp)                                
        
        temp=grid+".addWidget("+subgroup_phone+", 4, 0, 1, 1)"
        eval(temp)
#
        exec("%s=%s" % (subgroup3,tempG)) #self.groupBox_10_3 = QtGui.QGroupBox(self.groupBox_10_2)

        tempGr="QtGui.QGridLayout("+subgroup3+")"
        exec("%s=%s" % (subgrid3,tempGr)) #self.gridLayout_80 = QtGui.QGridLayout(self.groupBox_10_3)

        temp="QtGui.QLineEdit("+subgroup3+")"
        exec("%s=%s" % (add_line1,temp))  #self.lineEdit_10_1 = QtGui.QLineEdit(self.groupBox_10_3)
        temp="QtGui.QCheckBox("+subgroup3+")"
        exec("%s=%s" % (add_check,temp))
        
        temp=subgrid3+".addWidget("+add_line1+", 0, 0, 1, 1)"
        eval(temp)  #self.gridLayout_80.addWidget(self.lineEdit_10_1, 0, 0, 1, 1)
        
        temp=subgrid3+".addWidget("+add_check+", 2, 0, 1, 1)"
        eval(temp)
        
        temp=grid+".addWidget("+subgroup3+", 0, 0, 1, 1)"
        eval(temp)   #self.gridLayout_77.addWidget(self.groupBox_10_3, 0, 0, 1, 1)
        
        temp="self.gridLayout_76.addWidget("+add_group+", "+str(i+1)+", 0, 1, 1)"
        eval(temp)  #self.gridLayout_76.addWidget(self.groupBox_10_2, 1, 0, 1, 1)
        
        temp=add_group+".setTitle(_translate(\"Editor\", \"Αρμόδιο μέρος "+str(i+1)+" (*)\", None))"
        eval(temp)
        temp=subgroup1+".setTitle(_translate(\"Editor\", \"Ρόλος του αρμόδιου μέρους (*)\", None))"
        eval(temp)
        temp=subgroup2+".setTitle(_translate(\"Editor\", \"Ηλεκτρονική διεύθυνση (*)\", None))"
        eval(temp)
        temp=subgroup3+".setTitle(_translate(\"Editor\", \"Oνομασία του οργανισμού (*)\", None))"
        eval(temp)

        temp=subgroup_url+".setTitle(_translate(\"Editor\", \"Ιστότοπος (Προαιρετικό)\", None))"
        eval(temp)
        temp=subgroup_phone+".setTitle(_translate(\"Editor\", \"Τηλέφωνο (Προαιρετικό)\", None))"
        eval(temp)
        
        eval(add_check+".setObjectName(_fromUtf8(\"checkBox_10_A_"+str(i)+"\"))")
        eval("QObject.connect("+add_check+", QtCore.SIGNAL(_fromUtf8(\"clicked(bool)\")), self.listWidget_2.setVisible)")
        eval(add_check+".setText(_translate(\"Editor\", \"Επιλογή από λίστα\", None))")
        eval("QObject.connect("+add_check+", QtCore.SIGNAL(_fromUtf8(\"clicked(bool)\")), self.complete2)")
        
  def delGroup(self):
        i=self.gridLayout_76.count()
        tmp=self.gridLayout_76.itemAt(i-1)
        if tmp != None and i>4: self.gridLayout_76.itemAt(i-1).widget().setParent(None)
  
  def addCombo1(self):
        i=self.gridLayout_72.count()-1
        add_combo="self.comboBox_9_A_"+str(i)
        exec("%s=%s" % (add_combo,"QtGui.QComboBox(self.groupBox_9_2)"))
        temp=add_combo+".setEditable(True)"
        eval(temp)
        temp="self.gridLayout_72.addWidget("+add_combo+", "+str(i)+", 0, 1, 1)"
        eval(temp)
        for key in self.uselim:
           temp=add_combo+".addItem(key)"
           eval(temp)
  
  def delCombo1(self):
        i=self.gridLayout_72.count()
        tmp=self.gridLayout_72.itemAt(i-1)
        if tmp != None and i>2: self.gridLayout_72.itemAt(i-1).widget().setParent(None)
  
  def addCombo2(self):
        i=self.gridLayout_73.count()-1
        add_combo="self.comboBox_9_B_"+str(i)
        exec("%s=%s" % (add_combo,"QtGui.QComboBox(self.groupBox_9_2)"))
        temp=add_combo+".setEditable(True)"
        eval(temp)
        temp="self.gridLayout_73.addWidget("+add_combo+", "+str(i)+", 0, 1, 1)"
        eval(temp)
        for key in self.otherconstraints:
           temp=add_combo+".addItem(key)"
           eval(temp)
  
  def delCombo2(self):
        i=self.gridLayout_73.count()
        tmp=self.gridLayout_73.itemAt(i-1)
        if tmp != None and i>2: self.gridLayout_73.itemAt(i-1).widget().setParent(None)

  def makesave(self):
     if self.Empty_cell():
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                u"Δεν έχετε συμπληρώσει υποχρεωτικά πεδία!      ", u"Θέλετε σίγουρα να συνεχίσετε;",
                QtGui.QMessageBox.NoButton, self)
        msgBox.addButton(u"Ναι", QtGui.QMessageBox.AcceptRole)
        msgBox.addButton(u"&Επιστροφή", QtGui.QMessageBox.RejectRole)
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
            if self.lineEdit_2_3.text()=="": self.random_code()
        else:
            return
     ExportToXML(self, self.metaFilePath)                          #
     QMessageBox.information(self,u"Μεταδεδομένα", u"Το αρχείο μεταδεδομένων αποθηκεύτηκε με επιτυχία στη διαδρομή: "+self.metaFilePath)
  
  def closeEvent(self, event):
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                u"Κλείσιμο διαλόγου μεταδεδομένων", u"Θέλετε σίγουρα να τερματίσετε;",
                QtGui.QMessageBox.NoButton, self)
        msgBox.addButton(u"Ναι", QtGui.QMessageBox.AcceptRole)
        msgBox.addButton(u"&Όχι", QtGui.QMessageBox.RejectRole)
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
            event.accept()
        else:
            event.ignore()

  def completer(self):
     try : temp_tree = ET.parse(unicode(QDir.toNativeSeparators(os.path.join(os.path.abspath(os.path.dirname(__file__)),unicode('organizations.xml')))))
     except :
        QMessageBox.warning(self.iface.mainWindow(),u"organizations.xml",u"Μη έγκυρο αρχείο XML (ή δεν υπάρχει στη διαδρομή του προσθέτου!)")
        return
     temp_root = temp_tree.getroot()
     self.org={}
     for org in temp_root.findall('organization'):
        try: email = org.find('email').text
        except: rank =None
        try: name = org.find('name').text
        except: name=None
        self.org.update({name: email}) 
     
     for key in self.org:
        self.listWidget.addItem(key)
        self.listWidget_2.addItem(key)

     self.listWidget.setVisible(False)
     self.listWidget_2.setVisible(False)


  def complete1(self):
     key= self.sender().selectedItems()[0].text()
     self.lineEdit.setText(key)
     self.lineEdit_2.setText(self.org[key])
  def complete2(self):
     if self.sender()==self.listWidget_2:
        key= self.sender().selectedItems()[0].text()
        
        if self.hascalledlist==self.checkBox_10:
           self.lineEdit_10_1.setText(key)
           self.lineEdit_10_2.setText(self.org[key])
        else:
           lineid= self.hascalledlist.objectName().split("_")[3]
           add_line1="self.lineEdit_10_A_"+lineid
           add_line2="self.lineEdit_10_B_"+lineid
           eval(add_line1+".setText(key)")
           eval(add_line2+".setText(self.org[key])")
        
        self.hascalledlist.setChecked(False)
        self.listWidget_2.setVisible(False)
        self.hascalledlist!=None
        
     else:
        if self.hascalledlist!=None and self.hascalledlist!=self.sender(): 
           self.hascalledlist.setChecked(False)
        self.hascalledlist=self.sender()

  def complete_simorfosi(self):
     key= self.sender().selectedItems()[0].text()
     self.lineEdit_8_1.setText(key)
     self.dateEdit_8_1.setDate(QDate.fromString(self.simorfosi[key], "yyyy-MM-dd"))
     self.comboBox_8_2.setCurrentIndex(1)
     

  def getCoordinates(self):
     crs=int(self.iface.activeLayer().crs().authid().split(":")[1])
     if crs==4326:
        self.lineEdit_5_1.setText(str(self.iface.activeLayer().extent().yMaximum()))
        self.lineEdit_5_2.setText(str(self.iface.activeLayer().extent().xMaximum()))
        self.lineEdit_5_3.setText(str(self.iface.activeLayer().extent().yMinimum()))
        self.lineEdit_5_4.setText(str(self.iface.activeLayer().extent().xMinimum()))
     else:
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question,u"Μετασχηματισμός συντεταγμένων από "+str(self.iface.activeLayer().crs().authid()), u"Θέλετε να συνεχίσετε;"+58*" ",QtGui.QMessageBox.NoButton, self)
        msgBox.addButton(u"Ναι", QtGui.QMessageBox.AcceptRole)
        msgBox.addButton(u"&Όχι", QtGui.QMessageBox.RejectRole)
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
            pass
        else:
            return
        try:
           crsDest = QgsCoordinateReferenceSystem(4326)
           crsSrc = QgsCoordinateReferenceSystem(crs)
           xform = QgsCoordinateTransform(crsSrc, crsDest)
           ptmin = xform.transform(QgsPoint(self.iface.activeLayer().extent().xMinimum(),self.iface.activeLayer().extent().yMinimum()))
           ptmax=xform.transform(QgsPoint(self.iface.activeLayer().extent().xMaximum(), self.iface.activeLayer().extent().yMaximum()))

           if ptmin.x()<ptmax.x():
              west=ptmin.x()
              east=ptmax.x()
           else:
              west=ptmax.x()
              east=ptmin.x()
           if ptmin.y()<ptmax.y():
              south=ptmin.y()
              north=ptmax.y()
           else:
              south=ptmax.y()
              north=ptmin.y()
			   
           self.lineEdit_5_1.setText(str(north))
           self.lineEdit_5_2.setText(str(east))
           self.lineEdit_5_3.setText(str(south))
           self.lineEdit_5_4.setText(str(west))
           QMessageBox.warning(self,u"Προειδοποίηση:",u"Οι συντεταγμένες μετασχηματίστηκαν. Ελέγξτε την εγκυρότητά τους!")
           self.mapCanvas.refresh()
        except:
           QMessageBox.warning(self,u"Σφάλμα:",u"Αδυναμία μετασχηματισμού!")


  def onCoordChanged(self):
          
     try:
        self.mapCanvas.scene().removeItem(self.r)
        self.mapCanvas.scene().removeItem(self.m)
     except:pass
     
     try:
        try:
           xcover=abs(float(self.lineEdit_5_2.text())-float(self.lineEdit_5_4.text()))
           ycover=abs(float(self.lineEdit_5_1.text())-float(self.lineEdit_5_3.text()))
           d=max(xcover,ycover)/5
           rect2=QgsRectangle(float(self.lineEdit_5_2.text())+d, float(self.lineEdit_5_1.text())+d,float(self.lineEdit_5_4.text())-d, float(self.lineEdit_5_3.text())-d)
           self.mapCanvas.setExtent(rect2)
           if self.mapCanvas.scale()<25000:
              self.mapCanvas.zoomScale(25000)
        except: pass
           
        self.r = QgsRubberBand(self.mapCanvas, False)  # True = a polygon
        points = [QgsPoint(float(self.lineEdit_5_2.text()), float(self.lineEdit_5_1.text())), QgsPoint(float(self.lineEdit_5_2.text()), float(self.lineEdit_5_3.text())), QgsPoint(float(self.lineEdit_5_4.text()), float(self.lineEdit_5_3.text())),QgsPoint(float(self.lineEdit_5_4.text()), float(self.lineEdit_5_1.text())),QgsPoint(float(self.lineEdit_5_2.text()), float(self.lineEdit_5_1.text()))]
        
        self.r.setToGeometry(QgsGeometry.fromPolyline(points), None)

        self.r.setColor(QColor(0, 0, 255))
        self.r.setWidth(3)

        self.m = QgsVertexMarker(self.mapCanvas)
        x=(float(self.lineEdit_5_2.text())+float(self.lineEdit_5_4.text()))/2
        y=(float(self.lineEdit_5_1.text())+float(self.lineEdit_5_3.text()))/2
        self.m.setCenter(QgsPoint(x, y))
     except: pass
    
  def zoomIn(self):
        self.mapCanvas.zoomIn()
  def zoomOut(self):
        self.mapCanvas.zoomOut()
  def removetemplayer(self):
     QgsMapLayerRegistry.instance().removeMapLayer(self.templayer.id())
     QgsMapLayerRegistry.instance().removeMapLayer(self.templayer2.id())

  def makeHelp(self):
     try : temp_tree = ET.parse(unicode(QDir.toNativeSeparators(os.path.join(os.path.abspath(os.path.dirname(__file__)),unicode('help.xml')))))
     except :
        QMessageBox.warning(self.iface.mainWindow(),u"help.xml",u"Μη έγκυρο αρχείο XML (ή δεν υπάρχει στη διαδρομή του προσθέτου!)")
        return
     temp_root = temp_tree.getroot()

     for org in temp_root.findall('information'):
        try: name = org.find('name').text
        except: continue
        try: info = org.find('info').text
        except: continue

        message_name="self.info_"+name
        try: details = org.find('details').text
        except: details =None

        if details !=None:

           m = "MyMessageBox(self)"
           exec("%s=%s" % (message_name,m))
           eval(message_name+".setText(u\""+info+"\")")
           eval(message_name+".setDetailedText(u\""+details+"\")")
           
           eval("QtCore.QObject.connect(self."+name+", QtCore.SIGNAL(_fromUtf8(\"clicked()\")),"+message_name+".show)")
        else:
           title=u"Βοήθεια:"
           m="QtGui.QMessageBox(QtGui.QMessageBox.Information,u\""+title+"\", u\""+info+"\",QtGui.QMessageBox.NoButton, self)"
           exec("%s=%s" % (message_name,m))
        
           eval("QtCore.QObject.connect(self."+name+", QtCore.SIGNAL(_fromUtf8(\"clicked()\")),"+message_name+".show)")
           #QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")),self.msgBox.show)
        
  def Empty_cell(self):
     empty=False
     if self.lineEdit.text()=="":empty=True
     if self.lineEdit_2.text()=="":empty=True
     if self.lineEdit_2_1.text()=="":empty=True
     if self.lineEdit_2_3.text()=="":empty=True
     if self.textEdit.toPlainText()=="":empty=True
     if self.lineEdit_2_6.text()=="":empty=True
     if self.comboBox_3_1.currentText()=="":empty=True
     if self.comboBox_4_1.currentText()=="":empty=True
     if self.lineEdit_5_1.text()=="":empty=True
     if self.lineEdit_5_2.text()=="":empty=True
     if self.lineEdit_5_3.text()=="":empty=True
     if self.lineEdit_5_4.text()=="":empty=True
     if self.comboBox_9_1.currentText()=="":empty=True
     if self.comboBox_9_2.currentText()=="":empty=True
     if self.lineEdit_10_1.text()=="":empty=True
     if self.lineEdit_10_1.text()=="":empty=True
     if not (self.groupBox_6_5.isChecked() or self.groupBox_6_2.isChecked() or self.groupBox_6_3.isChecked() or self.groupBox_6_4.isChecked()):empty=True
     return empty

  def getCoordinates2(self):
     self.rect=RectangleMapTool(self.mapCanvas,self.lineEdit_5_1,self.lineEdit_5_2,self.lineEdit_5_3,self.lineEdit_5_4)
     self.mapCanvas.setMapTool(self.rect)

   
class MyMessageBox(QtGui.QMessageBox):
    def __init__(self,self2):
        QtGui.QMessageBox.__init__(self,QtGui.QMessageBox.Information,u"Βοήθεια:", u"info",QtGui.QMessageBox.NoButton | QtGui.QMessageBox.Ok,self2)
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QtGui.QMessageBox.event(self, e)

        self.setMinimumHeight(100)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(400)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        textEdit = self.findChild(QtGui.QTextEdit)
        if textEdit != None :
            textEdit.setMinimumHeight(400)
            textEdit.setMaximumHeight(16777215)
            textEdit.setMinimumWidth(400)
            textEdit.setMaximumWidth(16777215)
            textEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        return result

class RectangleMapTool(QgsMapToolEmitPoint):
  def __init__(self, canvas,lineEdit_5_1,lineEdit_5_2,lineEdit_5_3,lineEdit_5_4):
      self.lineEdit_5_1=lineEdit_5_1
      self.lineEdit_5_2=lineEdit_5_2
      self.lineEdit_5_3=lineEdit_5_3
      self.lineEdit_5_4=lineEdit_5_4
      self.canvas = canvas
      QgsMapToolEmitPoint.__init__(self, self.canvas)
      self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
      self.rubberBand.setColor(Qt.red)
      self.rubberBand.setWidth(2)
      self.rubberBand.setFillColor(QtGui.QColor(0,0,0,0))
      self.rubberBand.setLineStyle(Qt.DotLine)

      self.toolPan = QgsMapToolPan(self.canvas)

      self.reset()
      
  def reset(self):
      self.startPoint = self.endPoint = None
      self.isEmittingPoint = False
      self.rubberBand.reset(QGis.Polygon)

  def canvasPressEvent(self, e):
      self.startPoint = self.toMapCoordinates(e.pos())
      self.endPoint = self.startPoint
      self.isEmittingPoint = True
      self.showRect(self.startPoint, self.endPoint)

  def canvasReleaseEvent(self, e):
      self.isEmittingPoint = False
      r = self.rectangle()
      if r is not None:

        self.lineEdit_5_1.setText(str(r.yMaximum()))
        self.lineEdit_5_2.setText(str(r.xMaximum()))
        self.lineEdit_5_3.setText(str(r.yMinimum()))
        self.lineEdit_5_4.setText(str(r.xMinimum()))
        self.reset()
        self.canvas.setMapTool(self.toolPan)

  def canvasMoveEvent(self, e):
      if not self.isEmittingPoint:
        return

      self.endPoint = self.toMapCoordinates(e.pos())
      self.showRect(self.startPoint, self.endPoint)

  def showRect(self, startPoint, endPoint):
      self.rubberBand.reset(QGis.Polygon)
      if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
        return

      point1 = QgsPoint(startPoint.x(), startPoint.y())
      point2 = QgsPoint(startPoint.x(), endPoint.y())
      point3 = QgsPoint(endPoint.x(), endPoint.y())
      point4 = QgsPoint(endPoint.x(), startPoint.y())

      self.rubberBand.addPoint(point1, False)
      self.rubberBand.addPoint(point2, False)
      self.rubberBand.addPoint(point3, False)
      self.rubberBand.addPoint(point4, True)    # true to update canvas
      self.rubberBand.show()

  def rectangle(self):
      if self.startPoint is None or self.endPoint is None:
        return None
      elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
        return None

      return QgsRectangle(self.startPoint, self.endPoint)

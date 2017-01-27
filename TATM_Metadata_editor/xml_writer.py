# -*- coding:utf-8 -*-
import ConfigParser
import os.path
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.core import *
from qgis.gui import *
import urllib
import datetime

#==============================
# FONCTION TO WRITE XML EXPORT       
#==============================

def ExportToXML(self, zFile):
    zLOG = file(zFile, "w")
    if not zLOG : return
    
    MakeEnteteXML(self, zLOG)
    MakeFileIdentifierXML(self, zLOG, zFile)
    MakeFileLanguageXML(self, zLOG)
    MakeCharacterSetCodeXML(self, zLOG)
    MakeHierarchyLevelXML(self, zLOG)
    MakeContactXML(self, zLOG)
    MakeDateStampXML(self, zLOG, 1, True, None)
    MakeMetadataStandardNameXML(self, zLOG)
    MakeMetadataStandardVersionXML(self, zLOG)

    MakeIdentificationInfoXML(self, zLOG)
    MakeDistributionInfoXML(self, zLOG)
    MakeDataQualityInfoXML(self, zLOG)
    MakeEndXML(self, zLOG)

    CloseLOG(zLOG)

#------------------------------------
# FONCTION TO WRITE BLOCX XML EXPORT       
#------------------------------------
    
def MakeEnteteXML(self, zLOG):
    zPath = os.path.dirname(__file__).replace("\\","/")
    zXSL = ""
    
    WriteInLOG(zLOG, '<?xml version="1.0" encoding="UTF-8"?>' \
                     '%s' \
                     '<gmd:MD_Metadata xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd"' \
                     ' xmlns:gmd="http://www.isotc211.org/2005/gmd"' \
                     ' xmlns:gco="http://www.isotc211.org/2005/gco"' \
                     ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
                     ' xmlns:gml="http://www.opengis.net/gml"' \
                     ' xmlns:xlink="http://www.w3.org/1999/xlink">\n' % (zXSL))

def MakeFileIdentifierXML(self, zLOG, zFile):
    zObj = self.lineEdit_2_3
    if zObj.text()!="":
       WriteInLOG(zLOG, '\t<gmd:fileIdentifier>\n')
       WriteInLOG(zLOG, '\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.text())) 
       WriteInLOG(zLOG, '\t</gmd:fileIdentifier>\n')

def MakeFileLanguageXML(self, zLOG):
    zObj = self.comboBox
    zValue = zObj.currentText()
    if zValue in self.languages.keys(): zValue=self.languages[zValue]
    MakeBlocLangue(self, zLOG, zValue, 1)

def MakeCharacterSetCodeXML(self, zLOG):
    zValue = "MD_CharacterSetCode_utf8" 
    WriteInLOG(zLOG, '\t<gmd:characterSet>\n')
    WriteInLOG(zLOG, '\t\t<gmd:MD_CharacterSetCode codeSpace="ISOTC211/19115" codeListValue="%s" codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode">%s</gmd:MD_CharacterSetCode>\n' % (zValue, zValue))
    WriteInLOG(zLOG, '\t</gmd:characterSet>\n')

def MakeHierarchyLevelXML(self, zLOG):
    zValue ="dataset" 
    WriteInLOG(zLOG, '\t<gmd:hierarchyLevel>\n')
    WriteInLOG(zLOG, '\t\t<gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode" codeListValue="%s">%s</gmd:MD_ScopeCode>\n' % (zValue, zValue))
    WriteInLOG(zLOG, '\t</gmd:hierarchyLevel>\n')

def MakeContactXML(self, zLOG):
    zObj = [self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text(),self.lineEdit_4.text()]
    zValue = "pointOfContact"
    MakeBlocRole(self, zLOG, zObj, zValue, 1, True, 1)

def MakeDateStampXML(self, zLOG, zTab, isValue, zObj):
    sTab=""
    for k in range(zTab): sTab+="\t"
    WriteInLOG(zLOG, '%s<gmd:dateStamp>\n' % (sTab))
    if isValue :
        temp_var = self.dateEdit.date()
        zValue=temp_var.toPyDate()

        WriteInLOG(zLOG, '%s\t<gco:Date>%s</gco:Date>\n' % (sTab, zValue))
    else :
        if zObj != None : WriteInLOG(zLOG, '%s\t<gco:Date>%s</gco:Date>\n' % (sTab, ReturnDate(self, zObj)))
        else : WriteInLOG(zLOG, '%s\t<gco:Date>%s</gco:Date>\n' % (sTab, datetime.datetime.now().strftime("%d/%m/%Y %Hh%Mm%Ss")))
        
    WriteInLOG(zLOG, '%s</gmd:dateStamp>\n' % (sTab))

def MakeMetadataStandardNameXML(self, zLOG):
    WriteInLOG(zLOG, '\t<gmd:metadataStandardName>\n')
    WriteInLOG(zLOG, '\t\t<gco:CharacterString>ISO19115</gco:CharacterString>\n')
    WriteInLOG(zLOG, '\t</gmd:metadataStandardName>\n')

def MakeMetadataStandardVersionXML(self, zLOG):
    WriteInLOG(zLOG, '\t<gmd:metadataStandardVersion>\n')
    WriteInLOG(zLOG, '\t\t<gco:CharacterString>2003/Cor.1:2006</gco:CharacterString>\n')
    WriteInLOG(zLOG, '\t</gmd:metadataStandardVersion>\n')

def MakeReferenceSystemInfoXML(self, zLOG):
    zObj = getWidget(self, "tablescr")
    for i in range(zObj.rowCount()): 
        zEPSG = zObj.cellWidget(i, 0).text()
        if zObj.rowCount() == 1 :  WriteInLOG(zLOG, '\t<gmd:referenceSystemInfo>\n')
        else : WriteInLOG(zLOG, '\t<gmd:referenceSystemInfo id="proj00%s">\n' % (i+1))
        WriteInLOG(zLOG, '\t\t<gmd:MD_ReferenceSystem>\n')
        WriteInLOG(zLOG, '\t\t\t<gmd:referenceSystemIdentifier>\n')        
        WriteInLOG(zLOG, '\t\t\t\t<gmd:RS_Identifier>\n')
        zCodeESPG = int(zEPSG.replace("EPSG:",""))
        WriteInLOG(zLOG, '\t\t\t\t\t<gmd:code>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zCodeESPG))
        WriteInLOG(zLOG, '\t\t\t\t\t</gmd:code>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t<gmd:codeSpace>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>urn:ogc:def:crs:EPSG:6.11</gco:CharacterString>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t</gmd:codeSpace>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t<gmd:version>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>6.11</gco:CharacterString>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t</gmd:version>\n')
        WriteInLOG(zLOG, '\t\t\t\t</gmd:RS_Identifier>\n')
        WriteInLOG(zLOG, '\t\t\t</gmd:referenceSystemIdentifier>\n')
        WriteInLOG(zLOG, '\t\t</gmd:MD_ReferenceSystem>\n')    
        WriteInLOG(zLOG, '\t</gmd:referenceSystemInfo>\n')

def MakeIdentificationInfoXML(self, zLOG):     
    WriteInLOG(zLOG, '\t<gmd:identificationInfo>\n')
    WriteInLOG(zLOG, '\t\t<gmd:MD_DataIdentification>\n')
    #CITATION BLOC
    WriteInLOG(zLOG, '\t\t\t<gmd:citation>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:CI_Citation>\n')
    zValue=self.lineEdit_2_1.text()
    if zValue !="":
       WriteInLOG(zLOG, '\t\t\t\t\t<gmd:title>\n')
       WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue))
       WriteInLOG(zLOG, '\t\t\t\t\t</gmd:title>\n')
    
    if self.groupBox_6_2.isChecked():
        zTypeDate = "creation"
        temp_var = self.dateEdit_6_1.date()
        zValue=temp_var.toPyDate()
        MakeBlocDate(self, zLOG, zValue, zTypeDate, 5)

    if self.groupBox_6_3.isChecked():
        zTypeDate = "publication"
        temp_var = self.dateEdit_6_2.date()
        zValue=temp_var.toPyDate()
        MakeBlocDate(self, zLOG, zValue, zTypeDate, 5)

    if self.groupBox_6_4.isChecked():
        zTypeDate = "revision"
        temp_var = self.dateEdit_6_3.date()
        zValue=temp_var.toPyDate()
        MakeBlocDate(self, zLOG, zValue, zTypeDate, 5)
    #
    zObj = self.lineEdit_2_3
    
    WriteInLOG(zLOG, '\t\t\t\t\t<gmd:identifier>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:RS_Identifier>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:code>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.text()))
    WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:code>\n')
    if self.lineEdit_2_2.text()!="":
       WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:codeSpace>\n')
       WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (self.lineEdit_2_2.text()))
       WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:codeSpace>\n')
    
    WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:RS_Identifier>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t</gmd:identifier>\n')

    WriteInLOG(zLOG, '\t\t\t\t</gmd:CI_Citation>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:citation>\n')
    #End CITATION BLOC

    #ABSTRACT BLOC
    zValue=self.textEdit.toPlainText()
    if zValue!="":
       WriteInLOG(zLOG, '\t\t\t<gmd:abstract>\n')
       WriteInLOG(zLOG, '\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue))
       WriteInLOG(zLOG, '\t\t\t</gmd:abstract>\n')
    #End ABSTRACT BLOC

    #ROLES BLOC
    zObj = [self.lineEdit_10_1.text(),self.lineEdit_10_2.text(),self.lineEdit_10_3.text(),self.lineEdit_10_4.text()]
    zValue=self.roles[self.comboBox_10_1.currentText()]
    if zObj[0]!="":
       MakeBlocRole(self, zLOG, zObj, zValue, 1, False, 3)

    for i in range(1,self.gridLayout_76.count()-3):
        combo="self.comboBox_10_A_"+str(i)+".currentText()"
        zValue=self.roles[eval(combo)]
        line1="self.lineEdit_10_A_"+str(i)+".text()"
        line2="self.lineEdit_10_B_"+str(i)+".text()"
        line3="self.lineEdit_10_url_"+str(i)+".text()"
        line4="self.lineEdit_10_phone_"+str(i)+".text()"
        zObj = [eval(line1),eval(line2),eval(line3),eval(line4)]
        if zObj[0]!="":
           MakeBlocRole(self, zLOG, zObj, zValue, i+1, False, 3) 
    #End ROLES BLOC

    #BLOC INSPIRE required keywords
    WriteInLOG(zLOG, '\t\t\t<gmd:descriptiveKeywords>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_Keywords>\n')

    for i in range(self.gridLayout_48.count()):
        if i==0:
           zObj=[self.comboBox_4_1.currentText(),"GEMET - INSPIRE themes, version 1.0"]
        else:
           zObj=[eval("self.comboBox_4_A_"+str(i)+".currentText()"),"GEMET - INSPIRE themes, version 1.0"]

        if zObj[0]!=0:
           WriteInLOG(zLOG, '\t\t\t\t\t<gmd:keyword>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj[0]))
           WriteInLOG(zLOG, '\t\t\t\t\t</gmd:keyword>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t<gmd:thesaurusName>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:CI_Citation>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:title>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj[1]))
    WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:title>\n')

    MakeBlocDate(self, zLOG, "2008-06-01", "publication", 7)
    WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:CI_Citation>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t</gmd:thesaurusName>\n')
    WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_Keywords>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:descriptiveKeywords>\n')
    #End BLOC INSPIRE required keywords   

    #BLOC INSPIRE optional keywords 
    for i in range(self.gridLayout_49.count()):
        zObj = eval("self.lineEdit_4_A_"+str(i)+".text()")
        if zObj!="":
           WriteInLOG(zLOG, '\t\t\t<gmd:descriptiveKeywords>\n')
           WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_Keywords>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t<gmd:keyword>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj))
           WriteInLOG(zLOG, '\t\t\t\t\t</gmd:keyword>\n')


    
           WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_Keywords>\n')
           WriteInLOG(zLOG, '\t\t\t</gmd:descriptiveKeywords>\n')
    #End BLOC INSPIRE optional keywords

    #BLOC resourceConstraints
    WriteInLOG(zLOG, '\t\t\t<gmd:resourceConstraints>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_Constraints>\n')
    for i in range(self.gridLayout_72.count()-1):
        if i==0:
           zObj=self.comboBox_9_1.currentText()
        else:
           zObj=eval("self.comboBox_9_A_"+str(i)+".currentText()")
        if zObj!="":
           WriteInLOG(zLOG, '\t\t\t\t\t<gmd:useLimitation>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj))
           WriteInLOG(zLOG, '\t\t\t\t\t</gmd:useLimitation>\n')
    WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_Constraints>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:resourceConstraints>\n')

    WriteInLOG(zLOG, '\t\t\t<gmd:resourceConstraints>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_LegalConstraints>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t<gmd:accessConstraints>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions">otherRestrictions</gmd:MD_RestrictionCode>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t</gmd:accessConstraints>\n')
    for i in range(self.gridLayout_73.count()-1):
        if i==0:
           zObj=self.comboBox_9_2.currentText()
        else:
           zObj=eval("self.comboBox_9_B_"+str(i)+".currentText()")
        if zObj!="":
           WriteInLOG(zLOG, '\t\t\t\t\t<gmd:otherConstraints>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj))
           WriteInLOG(zLOG, '\t\t\t\t\t</gmd:otherConstraints>\n')

    WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_LegalConstraints>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:resourceConstraints>\n')
    #End BLOC resourceConstraints

    #BLOC Spatial Resolution

    for i in range(1):

        if self.radioButton_7_1.isChecked() :
            zWidget = self.spinBox_7_1
            WriteInLOG(zLOG, '\t\t\t<gmd:spatialResolution>\n')
            WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_Resolution>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t<gmd:equivalentScale>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:MD_RepresentativeFraction>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:denominator>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:Integer>%s</gco:Integer>\n' % (int(zWidget.value())))
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:denominator>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:MD_RepresentativeFraction>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t</gmd:equivalentScale>\n')
            WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_Resolution>\n')
            WriteInLOG(zLOG, '\t\t\t</gmd:spatialResolution>\n')
        else:
            zWidget = self.doubleSpinBox_7_1
            zValueMesureUnit = "%s" % (self.comboBox_7_1.currentText())
            WriteInLOG(zLOG, '\t\t\t<gmd:spatialResolution>\n')
            WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_Resolution>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t<gmd:distance>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:Distance uom="%s">%s</gco:Distance>\n' % (zValueMesureUnit, zWidget.value()))
            WriteInLOG(zLOG, '\t\t\t\t\t</gmd:distance>\n')
            WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_Resolution>\n')
            WriteInLOG(zLOG, '\t\t\t</gmd:spatialResolution>\n')
    #End BLOC Spatial Resolution

    #BLOC Language for the resource
    zObj = self.comboBox_2

    for i in range(1):
        zValue = zObj.currentText()
        if zValue in self.languages.keys(): zValue=self.languages[zValue]
        MakeBlocLangue(self, zLOG, zValue, 3) 
    #End BLOC Language for the resource

    #BLOC INSPIRE category(/ISO)
    
    for i in range(self.gridLayout_44.count()-4):
        text=None
        if i==0:
           zObj=self.comboBox_3_1.currentText()
           if zObj!="":
              text=self.categories[zObj]
        else:
           zObj=eval("self.comboBox_3_A_"+str(i)+".currentText()")
           if zObj!="":
              text=self.categories[zObj]
        if text!=None:
           WriteInLOG(zLOG, '\t\t\t<gmd:topicCategory>\n')
           WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_TopicCategoryCode>%s</gmd:MD_TopicCategoryCode>\n' % (text))
           WriteInLOG(zLOG, '\t\t\t</gmd:topicCategory>\n')
    #End BLOC INSPIRE category(/ISO)

    #BLOC Extents
    WriteInLOG(zLOG, '\t\t\t<gmd:extent>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:EX_Extent>\n')

    for i in range(1):
        if (self.lineEdit_5_4.text() !="" and self.lineEdit_5_2.text() !="" and self.lineEdit_5_3.text() !="" and self.lineEdit_5_1.text() !=""):
           WriteInLOG(zLOG, '\t\t\t\t\t<gmd:geographicElement>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:EX_GeographicBoundingBox>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:westBoundLongitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (self.lineEdit_5_4.text()))
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:westBoundLongitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:eastBoundLongitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (self.lineEdit_5_2.text()))
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:eastBoundLongitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:southBoundLatitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (self.lineEdit_5_3.text()))
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:southBoundLatitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:northBoundLatitude>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (self.lineEdit_5_1.text()))
           WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:northBoundLatitude>\n')    
           WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:EX_GeographicBoundingBox>\n')
           WriteInLOG(zLOG, '\t\t\t\t\t</gmd:geographicElement>\n')
       
    if self.groupBox_6_5.isChecked():
        for i in range(1):

            WriteInLOG(zLOG, '\t\t\t\t\t<gmd:temporalElement>\n')
 
            WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:EX_TemporalExtent>\n')

            WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:extent>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gml:TimePeriod gml:id="IDcd3b1c4f-b5f7-439a-afc4-3317a4cd89be" xsi:type="gml:TimePeriodType">\n')
            temp_var = self.dateEdit_6_4.date()
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t\t<gml:beginPosition>%s</gml:beginPosition>\n' % (temp_var.toPyDate()))
            if self.radioButton.isChecked():
                WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t\t<gml:endPosition indeterminatePosition="now"/>\n')
            else:
                temp_var = self.dateEdit_6.date()
                WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t\t<gml:endPosition>%s</gml:endPosition>\n'  % (temp_var.toPyDate()))
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t</gml:TimePeriod>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:extent>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:EX_TemporalExtent>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t</gmd:temporalElement>\n')
    WriteInLOG(zLOG, '\t\t\t\t</gmd:EX_Extent>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:extent>\n')
    #End BLOC Extents
    
    WriteInLOG(zLOG, '\t\t</gmd:MD_DataIdentification>\n')
    WriteInLOG(zLOG, '\t</gmd:identificationInfo>\n')


def spacer(space):
    spacer=""
    for i in range(space):spacer+="\t"
    return spacer

def MakeDistributionInfoXML(self, zLOG):
    WriteInLOG(zLOG, '\t<gmd:distributionInfo>\n')
    WriteInLOG(zLOG, '\t\t<gmd:MD_Distribution>\n')

    for i in range(1): MakeBlocFormat(self, zLOG, "zObj", i, 3)

   
    WriteInLOG(zLOG, '\t\t\t<gmd:transferOptions>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_DigitalTransferOptions>\n')

    for i in range(self.gridLayout_30.count()-3):
        if i==0:
           zObj=self.lineEdit_2_6.text()
        else:
           zObj=eval("self.lineEdit_2_A_"+str(i)+".text()")

        WriteInLOG(zLOG, '\t\t\t\t\t<gmd:onLine>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:CI_OnlineResource>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:linkage>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gmd:URL>%s</gmd:URL>\n' % (zObj))
        WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:linkage>\n')

        WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:CI_OnlineResource>\n')
        WriteInLOG(zLOG, '\t\t\t\t\t</gmd:onLine>\n')
    WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_DigitalTransferOptions>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:transferOptions>\n')
    
    WriteInLOG(zLOG, '\t\t</gmd:MD_Distribution>\n')
    WriteInLOG(zLOG, '\t</gmd:distributionInfo>\n')

def MakeDataQualityInfoXML(self, zLOG):

    WriteInLOG(zLOG, '\t<gmd:dataQualityInfo>\n')
    WriteInLOG(zLOG, '\t\t<gmd:DQ_DataQuality>\n')
    WriteInLOG(zLOG, '\t\t\t<gmd:scope>\n')
    WriteInLOG(zLOG, '\t\t\t\t<gmd:DQ_Scope>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t<gmd:level>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:MD_ScopeCode codeListValue="%s" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode">%s</gmd:MD_ScopeCode>\n' % ("dataset", "dataset"))
    WriteInLOG(zLOG, '\t\t\t\t\t</gmd:level>\n')
    WriteInLOG(zLOG, '\t\t\t\t</gmd:DQ_Scope>\n')
    WriteInLOG(zLOG, '\t\t\t</gmd:scope>\n')

    WriteInLOG(zLOG, '\t\t\t<gmd:report>\n')

    WriteInLOG(zLOG, '\t\t\t\t<gmd:DQ_DomainConsistency xsi:type="gmd:DQ_DomainConsistency_Type">\n')
    WriteInLOG(zLOG, '\t\t\t\t\t<gmd:result>\n')
    WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:DQ_ConformanceResult xsi:type="gmd:DQ_ConformanceResult_Type">\n')

    if self.groupBox_8_2.isChecked() :
         zValueSPEC = self.lineEdit_8_1.text()
         temp_var = self.dateEdit_8_1.date()
         zValueDate = temp_var.toPyDate()
         zValueTypeDate=self.datetype[self.comboBox_8_2.currentText()]
         zIndesDegre=self.comboBox_8_3.currentText()

         WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:specification>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gmd:CI_Citation>\n')
         
         if zValueSPEC!="":
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t\t<gmd:title>\n')
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValueSPEC))
            WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t\t</gmd:title>\n')

         MakeBlocDate(self, zLOG, zValueDate, zValueTypeDate, 9)

         WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t</gmd:CI_Citation>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:specification>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:explanation>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:CharacterString>See the referenced specification</gco:CharacterString>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:explanation>\n')

         if zIndesDegre == u"Σύμμορφος" : zValue = "true"
         elif zIndesDegre == u"Δεν είναι σύμμορφος": zValue = "false"
         else : zValue = ""
         if zValue != "" :
                WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:pass>\n')
                WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:Boolean>%s</gco:Boolean>\n' % (zValue))
                WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:pass>\n')
         else: WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:pass gco:nilReason="template"/>\n')   
            
         WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:DQ_ConformanceResult>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t</gmd:result>\n')
         WriteInLOG(zLOG, '\t\t\t\t</gmd:DQ_DomainConsistency>\n')
         WriteInLOG(zLOG, '\t\t\t</gmd:report>\n')
    else:
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:explanation>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t\t<gco:CharacterString>See the referenced specification</gco:CharacterString>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t</gmd:explanation>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t\t<gmd:pass gco:nilReason="template"/>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t\t</gmd:DQ_ConformanceResult>\n')
         WriteInLOG(zLOG, '\t\t\t\t\t</gmd:result>\n')
         WriteInLOG(zLOG, '\t\t\t\t</gmd:DQ_DomainConsistency>\n')
         WriteInLOG(zLOG, '\t\t\t</gmd:report>\n')


    zValue = self.textEdit_7_1.toPlainText()
    if zValue!="":
       WriteInLOG(zLOG, '\t\t\t<gmd:lineage>\n')
       WriteInLOG(zLOG, '\t\t\t\t<gmd:LI_Lineage>\n')
       WriteInLOG(zLOG, '\t\t\t\t\t<gmd:statement>\n')
       WriteInLOG(zLOG, '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue))
       WriteInLOG(zLOG, '\t\t\t\t\t</gmd:statement>\n')
       WriteInLOG(zLOG, '\t\t\t\t</gmd:LI_Lineage>\n')
       WriteInLOG(zLOG, '\t\t\t</gmd:lineage>\n')  

    WriteInLOG(zLOG, '\t\t</gmd:DQ_DataQuality>\n')
    WriteInLOG(zLOG, '\t</gmd:dataQualityInfo>\n')
#
def MakeSpatialRepresentation(self, zLOG):
    zObj = getWidget(self, "coherence")
    if zObj.toPlainText() != "" :
        import ast
        try : mydict = ast.literal_eval("%s" % (zObj.toPlainText()))
        except : mydict = None

        if mydict != None and type(mydict)==dict:

            zcondTopologyLevelCode = True if mydict.has_key('TopologyLevelCode') and mydict['TopologyLevelCode']!= 'unknow' else False
            zcondGeometricObjectTypeCode = True if mydict.has_key('GeometricObjectTypeCode') and mydict['GeometricObjectTypeCode']!= 'unknow' else False

            if zcondTopologyLevelCode or zcondGeometricObjectTypeCode :
                    WriteInLOG(zLOG, '\t<gmd:spatialRepresentationInfo>\n')
                    WriteInLOG(zLOG, '\t\t<gmd:MD_VectorSpatialRepresentation>\n')
                    if zcondTopologyLevelCode :
                        WriteInLOG(zLOG, '\t\t\t<gmd:topologyLevel>\n')
                        WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_TopologyLevelCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_TopologyLevelCode" codeListValue="%s">%s</gmd:MD_TopologyLevelCode>\n' % (mydict['TopologyLevelCode'], mydict['TopologyLevelCode']))
                        WriteInLOG(zLOG, '\t\t\t</gmd:topologyLevel>\n')
                    if zcondGeometricObjectTypeCode :    
                        WriteInLOG(zLOG, '\t\t\t<gmd:geometricObjects>\n')
                        WriteInLOG(zLOG, '\t\t\t\t<gmd:MD_GeometricObjects>\n')
                        WriteInLOG(zLOG, '\t\t\t\t\t<gmd:geometricObjectType>\n')
                        WriteInLOG(zLOG, '\t\t\t\t\t\t<gmd:MD_GeometricObjectTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_GeometricObjectTypeCode" codeListValue="%s">%s</gmd:MD_GeometricObjectTypeCode>\n' % (mydict['GeometricObjectTypeCode'],mydict['GeometricObjectTypeCode']))
                        WriteInLOG(zLOG, '\t\t\t\t\t</gmd:geometricObjectType>\n')
                        WriteInLOG(zLOG, '\t\t\t\t</gmd:MD_GeometricObjects>\n')
                        WriteInLOG(zLOG, '\t\t\t</gmd:geometricObjects>\n')
                    WriteInLOG(zLOG, '\t\t</gmd:MD_VectorSpatialRepresentation>\n')
                    WriteInLOG(zLOG, '\t</gmd:spatialRepresentationInfo>\n')

def MakeEndXML(self, zLOG):
    WriteInLOG(zLOG, '</gmd:MD_Metadata>')
    
#-----------------------------
# PRIMARY BLOC FOR XML EXPORT       
#----------------------------- 
def MakeBlocFormat(self, zLOG, zObj, i, zTab):
        sTab=""
        WriteInLOG(zLOG, '%s<gmd:distributionFormat>\n' % (sTab))
        WriteInLOG(zLOG, '\t%s<gmd:MD_Format>\n' % (sTab))
        WriteInLOG(zLOG, '\t\t%s<gmd:name>\n' % (sTab))
        WriteInLOG(zLOG, '\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab,"unknown"))
        WriteInLOG(zLOG, '\t\t%s</gmd:name>\n' % (sTab))
        WriteInLOG(zLOG, '\t\t%s<gmd:version>\n' % (sTab))
        WriteInLOG(zLOG, '\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab,"unknown"))
        WriteInLOG(zLOG, '\t\t%s</gmd:version>\n' % (sTab))
        WriteInLOG(zLOG, '\t%s</gmd:MD_Format>\n' % (sTab))
        WriteInLOG(zLOG, '%s</gmd:distributionFormat>\n' % (sTab))
   
def MakeBlocLangue(self, zLOG, zValue, zTab):
    sTab=""
    for k in range(zTab): sTab+="\t"
    WriteInLOG(zLOG, '%s<gmd:language>\n' % (sTab))
    WriteInLOG(zLOG, '%s<gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="%s">%s</gmd:LanguageCode>\n' % ("%s%s" % (sTab, "\t"),zValue, zValue))
    WriteInLOG(zLOG, '%s</gmd:language>\n' % (sTab))

def MakeBlocDate(self, zLOG, zValue, zType, zTab):
    sTab=""
    for k in range(zTab): sTab+="\t"
    WriteInLOG(zLOG, '%s<gmd:date>\n' % (sTab))
    WriteInLOG(zLOG, '\t%s<gmd:CI_Date>\n' % (sTab))
    WriteInLOG(zLOG, '\t\t%s<gmd:date>\n' % (sTab))
    WriteInLOG(zLOG, '\t\t\t%s<gco:Date>%s</gco:Date>\n' % (sTab, zValue))
    WriteInLOG(zLOG, '\t\t%s</gmd:date>\n' % (sTab))
    WriteInLOG(zLOG, '\t\t%s<gmd:dateType>\n' % (sTab))
    WriteInLOG(zLOG, '\t\t\t%s<gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="%s">%s</gmd:CI_DateTypeCode>\n' % (sTab, zType, zType))
    WriteInLOG(zLOG, '\t\t%s</gmd:dateType>\n' % (sTab))
    WriteInLOG(zLOG, '\t%s</gmd:CI_Date>\n' % (sTab))
    WriteInLOG(zLOG, '%s</gmd:date>\n' % (sTab))

def MakeBlocRole(self, zLOG, zObj, zValue, i, isPointOfContact, zTab):
    sTab, k = "", 0
    for k in range(zTab): sTab+="\t"    
    WriteInLOG(zLOG, '%s<gmd:contact>\n' % (sTab)) if isPointOfContact else WriteInLOG(zLOG, '%s<gmd:pointOfContact>\n' % (sTab))
    MakeResponsibleParty(self, zLOG, zObj, zValue, i, isPointOfContact, (k+1))
    WriteInLOG(zLOG, '%s</gmd:contact>\n' % (sTab)) if isPointOfContact else WriteInLOG(zLOG, '%s</gmd:pointOfContact>\n' % (sTab))

def MakeResponsibleParty(self, zLOG, zObj, zValue, i, isPointOfContact, zTab):
    sTab=""
    for k in range(zTab): sTab+="\t"     
    WriteInLOG(zLOG, '%s<gmd:CI_ResponsibleParty>\n' % (sTab))
    if zObj[0]!="": 
       WriteInLOG(zLOG, '\t%s<gmd:organisationName>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj[0]))
       WriteInLOG(zLOG, '\t%s</gmd:organisationName>\n' % (sTab))

#'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'
#'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'
#'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'

    if zObj[1]!="":
       WriteInLOG(zLOG, '\t%s<gmd:contactInfo>\n' % (sTab))
       WriteInLOG(zLOG, '\t%s<gmd:CI_Contact>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t%s<gmd:address>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t\t%s<gmd:CI_Address>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t\t\t%s<gmd:electronicMailAddress>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj[1] ))
       WriteInLOG(zLOG, '\t\t\t\t%s</gmd:electronicMailAddress>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t\t%s</gmd:CI_Address>\n' % (sTab))
       WriteInLOG(zLOG, '\t\t%s</gmd:address>\n' % (sTab))
       if zObj[2]!="":
          WriteInLOG(zLOG, '\t\t%s<gmd:onlineResource>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t%s<gmd:CI_OnlineResource>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t\t%s<gmd:linkage>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t\t\t%s<gmd:URL>%s</gmd:URL>\n' % (sTab, zObj[2] ))
          WriteInLOG(zLOG, '\t\t\t\t%s</gmd:linkage>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t%s</gmd:CI_OnlineResource>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t%s</gmd:onlineResource>\n' % (sTab))
       if zObj[3]!="":
          WriteInLOG(zLOG, '\t\t%s<gmd:phone>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t%s<gmd:CI_Telephone>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t\t%s<gmd:voice>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj[3] ))
          WriteInLOG(zLOG, '\t\t\t\t%s</gmd:voice>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t\t%s</gmd:CI_Telephone>\n' % (sTab))
          WriteInLOG(zLOG, '\t\t%s</gmd:phone>\n' % (sTab))
       WriteInLOG(zLOG, '\t%s</gmd:CI_Contact>\n' % (sTab))
       WriteInLOG(zLOG, '\t%s</gmd:contactInfo>\n' % (sTab))
    
    WriteInLOG(zLOG, '\t%s<gmd:role>\n' % (sTab))
    WriteInLOG(zLOG, '\t\t%s<gmd:CI_RoleCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode" codeListValue="%s">%s</gmd:CI_RoleCode>\n' % (sTab, zValue, zValue))
    WriteInLOG(zLOG, '\t%s</gmd:role>\n' % (sTab))
    WriteInLOG(zLOG, '%s</gmd:CI_ResponsibleParty>\n' % (sTab))

#-------------------------------
# FONCTIONs TO WRITE XML EXPORT       
#-------------------------------
def WriteInLOG(zLOG, zMsg):
    if zLOG != None : zLOG.write(zMsg.encode("utf-8"))

def CloseLOG(zLOG):     
    if zLOG != None : zLOG.close()


from xml.etree import ElementTree as ET
import urllib,os,sys

class xmlISOparser:
	def __init__(self, filenameIP, dataXML, isoFormat, langue):				
		self.inputXMLfile = filenameIP
		self.dataXML = dataXML
		self.isoFormatToExtract = isoFormat
		self.langueTR = langue

        def getTagDictionnary(self):
                if self.dataXML == None and self.inputXMLfile == None : return False
                else : self.root = self.getIsoXML(self.inputXMLfile, self.dataXML)
		if self.root is None : return False
		
		self.importISOxmlDefinition(self.isoFormatToExtract)
                self.dictionnary = self.getElementVal(self.isoModel.dictionnary())
                
                return (self.dictionnary==[[]])
                

		
	def createISOdataStructure(self, isMetaData):
		if isMetaData :


                        try:
                           self.orgfirstmail={}
                           for org in self.root.findall('{http://www.isotc211.org/2005/gmd}identificationInfo/{http://www.isotc211.org/2005/gmd}MD_DataIdentification/{http://www.isotc211.org/2005/gmd}pointOfContact/{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty'):
                              name=org.find('{http://www.isotc211.org/2005/gmd}organisationName/{http://www.isotc211.org/2005/gco}CharacterString').text
                              try: 
                                 mail=org.find('{http://www.isotc211.org/2005/gmd}contactInfo/{http://www.isotc211.org/2005/gmd}CI_Contact/{http://www.isotc211.org/2005/gmd}address/{http://www.isotc211.org/2005/gmd}CI_Address/{http://www.isotc211.org/2005/gmd}electronicMailAddress/{http://www.isotc211.org/2005/gco}CharacterString').text
                              except:
                                 mail=None
####
                              try: 
                                 phone=org.find('{http://www.isotc211.org/2005/gmd}contactInfo/{http://www.isotc211.org/2005/gmd}CI_Contact/{http://www.isotc211.org/2005/gmd}phone/{http://www.isotc211.org/2005/gmd}CI_Telephone/{http://www.isotc211.org/2005/gmd}voice/{http://www.isotc211.org/2005/gco}CharacterString').text
                              except:
                                 phone=None
                              try: 
                                 url=org.find('{http://www.isotc211.org/2005/gmd}contactInfo/{http://www.isotc211.org/2005/gmd}CI_Contact/{http://www.isotc211.org/2005/gmd}onlineResource/{http://www.isotc211.org/2005/gmd}CI_OnlineResource/{http://www.isotc211.org/2005/gmd}linkage/{http://www.isotc211.org/2005/gmd}URL').text
                              except:
                                 url=None
###
                              self.orgfirstmail.update({name:[mail,phone,url]})
                        except: self.orgfirstmail={None:[None,None,None]}

                        try:

                           temp=self.root.find('{http://www.isotc211.org/2005/gmd}dataQualityInfo/{http://www.isotc211.org/2005/gmd}DQ_DataQuality/{http://www.isotc211.org/2005/gmd}report/{http://www.isotc211.org/2005/gmd}DQ_DomainConsistency/{http://www.isotc211.org/2005/gmd}result/{http://www.isotc211.org/2005/gmd}DQ_ConformanceResult')
                              
                           try: Specification=temp.find('{http://www.isotc211.org/2005/gmd}specification/{http://www.isotc211.org/2005/gmd}CI_Citation/{http://www.isotc211.org/2005/gmd}title/{http://www.isotc211.org/2005/gco}CharacterString').text
                           except: Specification=None

                           try: date=temp.find('{http://www.isotc211.org/2005/gmd}specification/{http://www.isotc211.org/2005/gmd}CI_Citation/{http://www.isotc211.org/2005/gmd}date/{http://www.isotc211.org/2005/gmd}CI_Date/{http://www.isotc211.org/2005/gmd}date/{http://www.isotc211.org/2005/gco}Date').text
                           except: date=None

                           try: date_type=temp.find('{http://www.isotc211.org/2005/gmd}specification/{http://www.isotc211.org/2005/gmd}CI_Citation/{http://www.isotc211.org/2005/gmd}date/{http://www.isotc211.org/2005/gmd}CI_Date/{http://www.isotc211.org/2005/gmd}dateType/{http://www.isotc211.org/2005/gmd}CI_DateTypeCode').text
                           except: date_type=None

                           try: result=temp.find('{http://www.isotc211.org/2005/gmd}pass/{http://www.isotc211.org/2005/gco}Boolean').text
                           except: result=None

                           self.firstSpecification=[Specification,date,date_type,result]
                        except: self.firstSpecificationl=[None,None,None,None]



                        try : self.UUID = self.getElementVal(self.isoModel.UUID())
                        except : self.UUID = [[]]
                        
                        try : self.title = self.getElementVal(self.isoModel.title())
                        except : self.title = [[]]
                        
                        try : self.abstract = self.getElementVal(self.isoModel.abstract())
                        except : self.abstract = [[]]
                        
                        try : self.typedata = self.getElementVal(self.isoModel.typedata())
                        except : self.typedata = [[]]
                        
                        try : self.localisators = self.getElementVal(self.isoModel.localisators())
                        except : self.localisators = [[]]
                        
                        try : self.tablecarac = self.getElementVal(self.isoModel.tablecarac())
                        except : self.tablecarac = [[]]
                        
                        try : self.rs_identifier = self.getElementVal(self.isoModel.rs_identifier())
                        except : self.rs_identifier = [[]]
                        
                        try : self.languesjdd = self.getElementVal(self.isoModel.languesjdd())
                        except : self.languesjdd = [[]]
                        
                        try : self.categories = self.getElementVal(self.isoModel.categories())
                        except : self.categories = [[]]

                        #TOTO 2.8.0
                        try : self.codecategories = self.getElementVal(self.isoModel.codecategories())
                        except : self.codecategories = [[]]
                        
                        try : self.keywordsF = self.getElementVal(self.isoModel.keywordsF())
                        except : self.keywordsF = [[]]
                        
                        try : self.keywordsFNC = self.getElementVal(self.isoModel.keywordsFNC())
                        except : self.keywordsFNC = [[]]
                        
                        try : self.timeperiodes = self.getElementVal(self.isoModel.timeperiodes())
                        except : self.timeperiodes = [[]]
                   
                        try : self.dates = self.getElementVal(self.isoModel.dates())
                        except : self.dates = [[]]
                        
                        try : self.formatsjdd = self.getElementVal(self.isoModel.formatsjdd())
                        except : self.formatsjdd = [[]]
                        
                        try : self.boundingboxcoordinates = self.getElementVal(self.isoModel.boundingboxcoordinates())
                        except : self.boundingboxcoordinates = [[]]
                        
                        try : self.scr = self.getElementVal(self.isoModel.scr())
                        except : self.scr = [[]]
                        
                        try : self.genealogie = self.getElementVal(self.isoModel.genealogie())
                        except : self.genealogie = [[]]
                        
                        try : self.coherence = self.getElementVal(self.isoModel.coherence())
                        except : self.coherence = [[]]
                        
                        try : self.scalesEC = self.getElementVal(self.isoModel.scalesEC())
                        except : self.scalesEC = [[]]
                        
                        try : self.scalesUM = self.getElementVal(self.isoModel.scalesUM())
                        except : self.scalesUM = [[]]
                        
                        try : self.UnitsScalesUM = self.getElementVal(self.isoModel.UnitsScalesUM())
                        except : self.UnitsScalesUM = [[]]
                        
                        try : self.conformities = self.getElementVal(self.isoModel.conformities())
                        except : self.conformities = [[]]
                        
                        try : self.legalconstraints = self.getElementVal(self.isoModel.legalconstraints())
                        except : self.legalconstraints = [[]]
                        
                        try : self.accessconstraints = self.getElementVal(self.isoModel.accessconstraints())
                        except : self.accessconstraints = [[]]
                        
                        try : self.otherconstraints = self.getElementVal(self.isoModel.otherconstraints())
                        except : self.otherconstraints = [[]]
                        
                        try : self.authors = self.getElementVal(self.isoModel.authors())
                        except : self.authors = [[]]

                        try : self.pointsofcontact = self.getElementVal(self.isoModel.pointsofcontact())
                        except : self.pointsofcontact = [[]]
                        
                        try : self.pointsofcontactMDD = self.getElementVal(self.isoModel.pointsofcontactMDD())
                        except : self.pointsofcontactMDD = [[]]
                        
                        try : self.pointsofcontactCust  = self.getElementVal(self.isoModel.pointsofcontactCust())
                        except : self.pointsofcontactCust = [[]]
                        
                        try : self.languemdd = self.getElementVal(self.isoModel.languemdd())
                        except : self.languemdd = [[]]
                        
                        try : self.datetmdd = self.getElementVal(self.isoModel.datetmdd())
                        except : self.datetmdd = [[]]
                        
                        try : self.datemdd = self.getElementVal(self.isoModel.datemdd())
                        except : self.datemdd = [[]]
# added 4_6_2015 #############
                        try : self.useLimitation = self.getElementVal(self.isoModel.useLimitation())
                        except : self.useLimitation = [[]]

                        try : self.otherConstraints = self.getElementVal(self.isoModel.otherConstraints())
                        except : self.otherConstraints = [[]]
                        
                        try : self.rs_identifier2 = self.getElementVal(self.isoModel.rs_identifier2())
                        except : self.rs_identifier2 = [[]]
###################

                else :
                        self.pointsofcontact = self.getElementVal(self.isoModel.pointsofcontact())
                        self.pointsofcontactCust = self.getElementVal(self.isoModel.pointsofcontactCust())

		return True

	def boundingDateRange(self,boundingDatesList):
		allDates, returnDates = [], {}
		for outer in boundingDatesList:
			for inner in outer.keys():
				if outer[inner] is not None:
					if outer[inner] != 'None': allDates.append(outer[inner])
                if allDates != []:
                    returnDates['start'] = min(allDates)
                    returnDates['end'] = max(allDates)
		return returnDates


	def importISOxmlDefinition(self,format):
		if format == 'MEDDE':
		   from xmlISOreaderTag import xmlISOreaderTag as isoModel
		self.isoModel = isoModel()
			
	def getElementVal(self,keyMethod):
		returnValList, returnVal, dataStruct, counter =[], 'None', {}, 0
		for i in keyMethod:
                        if type(i) is dict:
                           for j in i.keys(): dataStruct[counter]=j
                        if type(i) is str: dataStruct[counter] = i
                        counter = counter + 1
		
		valueList, ordering, cnt = [], False, 1
                zTempoData = ""

		for i in dataStruct.keys()[1:]:
			thisData = keyMethod[i][dataStruct[i]]
                        
                        if 'basilexpath' in thisData.keys():
                                returnVal =  self.returnBaliseElt(thisData['basilexpath'])
                                valueList.append(returnVal)                                

                        if 'basilexpathvalue' in thisData.keys():
                                returnVal =  self.returnBaliseEltValue(thisData['basilexpathvalue'])
                                valueList.append(returnVal)
			
			if 'baseXpath' in thisData.keys():
                                #if 'elValXpath' in thisData.keys() and 'depValXpath' in thisData.keys() and 'depVal' in thisData.keys():
                                returnVal = self.returnDependantElementVal(thisData['baseXpath'],thisData['elValXpath'],thisData['depValXpath'],thisData['depVal'])
                                valueList.append(returnVal)
								
			if 'xpath' in thisData.keys():
                                returnVal =  self.returnSimpleElementVal(thisData['xpath'])
                                zTempoData = thisData['xpath']
                                if returnVal == [] and zTempoData == "gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode" :
                                        if 'baseXpath' in thisData.keys():
                                                returnVal = self.returnDependantElementVal(thisData['baseXpath'],thisData['elValXpath'],thisData['depValXpath'],thisData['depVal'])
                                                valueList.append(returnVal)
				else : valueList.append(returnVal)
				
			if 'order' in keyMethod[i].keys(): ordering, orderingList = True, thisData				
			else: pass
			cnt = cnt + 1
		
                if [] in valueList : return valueList
		if ordering:
			checkCompLnth = len(valueList[0])
			index=0
		
			for list in valueList:
				if len(list) != checkCompLnth:
                                        if len(list)> checkCompLnth:
                                           zElt = ""
                                           for elt in list : zElt+= " %s" % (elt)
                                           list=[]
                                           list.append(zElt)
                                           valueList[index] = list
                                        else : return 'None'
                                if zTempoData.startswith('gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo') or zTempoData.startswith('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact'):
                                   if list[0]==None :
                                         list=[]
                                         if index==0 : list.append("pointOfContact")
                                         elif index==3 and self.langueTR=="fr": list.append("France")
                                         else : list.append("")
                                         valueList[index] = list                                             
                                index+=1

			outer = []

			for localPos in range(0,checkCompLnth):
				inner=[]
				for listPos in range(0,len(valueList)):
                                    inner.append(valueList[listPos][localPos]) if valueList[listPos][localPos]!=None else inner.append(" ")    
				outer.append(inner)
		
			for returnedList in outer:
				orderedValsSub = {}
				if len(returnedList) != len(orderingList): returnValList.append('None')
				else:		
          		            for i in orderingList.keys(): orderedValsSub[i] = returnedList[orderingList[i]-1] 
   				    returnValList.append(orderedValsSub)
			
			return returnValList
			
		else:
			return valueList
			
			

	def returnDependantElementVal(self,baseXpath,elXpath,depXpath,depValReqd):
		baseXpath = self.appendNameSpace(baseXpath)
		resDependantVal = []
		try: rootEl = self.root.findall(baseXpath) 
		except:	return 'None'

		for el in rootEl:
			thisElXpth = self.appendNameSpace(elXpath)
			thisEl = self.doFindall(el,thisElXpth)
			if thisEl != 'None':
				elVal = thisEl[0].text 
                		thisEldepXpth = self.appendNameSpace(depXpath)					
				thisDepEl = self.doFindall(el,thisEldepXpth)								
				if thisDepEl != 'None':
        				depVal = thisDepEl[0].text
			                resDependantVal.append(elVal)			
																			
		return resDependantVal

	def returnBaliseElt(self,xpath):
		xpathNS = self.appendNameSpace(xpath)
		resElementVal = []
		try: rootEl = self.root.findall(xpathNS)
		except: return ['None']
		for elVal in rootEl:
		    if elVal is None: resElementVal.append('None')
		    else:
                       if elVal.attrib == {}:
                          for childItem in elVal :
                              if childItem.tag.find("Boolean")!=-1 : resElementVal.append(childItem.text)
                       else : resElementVal.append(elVal.attrib)
                return resElementVal        

	def returnBaliseEltValue(self,xpath):
		xpathNS = self.appendNameSpace(xpath)
		resElementVal = []
		try: rootEl = self.root.findall(xpathNS)
		except: return ['None']
		for elVal in rootEl:
		    if elVal is None: resElementVal.append('None')
		    else:
                       if elVal.attrib == {}:
                          for childItem in elVal :
                              if childItem.tag.find("Boolean")!=-1 : resElementVal.append(childItem.text)
                       else : resElementVal.append(elVal.attrib['codeListValue'])
                return resElementVal
                       
		
	def returnSimpleElementVal(self,xpath):
		xpathNS = self.appendNameSpace(xpath)
                #print "xpathNS", xpathNS, "xpath", xpath
		resElementVal = []
		try: rootEl = self.root.findall(xpathNS)
		except: return ['None']
		for elVal in rootEl:
			if elVal is None: resElementVal.append('None')
			else: resElementVal.append(elVal.text)
		return resElementVal

	def doFindall(self,el,thisElXpth):
		try:
			thisElXpthEl = el.findall(thisElXpth)
			if len(thisElXpthEl) == 0: thisElXpthEl = 'None'
		except: thisElXpthEl = 'None'
		return thisElXpthEl
		
		

	def getXmlVal(self,paths):
		xmlVals = []
		for path in paths:
			try: xmlVals.append(self.root.find(path).text)			
			except:	xmlVals.append('null')
		return xmlVals					
		

	def isoNameSpaces(self):
                """        
                namespaces={'om':'http://www.opengis.net/om/1.0',
                        'gml':'http://www.opengis.net/gml/3.2',
                        'swe':'http://www.opengis.net/swe/1.0.2',
                        'ioos':'http://www.noaa.gov/ioos/0.6.1',
                         'sos':'http://www.opengis.net/sos/1.0'}

                namespaces2={'om':'http://www.opengis.net/om/1.0',
                        'gml':'http://www.opengis.net/gml',
                        'swe':'http://www.opengis.net/swe/1.0.1',
                        'ioos':'http://www.noaa.gov/ioos/0.6.1',
                        'sos':'http://www.opengis.net/sos/1.0',
                        'ogc':'http://www.opengis.net/ogc',
                        'tml':'http://www.opengis.net/tml',
                        'sml':'http://www.opengis.net/sensorML/1.0.1',
                        'myorg':'http://www.myorg.org/features',
                        'xlink':'http://www.w3.org/1999/xlink'}
		"""
		isoNs = {'gmd':'http://www.isotc211.org/2005/gmd',
                         'gco':'http://www.isotc211.org/2005/gco',
			 'gmx':'http://www.isotc211.org/2005/gmx',
                         'gml':'http://www.opengis.net/gml',
			 'none':''
			 }
		return isoNs
	
	
	def defaultIsoNamespace(self):  return 'gmd'
	
	def getIsoXML(self, file, dataXML):
		etree = ET.parse(file) if file!= None else ET.parse(dataXML)
		root=etree.getroot()
		if root.tag != '{http://www.isotc211.org/2005/gmd}MD_Metadata':	return None
		return root
		
	def appendNameSpaceList(self,paths):
		nameSpaceAppendedPaths = []
		for path in paths:		
			pathElements = path.split('/')
			count = 0
			for element in pathElements:
				try:					
					if ':' in element:						
						splitElement = element.split(':')
						nsPrefix,nsElement = splitElement[0],splitElement[1]
					else:
						nsPrefix = self.defaultIsoNamespace()
						nsElement = element
					if count == 0: appendedPath = '{%s}%s' % (self.isoNameSpaces()[nsPrefix], nsElement)
					else: appendedPath = '%s/{%s}%s' % (appendedPath , self.isoNameSpaces()[nsPrefix] , nsElement)						
					count += 1
				except:	appendedPath = 'null'
							
			appendedPath = appendedPath.replace('{}','')
			nameSpaceAppendedPaths.append(appendedPath)
		return nameSpaceAppendedPaths
	

	def appendNameSpace(self,path):
		nameSpaceAppendedPath = ''
		pathElements = path.split('/')
		count = 0
		for element in pathElements:
			try:					
				if ':' in element:						
					splitElement = element.split(':')
					nsPrefix,nsElement = splitElement[0],splitElement[1]
				else:
					nsPrefix = self.defaultIsoNamespace()
					nsElement = element
				if count == 0: appendedPath = '{%s}%s' % (self.isoNameSpaces()[nsPrefix] , nsElement)
				else: appendedPath = '%s/{%s}%s' % (appendedPath , self.isoNameSpaces()[nsPrefix] , nsElement)
				count += 1
			except:	appendedPath = 'null'
		nameSpaceAppendedPath = appendedPath.replace('{}','')
		return nameSpaceAppendedPath

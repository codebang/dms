from py2xml import Py2XML


class Job(object):
  def __init__(self):
    self.definition = {
        'joblist':[{
                "description":[],
                "dispatch": [{"excludePrecedence":["true"],"keepgoing":["false"],"rankOrder":["ascending"],"threadcount":["1"]}],
                "nodefilters":{"filter":[]},
                "executionEnabled":['true'],
                "id": ["fd026e9e-8be4-469e-b732-8d9605f7c57e"],
                "name": [],
                "scheduleEnabled": ["true"],
                "sequence keepgoing='true' strategy='node-first'":[],
                "uuid":["fd026e9e-8be4-469e-b732-8d9605f7c57e"]
                }]
     } 
  
  def _addsequence(self,dict):
    self.definition['joblist'][0]["sequence keepgoing='true' strategy='node-first'"].append(dict)

  def addCopyFile(self,src,dst):
    dict = {'node-step-plugin':{"type":"copyfile","configuration":[{"key":"destinationPath","value":dst},{"key":"echo","value":"true"},{"key":"sourcePath","value":src}]}}
    self._addsequence(dict)
 
  def addCommand(self,command):
    dict = {"exec": command}
    self._addsequence(dict)

  def setDescription(self,desp):
    self.definition['joblist'][0]['description'].append(desp)

  def setName(self,name):
    self.definition['joblist'][0]['name'].append(name)

  def setNodeFilter(self,name):
    self.definition['joblist'][0]['nodefilters']['filter'].append(name)

  
  def to_xml(self):
    serializer = Py2XML()
    xml_string = serializer.parse( self.definition )
    return xml_string
  




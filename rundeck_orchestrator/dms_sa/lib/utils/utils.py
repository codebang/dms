import urllib2
import urllib
import xml.etree.ElementTree as ET
import os
import json
import xml
from xml.dom import minidom

import lib.env



def _post(url,data):
  req = urllib2.Request(url,headers={"X-Rundeck-Auth-Token":lib.env.token})
  data = urllib.urlencode(data) 
  response = urllib2.urlopen(req,data)
  return response.read()

def _get(url):
  req = urllib2.Request(url,headers={"X-Rundeck-Auth-Token":lib.env.token})
  response = urllib2.urlopen(req)
  return response.read()


def _Indent(dom, node, indent = 0):
  # Copy child list because it will change soon
  children = node.childNodes[:]
  # Main node doesn't need to be indented
  if indent:
    text = dom.createTextNode('\n' + '\t' * indent)
    node.parentNode.insertBefore(text, node)
  if children:
    # Append newline after last child, except for text nodes
    if children[-1].nodeType == node.ELEMENT_NODE:
      text = dom.createTextNode('\n' + '\t' * indent)
      node.appendChild(text)
      # Indent children which are elements
      for n in children:
        if n.nodeType == node.ELEMENT_NODE:
          _Indent(dom, n, indent + 1)

def _getNodeXml(attrs):
  impl = xml.dom.minidom.getDOMImplementation()
  dom = impl.createDocument(None, 'project', None)
  root = dom.documentElement
  node = dom.createElement('node')
  root.appendChild(node)
  for (name,value) in attrs.items():
    node.setAttribute(name,value)
  return dom


def getnodes():
  nodes={}
  xml = _get(lib.env.url_list_resources)
  root = ET.fromstring(xml)
  for elem in root.iterfind('node'):
     nodes[elem.attrib["name"]]=elem.attrib["tags"]
  return nodes


def createnode(attrs,nodeId):
  dom= _getNodeXml(attrs)
  domcopy = dom.cloneNode(True)
  _Indent(domcopy, domcopy.documentElement)
  f = open(os.path.join(lib.env.res_path,nodeId+'.xml'), 'wb')
  domcopy.writexml(f, encoding = 'utf-8')
  domcopy.unlink()
  f.close

def deletenode(nodeId):
  os.remove(os.path.join(lib.env.res_path,nodeId + '.xml'))

def createjob(job_xml):
  req = urllib2.Request(lib.env.url_create_job,data=job_xml,headers={"X-Rundeck-Auth-Token":lib.env.token,"Content-Type":'application/xml'})
  response = urllib2.urlopen(req)
  xml_resp = response.read()
  print xml_resp
  root = ET.fromstring(xml_resp)
  return root.find('./succeeded/job/id').text  

def runjob(jobid):
  dict={"loglevel":"INFO"}
  yaml=json.dumps(dict)
  req = urllib2.Request(lib.env.url_run_job % jobid,data=yaml,headers={"X-Rundeck-Auth-Token":lib.env.token,"Content-Type":'application/json'})
  response = urllib2.urlopen(req)
  return response.read()

def runmonitor(jobid,custom_name):
  dict={"loglevel" : "INFO", "argString":"-customer_name %s" % custom_name }
  yaml = json.dumps(dict)
  req = urllib2.Request(lib.env.url_run_job % jobid,data=yaml,headers={"X-Rundeck-Auth-Token":lib.env.token,"Content-Type":'application/json'})
  response = urllib2.urlopen(req)
  return response.read()

def queryjob(jobname):
   xml_string=_get(lib.env.url_query_job % jobname)
   doc = minidom.parseString(xml_string)
   root = doc.documentElement
   joblist = root.getElementsByTagName('job')
   return  joblist[0].getAttribute('id')

def deletejob(id):
  req = urllib2.Request(lib.env.url_delete_job % id,headers={"X-Rundeck-Auth-Token":lib.env.token})
  req.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(req)
  return response.read() 

  
def getTemplateName(event_name):
  return event_name.lower()

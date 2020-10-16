import json
import urllib.parse
from NCMB.NCMBObject import NCMBObject
from NCMB.NCMBRequest import NCMBRequest
from NCMB.NCMBSignature import NCMBSignature

class NCMB:
  fqdn = 'mbaas.api.nifcloud.com'
  version = '2013-09-01'
  applicationKeyName = 'X-NCMB-Application-Key'
  timestampName = 'X-NCMB-Timestamp'
  sessionTokenHeader = 'X-NCMB-Apps-Session-Token'
  
  def __init__(self, applicationKey, clientKey):
    self.applicationKey = applicationKey
    self.clientKey = clientKey
    self.sessionToken = None
    NCMBObject.NCMB = self
    NCMBRequest.NCMB = self
    NCMBSignature.ncmb = self

  def Object(self, class_name):
    return NCMBObject(class_name)

  def path(self, class_name, objectId):
    if class_name[0] == '/':
      return f'/{NCMB.version}{class_name}/{objectId or ""}'
    if class_name in ['installations', 'users', 'files', 'push']:
      return f'/{NCMB.version}/{class_name}/{objectId or ""}'
    return f'/{NCMB.version}/classes/{class_name}/{objectId or ""}'

  def encodeQuery(self, queries):
    encoded_queries = []
    for key in sorted(queries.items(), key=lambda x:x[0]):
      value = queries[key[0]]
      if type(value) in (list, dict):
        value = json.dumps(value, separators=(',', ':'))
      safe = ":" if key[0] == 'X-NCMB-Timestamp' else ""
      encoded_queries.append(f'{key[0]}={urllib.parse.quote(value, safe=safe)}')
    return '&'.join(encoded_queries)
  def url(self, class_name, queries, objectId):
    query = self.encodeQuery(queries)
    if query != "":
      query = f'?{query}'
    return f'https://{NCMB.fqdn}{self.path(class_name, objectId)}{query}'
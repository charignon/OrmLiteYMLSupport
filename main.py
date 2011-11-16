import yaml

#Keywords of the YML file
MODELS = "Models"
CONFIG = "Config"

class Field(object):
  _type     = ""   
  name      = ""
  index     = False
  generated = False
  
  def __init__(self, content, model_name, field_name):
    self.name = field_name
    for item in content[MODELS][model_name][field_name]:
      if item == "type":
        self._type  = content[MODELS][model_name][field_name][item]
      elif item == "generated":
        self.generated  = content[MODELS][model_name][field_name][item]
      elif item == "index":
        self.index  = content[MODELS][model_name][field_name][item]
  
  def __str__(self):
    ret = self._type + " " + self.name + " index:" + str(self.index)+   " generated:"+str(self.generated) 
    return ret

  def __repr__(self):
    return self.__str__()
  
  def getModifiers(self):
    #Make a modifier list
    modifiers = []
    result = ""
    if self.index:
      modifiers.append("index = true")
    if self.generated:
      modifiers.append("generated = true")
    if len(modifiers) > 1:
      result = "("
      for modifier in modifiers : 
        result = result + modifier +","
      #remove the trailing ,
      return result[:-1]+")"

    elif len(modifiers) == 1:
      return "("+modifiers[0]+")"
    
    else:
      return ""


  def toJavaField(self):
    ret = "@DatabaseField"
    ret = ret + getModifiers(self) +"\n"
    
    



class ConfigInfo(object):
  package_name = None
  def __init__(self):
    pass
  def setPackageName(self, package_name):
    self.package_name = package_name
  def get_java_header(self):
    if self.package_name:
      return "package "+self.package_name+";" 
    else:
      return ""

class Model(object):
  name = ""
  fields=[]
  def __init__(self, content,model_name ):
    for field in content[MODELS][model_name]:
      self.fields.append(Field(content,model_name,field))
    self.name = str(model_name)
  def __str__(self):
    return str(self.fields)
  def toJavaBody(self):
    body = "public class "+self.name+" { \n"
    for field in self.fields:
      field.getModifiers()
    return body














class ParseUtils(object):

  #Get the configuration information
  @staticmethod
  def get_configuration(content):
    #try to find a Config information, if there is none
    #assume that the user didn't provide it
    config = ConfigInfo()
    try:
      config.setPackageName(content[CONFIG]["package-name"])
    except:
      pass
    finally:
      return config

  #Get the models in a list
  @staticmethod 
  def get_models(content):
    models = []
    try:
      for model in content[MODELS]:
        models.append(Model(content,model))
    except:
      #the case where no models are given
      pass
    finally:
      return models







if __name__ == "__main__":
  f = open("config.yml")
  content =  yaml.load(f)
  f.close()
  config = ParseUtils.get_configuration(content) 
  models = ParseUtils.get_models(content)
  

  print config.get_java_header()
  for model in models:
    print model.toJavaBody()

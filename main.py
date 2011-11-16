import yaml
import shutil
import os

#Keywords of the YML file and other configuration
MODELS  = "Models"
CONFIG  = "Config"
SRC_DIR = "src"



#Rerpresents a Model of the database
class Model(object):
  name = ""
  fields=[]
  def __init__(self, content,model_name ):
    for field in content[MODELS][model_name]:
      self.fields.append(Field(content,model_name,field))
    self.name = str(model_name)
  def __str__(self):
    return str(self.fields)
  #Return the body of the model in java (the core of the java file)
  def toJavaBody(self):
    body  = "@DatabaseTable\n"
    body = body + "public class "+self.name+" { \n\n"
    for field in self.fields:
      body = body + field.toJavaField()  + "\n\n"
    for field in self.fields:
      body = body + field.toJavaGetter()  + "\n\n"
    for field in self.fields:
      body = body + field.toJavaSetter()  + "\n\n"
    return body + "}"
  



#Represents a field of a model
class Field(object):
  _type       = ""   
  name        = ""
  index       = False
  generated   = False
  foreign     = False
  canBeNull   = False
  columnName  = "" 

  def __init__(self, content, model_name, field_name):
    self.name = field_name
    for item in content[MODELS][model_name][field_name]:
      item_parsed  = content[MODELS][model_name][field_name][item]
      if item == "type":                self._type      = item_parsed
      elif item == "generated":         self.generated  =  item_parsed
      elif item == "index":             self.index      = item_parsed
      elif item == "canBeNull":         self.canBeNull  = item_parsed
      elif item == "foreign":           self.foreign      = item_parsed
      elif item == "columnName":        self.columnName   = item_parsed



  def __str__(self):
    ret = self._type + " " + self.name + " index:" + str(self.index)+   " generated:"+str(self.generated) 
    return ret

  def __repr__(self):
    return self.__str__()

  #The modifiers are everything except the type and the name of the field
  #This function returns the modifier in the Java annotation style
  def getModifiers(self):
    #Make a modifier list
    modifiers = []
    result = ""
    if self.index:
      modifiers.append("index = true")
    if self.generated:
      modifiers.append("generated = true")
    if self.foreign:
      modifiers.append("foreign = true")
    if self.canBeNull:
      modifiers.append("canBeNull = true")
    if self.columnName:
      modifiers.append("columnName = \""+self.columnName+"\"")



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

  #return the field in the java style
  def toJavaField(self):
    ret = "  @DatabaseField"
    ret = ret + self.getModifiers() +"\n  "
    ret = ret +  "private " + str(self._type) + " " + str(self.name)+";"
    return ret    
  #return a java getter for the field
  def toJavaGetter(self):
    ret = "  public "+self._type+" get"+self.name[0].upper()+""+self.name[1:]+"() {\n      "
    ret = ret + " return " + self.name +";\n  }" 
    return ret

  #return a java setter for the field
  def toJavaSetter(self):
    ret = "  public void set"+self.name[0].upper()+""+self.name[1:]+"( "+self._type+ " "+self.name+") {\n      "
    ret = ret + " this." + self.name + "="+self.name+";\n  }" 
    return ret




#Contains the global configuration information of the current
#generation process
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


#Retrieve the configuration and the models from the java file
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


#Does basic operation on files (high level)
class FileUtils(object):
  @staticmethod
  def create_source_dir():
    shutil.rmtree("./"+SRC_DIR, ignore_errors=True)
    os.mkdir(SRC_DIR)
  @staticmethod
  def create_source_file(filename, content):
    f = open("./"+SRC_DIR+"/"+filename,"w")
    f.write(content)
    f.close()




if __name__ == "__main__":
  f = open("config.yml")
  content =  yaml.load(f)
  f.close()
  config = ParseUtils.get_configuration(content) 
  models = ParseUtils.get_models(content)
  
  FileUtils.create_source_dir()
  for model in models:
    filename  = model.name +".java"
    FileUtils.create_source_file(filename,config.get_java_header()+"\n\n"+model.toJavaBody())
    print "Created:      "+filename









Author: Laurent Charignon
Date  : November 2011


CONTENT
=======

This python script is a tool that can make things easy while using ORMLite.
It generate Java Models and Config Files from a .yml file.
It looks like the Doctrine behavior to generate models on Symfony based projects.


INSTALL
=======
You need to install python 2.7 and pyyaml extension for python before using this script.
For the moment the script reads the content of a .yml file and generate the java classes (not yet the configuration files) on a separate directory.
Those detailed could be changed in the first line of the python script (for the moment main.py).
A sample of .yml file is attached in the folder as well as some sample outputs


EXAMPLE
=======

From this Yaml file, the program will generate two java models *SimpleData* and *Counter* and will create all the necessary anotations, getters, setters and so forth...
<blockquote>
#A model
Models:
  SimpleData:
    id:
      type: int
      generated: true
    string:
      type: String
      generated: true
      columnName: "BOB"
    millis:
      type: long
    date:
      type: Date
    even:
      type: boolean

  Counter:
    id:
      type: int
      generated: true
    value:
      type: int
    date:
      type: Date

</blockquote>





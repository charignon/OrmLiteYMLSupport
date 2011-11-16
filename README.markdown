Author: Laurent Charignon
Date  : November 2011


CONTENT
=======

This python script is a tool that can make things easy while using [ORMLite][1].
It generate Java Models and Config Files from a .yml (YAML) file.
It looks like the [Doctrine yml files][2] to generate models on [Symfony][3] based projects.


INSTALL
=======
You need to install python 2.7 and pyyaml extension for python before using this script.
On Ubuntu 11.10:

        sudo easy_install pyyaml

For the moment the script reads the content of a .yml file and generate the java classes (not yet the configuration files) on a separate directory.
Those detailed could be changed in the first line of the python script (for the moment main.py).
A sample of .yml file is attached in the folder as well as some sample outputs
To launch the script just type:

        python ./main.py


EXAMPLE
=======

From this Yaml file, the program will generate two java models *SimpleData* and *Counter* and will create all the necessary anotations, getters, setters and so forth...

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


[1]: http://ormlite.com/        "ORMLite"
[2]: http://www.doctrine-project.org/documentation/manual/1_2/pl/yaml-schema-files  "Doctrine YAML Schema"
[3]: http://www.symfony-project.org/   "Symfony"

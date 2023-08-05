EruditArticle Check
===================

A python library and command line tool to perform the validation of  
*EruditArticle* XMLs.

How to install
--------------

pip install eacheck

How to use
----------

**For command line help**

#> eacheck -h

**To validated a XML file (output in text mode)**

#> eacheck file.xml 

**To validated a XML file (output in json mode)**

#> eacheck file.xml -f json

**Writing output to o file**

#> eacheck file.xml -f json > output.json

EruditArticle Webapp
====================

A webapp to performe the validation of *EruditArticle* XMLs.

Docker Image
============

docker run --name eacheck -p 8000:8000 -i -t erudit/eacheck
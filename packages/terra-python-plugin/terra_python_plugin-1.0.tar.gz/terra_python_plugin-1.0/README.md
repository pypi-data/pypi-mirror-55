# Python Data Plugin

## Introduction
A python plugin to load data from any connected platform e.g. sponsored-data, marketing console e.t.c.
to a connected API.

### Technologies
Python==3.7.2  
requests==2.22.0

### Method
Method: send_data(data, data_source, data_type)  
data - the data to be sent in json format which could either be loaded as a valid python object or a file(.json)  
data_source - the platform for which the data is associated.  
data_type - the specific of the data.

### Valid data sources
- Marketing console 
- Sponsored data
- Trivia
### Valid data types
- Demography
- Transactional
- Billing


### How to Launch
##### Download the source code of the project  
git clone https://D-Scipher@bitbucket.org/terragonengineering/kafka-python-plugin.git  
##### Goto the downloaded directory
cd kafka-python-plugin
##### Run setup.py to install
python setup.py install  
### Using the module
from terra_python_plugin import PythonPlugin  
plugin = PythonPlugin()  
sample_data = '{"name": "Timothy", "level": 2}'  
plugin.send_data(sample_data, 'sponsored data', 'demography')  

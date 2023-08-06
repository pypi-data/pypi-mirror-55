## what it is
Olive is a python package for accessing vessel data from the AIS Database. 

## requirements
- Python 3.6

- AWS credentials from the TA Solutions "Alpha" account

## configuring your AWS credentials

Olive will automatically look for your Alpha AWS credentials in an aws credentials file. 

It will first look for credentials under a profile named `alpha`, otherwise it will use the credentials under the 
`default` profile. Instructions for installing AWS CLI and creating a new credentials file are below 
([reference](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)). 

If you already have an aws 
credentials file, you can also just open it in a text editor and add the following:

```
[alpha]
aws_access_key_id = <aws-access-key-for-alpha-account>
aws_secret_access_key = <aws-secret-access-key-for-alpha-account>
```

To install ASW CLI and create the credentials file, modify the following prompts as needed and execute them in the 
terminal. First, install AWS CLI.

`pip install awscli`

Create the credentials file using your Alpha credentials.

`aws configure set aws_access_key_id <alpha_access_key_id>`

`aws configure set aws_secret_access_key <alpha_secret_access_key>`

## installing olive
You can use pip to install olive, for example, `pip install olive`.

Here are some instructions on how to create a new conda environment and install olive. In the terminal, create a new 
conda environment with python 3.6 and follow prompts.

`conda create -n olive python=3.6`

Activate your new olive environment.

`conda activate olive`

Pip install the olive package.

`pip install olive`

### how to use olive

You should now be able to use olive to request vessel data from the AIS database. Use the following python code to 
both test that the install worked and that you can access the database. 

```python
from olive.metadata import GetMetadata
from pprint import pprint

# initialize metadata object, which will also configure your aws session
metagetter = GetMetadata()

# define mmsi (Maritime Mobile Service Identity) for the vessel of interest
example_mmsi = '211484674'

# this will return a json dictionary containing the vessel's most recent attributes
attributes = metagetter.get_current_attributes(mmsi=example_mmsi)

pprint(attributes)
```

In this first iteration of olive, there are three methods for retrieving vessel data from the AIS database. We have just demonstrated the 
first method, which returns a dictionary containing the current vessel attributes for a given mmsi. Here are examples of 
using the other two methods. 

The `get_timestamps` method will return a dictionary containing the most recent timestamps for the requested vessel's attributes.

```python
# retrieve timestamp for a vessel's most recent attribute change
timestamps = metagetter.get_timestamps(mmsi=example_mmsi)

pprint(timestamps)
```

If the vessel's attribute has been changed, the `changelog` method will provide the the timestamp for each time it changed. 
Inputs include the desired mmsi, attribute, and a date range (formatting should follow the example below). The output 
will be a list of dictionaries, each one containing the attribute and timestamp when it changed. 

```python
# retrieve latest changes to vessel attributes
changelog = metagetter.get_changelog(mmsi=example_mmsi,
                                     attribute='vessel_name',
                                     date_start='2019-04-09T10:00:00',
                                     date_end='2019-11-12T20:03:00')

pprint(changelog)
``` 



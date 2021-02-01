Before refactor concrete thing here is a list of things that need to be done all over the code:

1. Go Over All Namings And Improve them

2. Directory Organize:

   Current Directories

   | Directory Name | Porpuse                           |
   | :------------- | :-------------------------------- |
   | host           | files related to host command     |
   | init           | files related to init command     |
   | list           | files related to list command     |
   | login          | files related to login command    |
   | logout         | files related to logout command   |
   | policy         | files related to policy command   |
   | user           | files related to user command     |
   | variable       | files related to variable command |

   

   And this files are without a folder : api.py, client.py, argparse_wrapper.py, cli.py , client.py, config.py, constants.py, credentials_data.py, credentials_form_file.py, endpoint.py, errors.py, http_wrapper.py, ssl_service.py, version.py

   The change i want to make is to organize the files by their types and not by the command they do and have directories that can be used for the files without directory:

   

   | Directory Name | Porpuse                                                      |
   | :------------- | :----------------------------------------------------------- |
   | utils          | Wrappers and utils of diffrent python libsssl_servicearg_parse_wrapperhttp_wrapper |
   | api            | Files that do the directly talk with conjurclient.pyapi.py   |
   | logics         | All logic classes here                                       |
   | controllers    | all controller classes                                       |
   | logics         | all logic classes                                            |
   | data_objects   | all data objects classes                                     |

   

3. Go over thrown exceptions in the code and change them to our own exceptions

4. Type The Function. Use Python3 syntax on all function to add types to the arguments and return types
   Instead of

   `def greeting(name):    `			   
   
   Do This:
   
   `def greeting(name: str) -> str:`
  
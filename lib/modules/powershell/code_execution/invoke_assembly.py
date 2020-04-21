from __future__ import print_function
from builtins import str
from builtins import object
import re
from lib.common import helpers
import pdb

class Module(object):

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-Assembly',

            'Author': ['@TheRealWover'],

            'Description': ("Uses System.Reflection.Assembly.Load to load and execute a "
                            ".NET Assembly of your choice from memory."

            'Background' : False,

            'OpsecSafe' : True,

            'Language' : 'powershell',
            
            'Comments': [
                'https://docs.microsoft.com/en-us/dotnet/api/system.reflection.assembly.load'
            ]

        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Assembly' : {
                'Description'   :   '(Attacker) local .NET Assembly to load from memory.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Class' : {
                'Description'   :   'Class of entry point. A namespace can be specified in the format of "Namespace.Class"',
                'Required'      :   Optional,
                'Value'         :   ''
            },
            'Method' : {
                'Description'   :   'Method to invoke.',
                'Required'      :   Optional,
                'Value'         :   ''
            },
            'Parameters' : {
                'Description'   :   'Command-line parameters.',
                'Required'      :   Optional,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):
        
        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/code_execution/Invoke-Assembly.ps1"
        if obfuscate:
            helpers.obfuscate_module(moduleSource=moduleSource, obfuscationCommand=obfuscationCommand)
            moduleSource = moduleSource.replace("module_source", "obfuscated_module_source")
        try:
            f = open(moduleSource, 'r')
        except:
            print(helpers.color("[!] Could not read module source path at: " + str(moduleSource)))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode

        scriptEnd = "Invoke-Assembly"

        if obfuscate:
            scriptEnd = helpers.obfuscate(self.mainMenu.installPath, psScript=scriptEnd, obfuscationCommand=obfuscationCommand)
        script += scriptEnd
        return script

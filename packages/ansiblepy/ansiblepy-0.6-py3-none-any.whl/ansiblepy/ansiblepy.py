
from builtins import input
import sys
import os
from pymongo import MongoClient
import platform
import random


class Generate:
    """

    """
    def __init__(self):
        """

        """
        
        system = platform.system()
        if system != 'Windows':
            self.base_path = os.path.join('etc', 'ansible', 'ansibly')
            self.file_path = self.base_path + '/playbook_' + str(random.randint(1, 999)) + '.yml'
        else:
            self.base_path = os.getcwd()
            self.file_path = self.base_path + '\\playbook_' + str(random.randint(1, 999)) + '.yml'

        self.__client = MongoClient("mongodb://readonly:readonly@ansibly-shard-00-00-bsfa5.mongodb.net:27017,"
                                    "ansibly-shard-00-01-bsfa5.mongodb.net:27017,ansibly-shard-00-02-bsfa5.mongodb.net:27017/"
                                    "admin?ssl=true&replicaSet=Ansibly-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.__my_db = self.__client['Module_Index']
        self.generates()
        self.final_playbook = str()


    def get_vars_data(self):
        """

        :return:
        """
        var = dict()
        try :
            count = int(eval(input("Please enter number of variable definitions [max 10]: ")))
        except ValueError as e:
            count = int(eval(input("Please provide Integer value for variable definitions [max 10]: ")))
        if type(count) is not int:
            raise ValueError("Integer value expected, but ", type(count), "given!")
        if count > 10:
            self.get_vars_data()
        else:
            for i in range(count):
                var_name = eval(input("Please enter the Variable Name: "))
                var_value = eval(input("Please enter the value for '" + var_name + "': "))
                var[var_name] = var_value
        return var

    def create_roles(self):
        count = int(eval(input("Please enter no. of. roles to be created: [Max 5]")))
        if count > 5:
            self.create_roles()
        else:

            for i in range(1, count + 1):
                name = eval(input("Please enter the name of role {}: ".format(i)))
                leaf = ['tasks', 'vars', 'files', 'handlers', 'meta', 'templates']
                try:

                    for j in leaf:
                        dir = os.path.join(os.getcwd() + os.path.join('/etc/ansible/' + name + '/' + j))
                        os.makedirs(dir)
                    for k in leaf:
                        if k == 'handlers' or k == 'tasks' or k == 'vars':
                            f = os.path.join(os.getcwd() + os.path.join('/etc/ansible/' + name + '/' + k + '/main.yml'))
                            open(f, 'w').close()
                        if k == 'templates':
                            f = os.path.join(os.getcwd() + os.path.join('/etc/ansible/' + name + '/' + k + '/httpd.conf.j2'))
                            open(f, 'w').close()
                except FileExistsError:
                    print("Cannot create the file / directory when it already exists")

    def generates(self):
        """

        :return:
        """
        decide = eval(input("Do you want to create a simple Playbook or Roles? [P/R]"))
        while decide not in ['P', 'R', 'p', 'r']:
            decide = eval(input("Please provide a valid input to proceed. Playbook/Role [P/R]? "))
        if decide.lower() == 'r':
            self.create_roles()
        else:
            self.final_playbook = '---' + '\n' + '- name: Ansible Playbook' + '\n  hosts: '
            hosts = eval(input("Please enter the host string or IP: "))
            gather_facts = eval(input("Do you want to gather facts? [Y/N]: "))

            while gather_facts not in ['Y','N','y','n']:
                gather_facts = eval(input("Please provide correct input for gather facts? [Y/N]: "))

            vars_in = eval(input("Do you want to define variables directly into Playbook ? [Y/N]:"))
            if vars_in == 'Y' or vars_in == 'y':
                var = self.get_vars_data()
            else:
                var = dict()

            self.final_playbook += hosts + '\n' + '  become: yes' + '\n' + '  become_user: root' + '\n'

            if gather_facts.lower() == 'y':
                if vars_in.lower() == 'y':
                    self.final_playbook += '  gather_facts: True' + '\n\n' + '  vars:\n'
                else:
                    self.final_playbook += '  gather_facts: True' + '\n\n'
            else:
                if vars_in.lower() == 'y':
                    self.final_playbook += '  gather_facts: False' + '\n\n' + '  vars:\n'
                else:
                    self.final_playbook += '  gather_facts: False' + '\n\n'

            if len(var) > 0:
                for key, values in list(var.items()):
                    self.final_playbook += '    ' + key + ': ' + str(values) + '\n'
            self.final_playbook += '\n  tasks:\n'

            # Listing the Parameters
            def get_attributes(mod_name):
                print(mod_name)
                my_resources = self.__my_db.resources
                info = my_resources.find({"module_name": mod_name})
                self.final_playbook += '  - name: ' + mod_name + '\n'
                for value in info:
                    self.final_playbook += '    ' + value['Parameter'] + ':'
                    if 'Required Flag' in value:
                        self.final_playbook += ' ' * (61 - len(value['Parameter'])) + '# * Required Field'
                        if 'Type' in value:
                            self.final_playbook += ' & Type = ' + value['Type'] + '\n'
                    else:
                        self.final_playbook += ' ' * (61 - len(value['Parameter'])) + '# Type = ' + value[
                            'Type'] + '\n'

                self.final_playbook += '\n'

            def database():
                # Database call

                user_input = eval(input("Please enter the search keyword for Module:"))
                my_collection = self.__my_db.modules
                # user_input = re.compile('/' + user_input + '/')
                # user_input = '/' + user_input + '/'
                # cnt = my_collection.find({"module_name": {'$regex': user_input}}).count()
                result = list()
                for module in my_collection.find({'module_name': {'$regex': user_input}}):
                    result.append(module)
                # print(result)
                if len(result) == 0:
                    print("Search string not available in the Module index!")
                    database()
                else:
                    for j in range(1, len(result)):
                        print(str(j) + '. ' + result[j-1]['module_name'] + '\n' + '     - ' + result[j-1]['synopsis'])

                return result

            def excepting(result):
                row_num = int(eval(input("\nPlease select a module number from above: Ex: 12 :")))
                try:
                    print('\nYou have chosen the Ansible Module "' + str(result[row_num - 1]['module_name'])
                          + '"')
                    print("Description:", result[row_num - 1]['synopsis'])
                    return result[row_num - 1]['module_name']
                except IndexError:
                    print("\nError - Please enter number within the available limit!!! \n")
                    excepting(result)

            result = database()
            module_name = excepting(result)
            get_attributes(module_name)

            decision = eval(input("Do you want to continue: [Y/N]"))
            while decision.lower() == 'y':
                result = database()
                module_name = excepting(result)
                get_attributes(module_name)
                decision = eval(input("Do you want to continue: [Y/N]"))
                if decision.lower() != 'y' and decision.lower() != 'n':
                    print("Sorry wrong choice")

            self.final_playbook += '\n...'
            with open(self.file_path, "w+") as file:
                file.write(self.final_playbook)

            print("Please find the Playbook in", self.file_path)

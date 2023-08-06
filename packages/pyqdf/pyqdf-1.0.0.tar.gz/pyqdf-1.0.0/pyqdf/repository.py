# ***** BEGIN GPL LICENSE BLOCK *****
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   The Original Code is Copyright (C) 2019, Paralelo Consultoria e Servicos Ltda
#   All rights reserved.
# ***** END GPL LICENSE BLOCK *****

from .container import Container
from .qvs import Qvs
import os
import re

class Repository():

    repository = '1.QVD'

    def __init__(self, path):
        self.path = path        
         
    # def is_valid_repository(self):
    #     return len(self.container_name.split('.')) > 0 if False else True
    
    @staticmethod
    def has_deep_path(path):
        if(os.path.isdir(path)):
            list_repo = ' ; '.join(os.listdir(path))
            if(re.search('1.QVD', list_repo)):
                return False
            else:
                return True

    @staticmethod
    def get_container_deep(self, path):
        deep_list = []
        deep_dict = []
        containers_list = os.listdir(path)
        for container_item in containers_list:           
            container_path = path + '\\' + container_item
            container = Container(container_path, self.path)
            
            if(container.is_valid_container()):
                if(container.is_container_exception() == False):
                    if(container.is_container_repository() == True):
                        deep_dict.append(container.container_fullpath)
                        deep_list.append(deep_dict)
                    else:
                        if(self.has_deep_path(container.container_fullpath)):
                            deep_list.append(self.get_container_deep(self, container.container_fullpath))
        return deep_list


    def get_list_of_containers(self):
        dict_of_containers = self.get_container_deep(self, self.path)
        list_containers = []

        def remove_nested (items):
            for item in items:
                if(type(item) == list):
                    remove_nested(item)
                else:
                    list_containers.append(item)

        remove_nested(dict_of_containers)
        
        return list(dict.fromkeys(list_containers))

    #Função que entra nos containers e busca os metadados e retorna uma lista de dicionários.
    @staticmethod
    def get_scripts_context(repository_path, list_of_containers):
        scripts = []

        for item in list_of_containers:
            container = Container(item, repository_path)
            script_list = []
            container_dict = {}
            if (container.is_container_exception() == False):
                if(container.is_container_repository()):
                    container_dict['path'] = container.get_container_path()
                    container_dict['container'] = container.container_name
                    container_dict['container_prefix'] = container.get_container_prefix()
                    custom_scripts = container.get_files(container.get_custom_path())

                    for script in custom_scripts:
                        script_context = {}
                        #Cria instancia do script QVS
                        qvsfile = Qvs(container.get_custom_path(),script)
                        
                        #Verifica se o arquivo é um QVS
                        if(qvsfile.is_qvs()):
                            script_context = qvsfile.get_script_context()
                            script_list.append(script_context)
                    container_dict['qvs_files'] = script_list
                scripts.append(container_dict)
        return scripts
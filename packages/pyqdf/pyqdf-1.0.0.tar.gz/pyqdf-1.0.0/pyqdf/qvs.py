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

import re
import os

class Qvs():

    body=None
    body_lower=None
    body_lower_nospace=None

    def __init__(self, path=os.getcwd(), qvs='', **kwargs):
        self.body = open(path + '/' + qvs,'r', encoding='windows-1252').read()
        self.filename = qvs
        self.path = path
        self.body_lower = self.body.lower()
        self.body_lower_nospace =  re.sub(r"[\n\t\s]*", "", self.body_lower)
        self.body_lower_with_space =  re.sub(r"[\n]*", "", self.body_lower).replace('\t',' ')

        for key, value in kwargs.items():
            setattr(self, key, value)

    def mappings(self):
        return re.findall('mappingload', self.body_lower_nospace)

    def get_body(self):
        return self.body

    def get_body_lower(self):
        return self.body_lower
    
    def get_body_lower_nospace(self):
        return self.body_lower_nospace

    def is_qvs(self):
        return len(re.findall('.qvs', self.filename)) > 0 if True else False

    def has_include_commented(self):
        has = []

        has.append(re.findall("[/][/][$][(]must_include=.*?.qvs", self.body_lower_nospace))
        has.append(re.findall("[/][*][$][(]must_include=.*?.qvs", self.body_lower_nospace))
        has.append(re.findall("[/][/][$][(]include=.*?.qvs", self.body_lower_nospace))
        has.append(re.findall("[/][*][$][(]include=.*?.qvs", self.body_lower_nospace))
       
        #cleaning the list
        tscores = [x for x in has if x != []]

        return len(tscores) > 0 if True else False


    def has_call_commented(self):
        has = []
        has.append(re.findall("[/][/]call.*", self.body_lower_nospace))
        has.append(re.findall("[/][*]call.*?[*][/]", self.body_lower_nospace))

        #cleaning the list
        tscores = [x for x in has if x != []]

        return len(tscores) > 0 if True else False

    def has_exit_script(self):
        return len(re.findall(r'(?<![/][/])exitscript', self.body_lower_nospace)) > 0 if True else False


    def has_store_into(self):
        return len(re.findall(r'store.* into.*[(].*qvd[)]', self.body_lower_nospace)) > 0 if True else False


    def how_many_mappings(self):
        return len(re.findall("mappingload", self.body_lower_nospace))

    def how_many_froms(self):
        return len(re.findall("from", self.body_lower_nospace))

    def how_many_residents(self):
        return len(re.findall("resident", self.body_lower_nospace))

    def how_many_inlines(self):
        return len(re.findall("inline", self.body_lower_nospace))

    def how_many_droptables(self):
        return len(re.findall("droptable.*?;", self.body_lower_nospace))

    def get_table_names(self):
        return re.findall(r'(?=\S)\D\w.*?:', self.body_lower)

    #Função que adiciona [] nos caracteres especiais no momento de pesquisar o nome da tabela.
    @staticmethod
    def get_search_term(term):
        term = re.sub(r"[(]", "[(]", term)
        term = re.sub(r"[)]", "[)]", term)
        term = re.sub(r"[$]", "[$]", term)
        term = re.sub(r"[']", "[']", term)
        term = re.sub(r"[[]", "", term)
        term = re.sub(r"[]]", "[]]", term)
        return term

    #Função que cria um dicionário com todas as informações dentro do script.
    def get_script_context(self):
        tables_name = self.get_table_names()

        script = {}
        script['qvs'] = self.filename

        table_list = []
        
        id_tables = 1 
        index = 1
        #Para cada tabela no script, é criado um dicionário com informações dessa tabela.
        for table_name in tables_name:
            script_context = {}
            script_context['id'] = id_tables  
            #Define os termos de pesquisa
            search_term = self.get_search_term(table_name)
            search_table = r"(?<={}).*?[;]".format(search_term)
            search_term_concat = search_term.replace(':','')
            search_concatenate_1 = r"(?<=concatenate[(]{}[)]).*?[;]".format(search_term_concat)
            search_concatenate_2 = r"(?<=concatenate [(]{}[)]).*?[;]".format(search_term_concat)
            search_join_1 = r"(?<=join[(]{}[)]).*?[;]".format(search_term_concat)
            search_join_2 = r"(?<=join [(]{}[)]).*?[;]".format(search_term_concat)

            #Cria dicionário
            script_context['table_name'] = table_name.replace(':','')
            script_context['search_term'] = search_term
            script_context['regex_search_term'] = search_table
            
            # Uni todos os loads envolvidos na criação da tabela.
            load_scripts = ' '.join(re.findall(search_table, self.body_lower_with_space))
            concatenate_scripts = ' '.join(re.findall(search_concatenate_1, self.body_lower_with_space)) + ' '.join(re.findall(search_concatenate_2, self.body_lower_with_space))
            join_scripts = ' '.join(re.findall(search_join_1, self.body_lower_with_space)) + ' '.join(re.findall(search_join_2, self.body_lower_with_space))
                
            # Uni os scripts
            scripts = load_scripts + concatenate_scripts + join_scripts
            script_context.update({'script': scripts})
            froms = re.findall(r'(?<=from).*?;', scripts)
            froms_list = []

            
            # Recupera todos os Loads que foram pelo from
            for _from in froms:
                from_dict = {}
                from_dict.update({'id': index})
                has_extension =  False
                where = _from.split('where')
                group = _from.split('group by')
                order = _from.split('order by')

                if(len(where) > 1):
                    #from_dict.update({'where': where[1]})
                    from_dict.update({'from': where[0]})
                    has_extension = True
                    
                if(len(group) > 1):
                    #from_dict.update({'group_by': group[1]})
                    if has_extension == False:
                        from_dict.update({'from': group[0]})
                        has_extension = True

                if(len(order) > 1):
                    #from_dict.update({'order_by': order[1]})
                    if has_extension == False:
                        from_dict.update({'from': order[0]})
                        has_extension = True
                
                if has_extension == False:
                        from_dict.update({'from': _from})
                froms_list.append(from_dict)
                index += 1
            # Recupera todos os Loads que foram pelo resident
            residents = re.findall(r'(?<=resident).*?;', scripts)
            for resident in residents:
                from_dict = {}
                from_dict.update({'id': index})
                has_extension =  False
                where = resident.split('where')
                group = resident.split('group by')
                order = resident.split('order by')

                if(len(where) > 1):
                    #from_dict.update({'where': where[1]})
                    from_dict.update({'resident': where[0]})
                    has_extension = True
                    
                if(len(group) > 1):
                    #from_dict.update({'group_by': group[1]})
                    if has_extension == False:
                        from_dict.update({'resident': group[0]})
                        has_extension = True

                if(len(order) > 1):
                    #from_dict.update({'order_by': order[1]})
                    if has_extension == False:
                        from_dict.update({'resident': order[0]})
                        has_extension = True
                
                if has_extension == False:
                        from_dict.update({'resident': resident})

                froms_list.append(from_dict)
                index += 1
            script_context.update({'froms': froms_list})
            id_tables += 1
            table_list.append(script_context)

        # Extracao Stage
        extracao_stages = re.findall(r"(?<=extracaostage[(][']).*?;", self.body_lower_nospace)
        for extracao_stage in extracao_stages:
            line = extracao_stage.split(',')
            script_context = {}
            froms_list = []
            script_context['id'] = id_tables  
            script_context['table_name'] = line[3]
            script_context.update({'script': str('extracaostage(') + extracao_stage})

            from_dict = {}
            from_dict.update({'id': index})
            from_dict.update({'from': str(line[2] + '.' + line[1])})
            
            froms_list.append(from_dict)
            index += 1
            script_context.update({'froms': froms_list})
            id_tables += 1
            table_list.append(script_context)
        
        script.update({'tables': table_list})

        return script

    def has_if_to_much_and(self):
        and_conditions = []
        if_and_conditions = re.findall(r'if[(].*?[)]as', self.body_lower_nospace)
        
        for item in if_and_conditions:
            and_condition = re.findall(r'and.*and.*and.*and.*', item)
            if(len(and_condition) > 0):
                and_conditions.append(and_condition)
        
        return len(and_conditions) > 0 if True else False

    def has_if_to_much_or(self):
        or_conditions=[]
        if_or_conditions = re.findall(r'if[(].*?[)]as', self.body_lower_nospace)

        for item in if_or_conditions:
            or_condition = re.findall(r'(?<!flo)or.*(?<!flo)or.*(?<!flo)or.*(?<!flo)or.*', item)
            if(len(or_condition) > 0):
                or_conditions.append(or_condition)

        return len(or_conditions) > 0 if True else False

    def has_nested_if(self):
        nested_if= re.findall(r'if[(].*,.*[)]{4,}.*', self.body_lower_nospace)

        return len(nested_if) > 0 if True else False
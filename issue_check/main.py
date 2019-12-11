#!/usr/bin/python
# coding: utf-8

"""
O que agente que fazer?

    Poder ter a capacidade de garantir que os novos conteúdo no SciELO Web form inseridos corretamente.

Como iremos fazer?

    Verificar no site os conteúdos a cada termino de processamento.

Iremos inicialmente utilizar programação estrutura em Python

Temos a scilista.lst como indicação das últimas alterações que precisam ser validadas.

Validação manual:
    Acessa o site web e verificar os novos facículos e artigos, pdfs, images e tabelas.
"""
import re
import requests
import pdb
from lxml import etree
import os
from pprint import pprint


REGEX_ISSN = r'[\S]{4}\-[\S]{4}'
PROTOCOL = 'http://'
DOMAIN = 'www.scielo.br'
URL_SEGMENT = 'scielo.php?script=%s&pid=%s&debug=xml'
SCRIPT_URL = {
                'grid': 'sci_issues',
                'toc': 'sci_issuetoc',
                'article': 'sci_arttext'
             }


if __name__ == "__main__":

    # Ler o arquivo do scilista.lst
    os_path = os.path.join(os.path.dirname(__file__), "scilista.lst")
    fp = open(os_path, 'r')

    issns = []  # Periódicos encontrados
    j_not_found = []  # Periódicos não encontrados
    revistas = []
    journal_list = []

    # Obtém os issns
    for line in fp.readlines():
        acron, issue_label = line.split()
        ret = requests.get("%s%s/%s" % (PROTOCOL, DOMAIN, acron))

        if ret.status_code == 200:
            issn = re.search(REGEX_ISSN, ret.url)
            issns.append(issn.group())
        else:
            j_not_found.append(acron)
            print('Acrônimos não encontrados:')
            print(j_not_found)

        current_dict = {'acron': acron}

        #dict_issue = {}

        # Verifica o fascículo na grade
        for issn in issns:
            url_segment = URL_SEGMENT % (SCRIPT_URL['grid'], issn)
            ret = requests.get("%s%s/%s" % (PROTOCOL, DOMAIN, url_segment))
            tree = etree.fromstring(ret.content)
            issues = tree.xpath("//AVAILISSUES")[0]
            
            #Dicionários usados nos laços para criaçao do dicionário principal
            ano_dic = {}
            vols_dic = {}
            num_dic = {}


            for year_issue in issues:
                if year_issue.values():
                    ano_dic["ano"] = year_issue.values()[0]
                    current_dict["year"] = [ano_dic]

                    for vols in year_issue:
                        vols_dic["vol"] = vols.values()[0]
                        ano_dic["volume"] = [vols_dic]
                        
                        num_list = []
                        for nums in vols:
                            
                            if nums.values():
                                
                                if len(nums.values()) > 2:
                                
                                    num_dic["num"] = nums.values()[0]
                                    num_dic["pid"] = nums.values()[2]
                                else:
                                    num_dic["pid"] = nums.values()[1]
                                    num_dic["num"] = 'null'
                            num_list.append(num_dic)
                        journal_list.append(num_list) 
                        pprint(journal_list)
                        pdb.set_trace()

                        vols_dic["issues"] = [num_dic]

                                
                              
                            

"""                               
            
            # YEARISSUE
            for year_issue in issues:
                # ANO
                    ano_dic = {}
                    
                    # VOLISSUE
                    for vol_issue in issue:
                        # Volume
                        
                        current_dict["ano"] = issue.values()[0]
                        current_dict["vol"] = vol_issue.values()[0]

                        #NUMS
                        for number in vol_issue:
                            


                            if number.values():
                                num = {}

                                if len(number.values()) > 2:
                                    num['num'] = number.values()[0]
                                    num['pid'] = number.values()[2]
                                else:
                                    num['pid'] = number.values()[1]
                            
                                    
                            num_list.append(num)

            current_dict['nums'] = num_list    

        journal_list.append(current_dict)

pprint(journal_list)
"""





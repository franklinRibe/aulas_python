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

    j_not_found = []  # Periódicos não encontrados
    journal_list = [] # Periódicos encontrados

    # Obtém os issns
    for line in fp.readlines():
        acron, issue_label = line.split()
        ret = requests.get("%s%s/%s" % (PROTOCOL, DOMAIN, acron))

        if ret.status_code == 200:
            issn = re.search(REGEX_ISSN, ret.url).group()
        else:
            j_not_found.append(acron)
            print('Acrônimos não encontrados:')
            print(j_not_found)

        # Verifica o fascículo na grade
        url_segment = URL_SEGMENT % (SCRIPT_URL['grid'], issn)
        ret = requests.get("%s%s/%s" % (PROTOCOL, DOMAIN, url_segment))
        tree = etree.fromstring(ret.content)
        issues = tree.xpath("//AVAILISSUES")[0]
        
        #Dicionários usados nos laços para criaçao do dicionário principal

        for year_issue in issues:
            current_dict = {}

            if year_issue.values():
                for vols in year_issue:
                    num_list = []
                    current_dict["acron"] = acron
                    current_dict["vol"] = vols.values()[0]
                    
                    for nums in vols:
                        if nums.values():
                            num_dic = {}
                            if len(nums.values()) > 2:
                                
                                num_dic["num"] = nums.values()[0]
                                num_dic["pid"] = nums.values()[2]      
                            else:
                                num_dic["num"] = 'Null'
                                num_dic["pid"] = nums.values()[1]

                            num_list.append(num_dic)
                            current_dict["numero"] = num_list
               
                journal_list.append(current_dict)
        pprint(journal_list)
        #print(journal_list[3]['pid'])
        pdb.set_trace()
        """
        Acessando as URLs baseadas nas listagens criadas
        
        pid = journal_list
        url_segment_toc = URL_SEGMENT % (SCRIPT_URL['toc'], pid)
        ret = requests.get("%s%s/%s" % (PROTOCOL, DOMAIN, url_segment_toc))
        """ 

        
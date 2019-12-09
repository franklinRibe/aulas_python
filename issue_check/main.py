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
    fp = open('/Users/franklin.ribeiro/Documents/aulas_python/issue_check/scilista.lst', 'r')

    issns = []  # Periódicos encontrados
    j_not_found = []  # Periódicos não encontrados
    dic_teste = [{}]

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
            

        # [
        #   {
        #   'ano': 2001, 'vol': 1,
        #   'nums': [
        #             {'number': 1, 'link': ''},
        #           ]
        #   }
        # ]

        #dic_teste = [{'acr':'%s','year':'%s','vol':['%s', '%s']}] 

        
        dic_teste.append(acron) 
        print(dic_teste)
        
  

        #dict_issue = {}

        # Verifica o fascículo na grade
        for issn in issns:
            url_segment = URL_SEGMENT % (SCRIPT_URL['grid'], issn)
            ret = requests.get("%s%s/%s" % (PROTOCOL, DOMAIN, url_segment))

            tree = etree.fromstring(ret.content)
            issues = tree.xpath("//AVAILISSUES")[0]

            # YEARISSUE
            
            for issue in issues:
                # ANO
                
                #print(issue.values())
        
                # VOLISSUE
                for vol_issue in issue:
                    # Volume
                    dic_teste.update({'year':issue.values()})
                    dic_teste.update({'vol':vol_issue.values()})
                
                    #for number in vol_issue:
                    #if number.values():
                    print(dic_teste)
                        
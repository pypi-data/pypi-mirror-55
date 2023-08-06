#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:20:52 2019

@author: whe3
"""

import json



domain_all = json.loads(open('Pfam_genome_dic').read())

print(domain_all['ZNF236'])
'''
domain_all['ZNF236'] = {'zf9': {'start': 285, 'end': 308}, 
                        'zf8': {'start': 253, 'end': 276}, 
                        'zf12': {'start': 538, 'end': 560}, 
                        'zf13': {'start': 566, 'end': 588}, 
                        'zf18': {'start': 967, 'end': 989},
                        'zf3': {'start': 93, 'end': 115},
                        'zf2': {'start': 66, 'end': 88}, 
                        'zf1': {'start': 37, 'end': 59}, 
                        'zf14': {'start': 657, 'end': 679}, 
                        'zf7': {'start': 225, 'end': 247}, 
                        'zf6': {'start': 197, 'end': 219}, 
                        'zf5': {'start': 153, 'end': 175}, 
                        'zf4': {'start': 121, 'end': 143}, 
                        'zf17': {'start': 741, 'end': 763}, 
                        'zf11': {'start': 510, 'end': 532}, 
                        'zf16': {'start': 713, 'end': 735},
                        'zf10': {'start': 482, 'end': 504}, 
                        'zf15': {'start': 685, 'end': 707},
                        'zf19': {'start': 995, 'end': 1017},
                        'zf20': {'start': 1023, 'end': 1045},
                        'zf21': {'start': 1051, 'end': 1073},
                        'zf22': {'start': 1167, 'end': 1189},
                        'zf23': {'start': 1195, 'end': 1217},
                        'zf24': {'start': 1223, 'end': 1245},
                        'zf25': {'start': 1251, 'end': 1273},
                        'zf26': {'start': 1657, 'end': 1680},
                        'zf27': {'start': 1686, 'end': 1708},
                        'zf28': {'start': 1722, 'end': 1744},
                        'zf29': {'start': 1750, 'end': 1772},
                        'zf30': {'start': 1778, 'end': 1801},
                        }

print(domain_all['ZNF236'])
f = open('Pfam_genome_dic','w')
data = json.dumps(domain_all)
f.write(data)
f.close()
'''
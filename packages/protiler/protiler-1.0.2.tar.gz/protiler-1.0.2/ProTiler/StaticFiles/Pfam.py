#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:18:56 2019

@author: whe3
"""
import json

pfam_dic = json.loads(open('Pfam_genome_dic').read())


pfam_dic['CTCF'] ={u'zf1': {u'end': 288, u'start':266},
 u'zf2': {u'end': 316, u'start': 294},
 u'zf3': {u'end': 345, u'start': 322},
 u'zf4': {u'end': 373, u'start': 351},
 u'zf5': {u'end': 401, u'start': 379},
 u'zf6': {u'end': 430, u'start': 407},
 u'zf7': {u'end': 460, u'start': 437},
 u'zf8': {u'end': 489, u'start': 467},
 u'zf9': {u'end': 517, u'start': 495},
 u'zf10': {u'end':546, u'start': 523},
 u'zf11': {u'end': 575, u'start': 555}
 }

pfam_dic['TCF7L2'] = {'CTNNB1_binding':{'start':1,'end':259},
                      'HMG_box':{'start':349,'end':419}}

pfam_dic['CDC5L'] = {'Myb_domain1':{'start':1,'end':58},
                      'Myb_domain2':{'start':59,'end':108},
                      'Myb_Cef':{'start':404,'end':655}}

pfam_dic['ZNF236'] = {u'zf1': {u'start': 37, u'end':59},
 u'zf2': {u'start': 94, u'end': 115},
 u'zf3': {u'start': 153, u'end': 175},
 u'zf4': {u'start': 197, u'end': 219},
 u'zf5': {u'start': 225, u'end': 247},
 u'zf6': {u'start': 284, u'end': 310},
 u'zf7': {u'start': 482, u'end': 504},
 u'zf8': {u'start': 510, u'end': 532},
 u'zf9': {u'start': 685, u'end': 707},
 u'zf10': {u'start':967, u'end': 989},
 u'zf11': {u'start': 995, u'end':1017},
 u'zf12': {u'start': 1023, u'end': 1045},
 u'zf13': {u'start': 1168, u'end': 1189},
 u'zf14': {u'start': 1223, u'end': 1245},
 u'zf15': {u'start': 1688, u'end': 1708},
 u'zf16': {u'start':1722, u'end': 1744},
 u'zf17': {u'start': 1750, u'end':1772},
 u'zf18': {u'start': 1778, u'end':1801}
 }

pfam_dic['ZNF335'] = {u'zf1': {u'start': 245, u'end':268},
 u'zf2': {u'start': 465, u'end': 492},
 u'zf3': {u'start': 495, u'end': 522},
 u'zf4': {u'start': 523, u'end': 550},
 u'zf5': {u'start': 562, u'end': 589},
 u'zf6': {u'start': 590, u'end': 612},
 u'zf7': {u'start': 621, u'end': 648},
 u'zf8': {u'start': 649, u'end': 677},
 u'zf9': {u'start': 678, u'end': 706},
 u'zf10': {u'start':1019, u'end':1046},
 u'zf11': {u'start': 1047, u'end':1074},
 u'zf12': {u'start': 1075, u'end':1102},
 u'zf13': {u'start': 1103, u'end':1131}}


pfam_dic['E4F1'] = {u'zf1': {u'start': 192, u'end':214},
 u'zf2': {u'start': 220, u'end': 242},
 u'zf3': {u'start': 248, u'end': 272},
 u'zf4': {u'start': 435, u'end': 457},
 u'zf5': {u'start': 463, u'end': 485},
 u'zf6': {u'start': 491, u'end': 513},
 u'zf7': {u'start': 519, u'end': 541},
 u'zf8': {u'start': 547, u'end': 569},
 u'zf9': {u'start': 575, u'end': 597}}


pfam_dic['PRDM10'] = {u'zf1': {u'start': 355, u'end':377},
 u'zf2': {u'start': 530, u'end': 552},
 u'zf3': {u'start': 560, u'end': 582},
 u'zf4': {u'start': 588, u'end': 610},
 u'zf5': {u'start': 616, u'end': 639},
 u'zf6': {u'start': 644, u'end': 666},
 u'zf7': {u'start': 672, u'end': 695},
 u'zf8': {u'start': 727, u'end': 750},
 u'zf9': {u'start': 772, u'end': 795},
 'SET':{'start':208,'end':326}}


pfam_dic['ZBTB17'] = {u'zf1': {u'start': 306, u'end':328},
 u'zf2': {u'start': 334, u'end': 356},
 u'zf3': {u'start': 362, u'end': 384},
 u'zf4': {u'start': 390, u'end': 412},
 u'zf5': {u'start': 418, u'end': 440},
 u'zf6': {u'start': 446, u'end': 468},
 u'zf7': {u'start': 474, u'end': 496},
 u'zf8': {u'start': 502, u'end': 524},
 u'zf9': {u'start': 530, u'end': 552},
 u'zf10': {u'start':558, u'end':580},
 u'zf11': {u'start': 586, u'end':608},
 u'zf12': {u'start': 614, u'end':637},
 u'zf13': {u'start': 717, u'end':739},
 'BTB':{'start':1,'end':104}}


pfam_dic['ZBTB11'] = {u'zf1': {u'start': 569, u'end':591},
 u'zf2': {u'start': 597, u'end': 619},
 u'zf3': {u'start': 651, u'end': 673},
 u'zf4': {u'start': 679, u'end': 701},
 u'zf5': {u'start': 707, u'end': 729},
 u'zf6': {u'start': 735, u'end': 757},
 u'zf7': {u'start': 766, u'end': 788},
 u'zf8': {u'start': 794, u'end': 816},
 u'zf9': {u'start': 822, u'end': 846},
 u'zf10': {u'start':858, u'end':880},
 u'zf11': {u'start': 886, u'end':908},
 u'zf12': {u'start': 914, u'end':937},
 'BTB':{'start':214,'end':282}}


data = json.dumps(pfam_dic)
f = open('Pfam_genome_dic','w')
f.write(data)
f.close()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tabletree.tabletree import TableTree, TableNode, TableLink
import pandas as pd

__author__ = "Xi Rossi LUO"
__copyright__ = "Xi Rossi LUO"
__license__ = "mit"


def test():
        tab1_list = list( zip([1,2,3,4], ['M', 'F', 'M', 'F'] ) )
        tab2_list = list( zip(  [1,2,3,4], ['red', 'green', 'yellow', 'blue'] ) )
        tab3_list = list( zip(  [1,2,3,4], [' ', ' ', ' ', ''] ) )
        tab1 = pd.DataFrame( tab1_list,   columns = ['tab1_v1', 'tab1_v2'])
        tab2 = pd.DataFrame( tab2_list,   columns = ['tab2_v1', 'tab2_v2'])
        tn1 = TableNode('sex', tab1)
        tn2 = TableNode('preference', tab2)
        ttree = TableTree(tn1)
        ttree.addChildren(tn2, TableLink('tab1_v1', 'tab2_v1'))
        assert all( [ a == b for a, b in zip(ttree.getAncestors('preference'), ['sex'] )  ] ), "getAncestors: wrong returns!"
        df = ttree.findMatched('preference', 'sex', tn1.df.tab1_v2 == 'M')
        df_exp = pd.DataFrame(list(zip([1,3], ['red', 'yellow'])),columns = ['tab2_v1', 'tab2_v2'] )
        df = df.reset_index(drop= True)
        assert  df.equals(df_exp), "findMatched: two DFs don't match!"

def test_4node():
        tab1_list = list( zip([1,2,3,4], ['M', 'F', 'M', 'F'] ) )
        tab2_list = list( zip(  [1,2,3,4], ['red', 'green', 'yellow', 'blue'] ) )
        tab3_list = list( zip(  ['red', 'green', 'yellow', 'blue'], ['apple', 'grape', 'banana', 'berry'] ) )
        tab4_list = list( zip(  [1,2,3,4], ['swimming', 'football', 'piano', 'painting'] ) )
        tab1 = pd.DataFrame( tab1_list,   columns = ['tab1_v1', 'tab1_v2'])
        tab2 = pd.DataFrame( tab2_list,   columns = ['tab2_v1', 'tab2_v2'])
        tab3 = pd.DataFrame( tab3_list,   columns = ['tab3_v1', 'tab3_v2'])
        tab4 = pd.DataFrame( tab4_list,   columns = ['tab4_v1', 'tab4_v2'])
        tn1 = TableNode('sex', tab1)
        tn2 = TableNode('preference', tab2)
        tn3 = TableNode('fruit', tab3)
        tn4 = TableNode('hobby', tab4)
        ttree = TableTree(tn1)
        ttree.addChildren(tn2, TableLink('tab1_v1', 'tab2_v1'))
        ttree.addChildren(tn3, TableLink('tab2_v2', 'tab3_v1'))
        ttree.addTN('sex', tn4, TableLink('tab1_v1', 'tab4_v1'))
        print(ttree.getAncestors('hobby'))
        ttree.findMatched('fruit', 'sex', tn1.df.tab1_v2 == 'M')
        print( ttree.findMatched('hobby', 'sex', tn1.df.tab1_v2 == 'M') )
        print(ttree)
        ttree.search_children(ttree.getTN('sex'), 'hobby')
        ttree.search_children( 'sex', 'hobby')
        ttree.getTN('fruit')
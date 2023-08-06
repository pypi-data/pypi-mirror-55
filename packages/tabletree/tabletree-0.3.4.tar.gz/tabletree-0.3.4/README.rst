=========
tabletree
=========


Python package for exploring and linking multiple SQL-like tables

Description
===========

This package will link multiple SQL-tables together to facilitate (potentially large-scale) analysis of data from various sources. All tables are implemented using Pandas Data.Frame objects.


Examples
========

In the following example, 3 tables are linked together via different columns and different data types. They form a tree: sex -> preference -> fruit.  This package  enables finding  the favoriate fruits for 'M' ids by transversing this table tree automatically. 

.. code-block:: python


    from tabletree import TableNode, TableTree, TableLink
    import pandas as pd

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
    #['sex', 'hobby']
    ttree.findMatched('fruit', 'sex', tn1.df.tab1_v2 == 'M')
    print( ttree.findMatched('hobby', 'sex', tn1.df.tab1_v2 == 'M') )
    #tab4_v1   tab4_v2
    #1         swimming
    #3         piano
    print(ttree)
    #['sex', [['preference', [['fruit']]], ['hobby']]]


Note
====

Github: https://github.com/rluo/tabletree

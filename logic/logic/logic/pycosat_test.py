# pycosat_test.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import pycosat
from typing import Dict, List, Tuple, Callable, Generator, Any
import util
import sys
import logic
import game

from logic import conjoin, disjoin
from logic import PropSymbolExpr, Expr, to_cnf, pycoSAT, parseExpr, pl_true
from logicPlan import *
print(findModel(sentence1()))
import itertools
import copy
cnf = [[1, -5, 4], [-1, 5, 3, 4], [-3, -4]]
a = Expr('A')
class dummyClass:
        """dummy('A') has representation A, unlike a string 'A' that has repr 'A'.
        Of note: Expr('Name') has representation Name, not 'Name'.
        """

        def __init__(self, variable_name: str):
            self.variable_name = variable_name

        def __repr__(self):
            return self.variable_name

print({'a': True},{dummyClass("a"): True})
"*** BEGIN YOUR CODE HERE ***"
print("a.__dict__ is:", a.__dict__)
print(pycosat.solve(cnf))
print(PropSymbolExpr('Kl'))

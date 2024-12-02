# factorOperations.py
# -------------------
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

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))

    
    #Factor.getAllPossibleAssignmentDicts:获取一个因子所有可能的变量赋值组合
    #Factor.getProbability:获取指定赋值组合的概率
    #Factor.setProbability为指定的赋值组合设置一个新的概率
    #Factor.unconditionedVariables返回因子的无条件变量集合
    #Factor.conditionedVariables返回因子的有条件变量集合
    #Factor.variableDomainsDict返回因子的变量域字典，描述每个变量可能的取值。
    #步骤:确定无条件变量和条件变量->合并->确定变量域->计算联合概率(相乘即可)
    setsOfConditioned=[set(factor.conditionedVariables())for factor in factors]
    Unconditioned_var=set().union(*setsOfUnconditioned)
    Conditioned_var=set().union(*setsOfConditioned)
    Conditioned_var -= Unconditioned_var#集合操作
    # set_unconditioned=frozenset(frozenset(setsOfUnconditioned))
    # setsOfConditioned=[x for x in setsOfConditioned if x not in set_unconditioned]
    domains={}
    for x in factors:
        domains.update(x.variableDomainsDict())#每一个变量可能的取值(重复怎么办?应该不用担心,因为更新的时候会自动屏蔽掉重复的变量)
    #构建一个新的factor
    new_factor=Factor(Unconditioned_var,Conditioned_var,domains)
    all_possible_assignments=new_factor.getAllPossibleAssignmentDicts()
    for i in all_possible_assignments:#对于每一个可能的变量赋值组合
        jp=1.0#设置联合概率值(对于当前组合的联合概率)
        for j in factors:
            factor_vars = set(j.unconditionedVariables()) | set(j.conditionedVariables())#所有变量合并,存在就加进来
            filters={k:v for k,v in i.items() if k in factor_vars}#i.item()返回所有键值对
            jp*=j.getProbability(filters)#联合概率=每个因子在当前组合下的概率

        new_factor.setProbability(i,jp)
    return new_factor
    "*** YOUR CODE HERE ***"
    raiseNotDefined()   
    "*** END YOUR CODE HERE ***"

########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))
        #print(f"factor variables: {factor.unconditionedVariables()} {factor.conditionedVariables()}")
        #print(f"elimination variables: {eliminationVariable}")
        #print(f"Current assignment of factor: {factor.getAllPossibleAssignmentDicts()}")
        setsOfUnconditioned = [set(factor.unconditionedVariables())]
        setsOfConditioned=[set(factor.conditionedVariables())]
        Unconditioned_var=set().union(*setsOfUnconditioned)
        Conditioned_var=set().union(*setsOfConditioned)
        setsOfremoved = [set([eliminationVariable])]
        removed_var=set().union(*setsOfremoved)
        #print(removed_var)
        Conditioned_var -= removed_var#集合操作
        Unconditioned_var -= removed_var
        domains={}
        domains2={}
        domains.update(factor.variableDomainsDict())
        domains2.update(factor.variableDomainsDict())
        #print(domains)
        del domains[eliminationVariable]
        #print(domains) #已经得到了新的newfactor,现在要让它的概率值符合删除后的值
        #print(f"factor variables: {factor.unconditionedVariables()} {factor.conditionedVariables()}")
        #print(f"this: {Unconditioned_var} {Conditioned_var}")
        new_factor=Factor(Unconditioned_var,Conditioned_var,domains)
        #print('er')
        all_possible_assignments=new_factor.getAllPossibleAssignmentDicts()
        #print(f"new_factor variables: {new_factor.unconditionedVariables()} {new_factor.conditionedVariables()}")
        for i in all_possible_assignments:#对于每一个可能的变量赋值组合
            jp=0.0#设置联合概率值(对于当前组合的联合概率)
            #这和第二题相乘的逻辑不一样,应要对于eliminationvariable的每一个取值,去计算当前这个赋值组合的概率情况并将其相加
            factor_vars = set(new_factor.unconditionedVariables()) | set(new_factor.conditionedVariables())#所有变量合并,存在就加进来
            filters={k:v for k,v in i.items()if k in factor_vars}#i.item()返回所有键值对
            #print('error')
            for value in domains2[eliminationVariable]:
                fake_filters=filters.copy()
                fake_filters[eliminationVariable]=value
                jp+=factor.getProbability(fake_filters)
            
            #print(f"new_factor variables: {new_factor.unconditionedVariables()} {new_factor.conditionedVariables()}")
            #print(f"Filters being passed: {filters}")
            #print(f"Current assignment: {i}")
            #联合概率=每个因子在当前组合下的概率
            

            new_factor.setProbability(i,jp)
        return new_factor
        "*** YOUR CODE HERE ***"
        raiseNotDefined()
        "*** END YOUR CODE HERE ***"

    return eliminate

eliminate = eliminateWithCallTracking()


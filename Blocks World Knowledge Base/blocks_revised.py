import facts_and_rules,read

def Assert(fact):
    temp_KB=[]
    for f in KB:
        temp_KB.append(f.full)
    if fact.full not in temp_KB:
        KB.append(fact)
        infer_from_fact(fact)

def Assert_Rule(rule):
    temp_RB=[]
    for r in RB:
        temp_RB.append(r.full)
    if rule.full not in temp_RB:
        RB.append(rule)
        infer_from_rule(rule)

def infer_from_fact(fact):
    for r in RB:
        bindings=facts_and_rules.match(r.lhs[0],fact)
        if bindings!=False:
            if (r.type == "Assert"):
                if len(r.lhs)==1:
                    new_statement= facts_and_rules.statement(facts_and_rules.instantiate(r.rhs.full,bindings))
                    fact.add_fact(new_statement)
                    r.add_rule(new_statement)
                    Assert(new_statement)
                else:
                    tests=map(lambda x:facts_and_rules.instantiate(x.full,bindings),r.lhs[1:])
                    rhs=facts_and_rules.instantiate(r.rhs.full,bindings)
                    new_rule=facts_and_rules.rule(tests,rhs)
                    r.add_rule(new_rule)
                    fact.add_rule(new_rule)
                    Assert_Rule(new_rule)
            if (r.type == "Retract"):
                new_statement = facts_and_rules.statement(facts_and_rules.instantiate(r.rhs.full, bindings))
                fact.add_fact(new_statement)
                for ff in fact.facts:
                    delete(ff)
                for rr in fact.rules:
                    delete(rr)




def infer_from_rule(rule):
    for f in KB:
        bindings=facts_and_rules.match(rule.lhs[0],f)
        if bindings!=False:
            if (rule.type == "Assert"):
                if len(rule.lhs)==1:
                    new_statement = facts_and_rules.statement(facts_and_rules.instantiate(rule.rhs.full, bindings))
                    rule.add_fact(new_statement)
                    f.add_fact(new_statement)
                    Assert(new_statement)
                else:
                    tests=map(lambda x:facts_and_rules.instantiate(x.full,bindings),rule.lhs[1:])
                    rhs=facts_and_rules.instantiate(rule.rhs.full,bindings)
                    new_rule=facts_and_rules.rule(tests,rhs)
                    rule.add_rule(new_rule)
                    f.add_rule(new_rule)
                    Assert_Rule(new_rule)

            if (rule.type == "Retract"):
                new_statement = facts_and_rules.statement(facts_and_rules.instantiate(rule.rhs.full, bindings))
                f.add_fact(new_statement)
                for ff in f.facts:
                    delete(ff)
                for rr in f.rules:
                    delete(rr)


def delete(factorrule):
    temp=[]
    for fact_temp in KB:
        if factorrule.full==fact_temp.full:
            print 'delete the fact: '+fact_temp.pretty()
            temp.append(fact_temp)
            KB.remove(fact_temp)
    for rule_temp in RB:
        if rule_temp.full==factorrule.full:
            print 'delete the rule: '+rule_temp.pretty()
            temp.append(rule_temp)
            RB.remove(rule_temp)

    for insf in temp:
        for s in insf.facts:
            print 'Relevant facts(support): '+ s.pretty()
            delete(s)
    for insr in temp:
        for s in insr.rules:
            print 'Relevant rules(support): '+ s.pretty()
            delete(s)
    return



def Ask(pattern,flag):
    result=[]
    list_of_bindings_lists=[]
    for fact in KB:
        bindings=facts_and_rules.match(facts_and_rules.statement(pattern),fact)
        if bindings!=False and not(bindings in list_of_bindings_lists):
            list_of_bindings_lists.append(bindings)
            if(flag==1):
                print "Asking "+ facts_and_rules.statement(pattern).pretty()
                print "This is true: \t",
                print facts_and_rules.statement(facts_and_rules.instantiate(pattern,bindings)).pretty()
            result.append(facts_and_rules.statement(facts_and_rules.instantiate(pattern,bindings)))
    if len(list_of_bindings_lists)==0:
        if(flag==1):
            print 'No matching solutions \n'
    return result


def Retract(pattern):
    fact=facts_and_rules.statement(pattern)
    delete(fact)

    
def big_Ask(patterns):
    bindings_lists=[]
    for pattern in patterns:
        if bindings_lists !=[]:
            for pair in map(lambda b:(facts_and_rules.instantiate(pattern,b),b),bindings_lists):
                for fact in KB:
                    bindings=facts_and_rules.match(facts_and_rules.statement(pair[0]),fact)
                    if bindings !=False:
                        for key in pair[1]:
                            bindings[key]=pair[1][key]
                        bindings_lists.append(bindings)
        else:
            for fact in KB:
                bindings=facts_and_rules.match(facts_and_rules.statement(pattern),fact)
                if bindings !=False:
                    bindings_lists.append(bindings)

    a={}
    for bi in bindings_lists:
        if bindings_lists.count(bi)>1:
            a[bi.get(key)]=bindings_lists.count(bi)

    bindings_lists_new=[]
    for ai in a:
        temp={}
        temp[key]=ai
        bindings_lists_new.append(temp)

    for b in bindings_lists_new:
        print 'This is True: '
        for pattern in patterns:
            print facts_and_rules.statement(facts_and_rules.instantiate(pattern,b)).pretty()
    if len(bindings_lists_new) == 0:
        print 'No matching solutions \n'



if __name__ == "__main__":
    
    
    global KB
    global RB
    KB=[]
    RB=[]
    

    facts,rules=read.read_tokenize("statements.txt")
    
    for fact in facts:
        Assert(facts_and_rules.statement(fact))
    for new_rule in rules:
        Assert_Rule(facts_and_rules.rule(new_rule[0],new_rule[1]))
    
    print '\n*******************************Knowledge Base*******************************************\n'
    for kb in KB:
        print 'facts: '+facts_and_rules.statement.pretty(kb)
    print '\n*******************************Rules Base*******************************************\n'
    for rb in RB:
        print facts_and_rules.rule.pretty(rb)     
    
    print '\n******************************* Ask *******************************************\n'    
    result1=Ask(['color','pyramid1','?x'],1)
    Ask(['size','littlebox','?x'],1)
    result3=Ask(['color','?x','green'],1)
    
    print '\n*******************************Big Ask*******************************************\n'
    result4=big_Ask([['inst', '?x', 'pyramid'],['color', '?x', 'green']])
    
    print '\n******************************* Retract *******************************************\n'    
    Retract(['isa','cube','block'])
    
    
    print '\n******************************* Knowledge Base After Retract *******************************************\n'  
    for ele in KB:
        print ele.pretty()
        
#coding: UTF-8

# ===========================================================================
# CaseMachine (prototype for iteration 02 of inSitu)
# ---------------------------------------------------------------------------
# (c) 2015 Markus Hillebrand, Dipl.Inf.(FH) - www.markus-hillebrand.de
# Markus Hillebrand, Amalienstr. 71, 80799 München, Germany
# See LICENSE for more copyright details.
# ===========================================================================


class BasicCase:
    def __init__(self, stateInitial=False, onEnter=None, onEvery=None, onLeave=None, name=None, debug=False):
        self.state=stateInitial
        if onEnter!=None:
            self.onEnter=onEnter
        if onEvery!=None:
            self.onEvery=onEvery
        if onLeave!=None:
            self.onLeave=onLeave
        if name!=None:
            self._name=name
        if debug is True:
            self._debug=debug
        self.eventLast=None
        
    @property
    def name(self):
        try:
            return self._name
        except AttributeError:
            return "%s[%s]" % (self.__class__.__name__, id(self))
        
    @property
    def debug(self):
        try:
            return self._debug
        except AttributeError:
            return False
        
    def __and__(self, other):
        return ComplexCase_And(self, other)
    
    def __or__(self, other):
        return ComplexCase_Or(self, other)
    
    def __xor__(self, other):
        return ComplexCase_Xor(self, other)
    
    def __invert__(self):
        return ComplexCase_Not(self)

    def __bool__(self):
        return self.state
    
    def __eq__(self, other):
        return self.state==other.state

    def handleEvent(self, eventCurrent):
        try:
            if self.eventLast is eventCurrent:
                pass
            else:        
                stateNew=self.evaluate(eventCurrent.value)
                if not self.state and stateNew:
                    self.state=stateNew
                    self.onEnter(eventCurrent)
                elif self.state and not stateNew:
                    self.state=stateNew
                    self.onLeave(eventCurrent)
        finally:
            self.eventLast=eventCurrent
    
    def onEnter(self, eventCurrent):
        if self.debug:
            print("%s %s::onEnter [%s=>%s]" % (self.__class__.__name__, self.name, eventCurrent.nameValue, eventCurrent.value))
    
    def onEveryFunction(self, eventCurrent):
        if self.debug:
            print("%s %s::onEvery [%s=>%s]" % (self.__class__.__name__, self.name, eventCurrent.nameValue, eventCurrent.value))
    
    def onLeave(self, eventCurrent):
        if self.debug:
            print("%s %s::onLeave [%s=>%s]" % (self.__class__.__name__, self.name, eventCurrent.nameValue, eventCurrent.value))

class Case(BasicCase):
    def __init__(self, expr, **kwargs):
        self.expr=expr
        super().__init__(**kwargs)
        self.dependencies=self.expr.dependencies
        self.evaluate=self.expr.evaluate
                
    def handleEvent(self, eventCurrent):
        self.expr.handleEvent(eventCurrent)
        super().handleEvent(eventCurrent)
                        
class ValueCase(BasicCase):
    def __init__(self, nameValue, funcEval, **kwargs):
        super().__init__(**kwargs)
        self.nameValue=nameValue
        self.evaluate=funcEval
        
    @property
    def dependencies(self):
        yield self.nameValue
        
    def handleEvent(self, eventCurrent):
        assert eventCurrent.nameValue==self.nameValue
        return super().handleEvent(eventCurrent)
        
class ComplexCase(BasicCase):
    def __init__(self, cases, **kwargs):
        super().__init__(**kwargs)
        self.cases=cases

    @property
    def dependencies(self):
        for case in self.cases:
            yield from case.dependencies
        
    def handleEvent(self, eventCurrent):
        for c in self.cases:
            if eventCurrent.nameValue in c.dependencies:
                c.handleEvent(eventCurrent)
        return super().handleEvent(eventCurrent)

class ComplexCase_And(ComplexCase):
    def __init__(self, *cases, **kwargs):
        assert len(cases)>0, "should have minimum of one given case"
        casesOpt=[]
        for case in cases:
            if isinstance(case, ComplexCase_And):
                casesOpt.extend(case.cases)
            else:
                casesOpt.append(case)
        super().__init__(casesOpt, stateInitial=all(map(lambda c: c.state, casesOpt)), **kwargs)
            
    def evaluate(self, value):
        return all(map(lambda c: c.state, self.cases))
    
class ComplexCase_Or(ComplexCase):
    def __init__(self, *cases, **kwargs):
        assert len(cases)>0, "should have minimum of one given case"
        casesOpt=[]
        for case in cases:
            if isinstance(case, ComplexCase_Or):
                casesOpt.extend(case.cases)
            else:
                casesOpt.append(case)
        super().__init__(casesOpt, stateInitial=any(map(lambda c: c.state, casesOpt)), **kwargs)
            
    def evaluate(self, value):
        return any(map(lambda c: c.state, self.cases))

class ComplexCase_Not(ComplexCase):
    def __init__(self, case, **kwargs):
        super().__init__((case,), stateInitial=not case.state)
    
    def evaluate(self, value):
        return not self.cases[0].evaluate(value)

class ComplexCase_Xor(ComplexCase):
    def __init__(self, *cases, **kwargs):
        assert len(cases)>0, "should have minimum of one given case"
        casesOpt=[]
        for case in cases:
            if isinstance(case, ComplexCase_Xor):
                casesOpt.extend(case.cases)
            else:
                casesOpt.append(case)
        super().__init__(casesOpt, stateInitial=any(map(lambda c: c.state, casesOpt)), **kwargs)
            
    def evaluate(self, value):
        current=None
        for case in self.cases:
            if current==None:
                current=case.state
            else:
                current^=case.state
        return current

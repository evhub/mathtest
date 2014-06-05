from rabbit.all import *

class interface(object):
    def __init__(self):
        self.questions = [polynomials(), slope(), manipulation(), foil(), systems()]
        self.debug = self.Hook.debug
        self.pos = -1
        self.gen = random()
        for x in self.questions:
            x.Hook = self
    def new(self):
        self.pos = self.gen.chooseint(len(self.questions))
        return self.questions[self.pos].new()
    def check(self, answer):
        fanswer = superformat(answer)
        if fanswer == "skip":
            return True
        elif fanswer == "debug":
            self.debug = not self.debug
        elif fanswer.startswith("goto "):
            self.pos = int(fanswer[5:])
            self.Hook.main.display("\n"+self.questions[self.pos].new())
        else:
            return self.questions[self.pos].check(answer)
    def getdigit(self):
        return self.gen.chooseint(19)-9
    def nonzero(self):
        out = 0
        while out == 0:
            out = self.getdigit()
        return out
    def geteq(self, order):
        out = ""
        coeffs = {}
        for x in self.gen.scramble(range(0, int(order)+1)):
            coeff = self.getdigit()
            while x == order and coeff == 0:
                coeff = self.getdigit()
            coeffs[x] = coeff
            if coeff != 0:
                if coeff == 1 and x != 0:
                    coeff = ""
                elif coeff == -1 and x != 0:
                    coeff = "-"
                else:
                    coeff = str(coeff)
                if x == 0:
                    out += coeff
                elif x == 1:
                    if coeff != "" and coeff != "-":
                        coeff += "*"
                    out += coeff+"x"
                else:
                    if coeff != "" and coeff != "-":
                        coeff += "*"
                    out += coeff+"x^"+str(x)
                out += " + "
        out = out[:-3]
        if self.debug:
            print(coeffs)
        return out, coeffs

class polynomials(object):
    def new(self):
        self.order = self.Hook.gen.chooseint(6)+1
        out, coeffs = self.Hook.geteq(self.order)
        return "What is the order/degree of the polynomial:\n"+out
    def check(self, answer):
        if self.Hook.debug:
            print(self.order)
        return getnum(answer) == self.order

class foil(object):
    def new(self):
        a = self.Hook.nonzero()
        b = self.Hook.nonzero()
        c = self.Hook.nonzero()
        d = self.Hook.nonzero()
        self.answers = [a*c, a*d+b*c, b*d]
        return """Put the following expression into standard/normal form and enter
the coefficients into the calculator under their usual variable names:
("""+str(a)+"x+"+str(b)+")("+str(c)+"x+"+str(d)+")"
    def check(self, answer):
        if self.Hook.debug:
            print(self.answers)
        a = float(self.answers[0])
        b = float(self.answers[1])
        c = float(self.answers[2])
        out = True
        ratio = None
        if a == 0:
            out = out and self.Hook.Hook.calc("a") == a
        else:
            ratio = self.Hook.Hook.calc("a")/a
        if b == 0:
            out = out and self.Hook.Hook.calc("b") == b
        elif ratio == None:
            ratio = self.Hook.Hook.calc("b")/b
        else:
            out = out and self.Hook.Hook.calc("b")/b == ratio
        if c == 0:
            out = out and self.Hook.Hook.calc("c") == c
        elif ratio == None:
            ratio = self.Hook.Hook.calc("c")/c
        else:
            out = out and self.Hook.Hook.calc("c")/c == ratio
        if ratio == 0 or ratio == matrix(0):
            return False
        else:
            return out

class systems(object):
    def new(self):
        self.eqs = matrix(2,3)
        det = 0.0
        while det == 0.0:
            self.eqs.fill(self.Hook.getdigit)
            det = self.eqs.det()
        out = """Find the point of intersection:
"""+str(int(self.eqs.retreive(0,0)))+"x+"+str(int(self.eqs.retreive(0,1)))+"y="+str(int(self.eqs.retreive(0,2)))+"""
"""+str(int(self.eqs.retreive(1,0)))+"x+"+str(int(self.eqs.retreive(1,1)))+"y="+str(int(self.eqs.retreive(1,2)))
        self.eqs.keepsolvingfull(check=False)
        return out
    def check(self, answer):
        if self.Hook.debug:
            print(self.eqs)
        answer = superformat(answer)
        if len(answer) >= 3 and answer[0] == "(" and answer[-1] == ")":
            answer = answer[1:-1]
            anslist = answer.split(",")
            if len(anslist) == 2:
                answers = self.eqs.getdiag()
                return round(self.Hook.Hook.calc(anslist[0]),6) == round(answers[0],6) and round(self.Hook.Hook.calc(anslist[1]),6) == round(answers[1],6)
        return False

class slope(object):
    def new(self):
        a = self.Hook.getdigit()
        b = self.Hook.getdigit()
        c = self.Hook.getdigit()
        d = self.Hook.getdigit()
        self.answer = float(d-b)/float(c-a)
        return "Find the slope between ("+str(a)+","+str(b)+") and ("+str(c)+","+str(d)+")."
    def check(self, answer):
        if self.Hook.debug:
            print(self.answer)
        return round(self.Hook.Hook.calc(answer),12) == round(self.answer,12)

class manipulation(object):
    def new(self):
        aeq, acoeffs = self.Hook.geteq(self.Hook.gen.chooseint(2)+1)
        beq, bcoeffs = self.Hook.geteq(self.Hook.gen.chooseint(2)+1)
        self.coeffs = {}
        for k in acoeffs:
            self.coeffs[k] = acoeffs[k]
        for k in bcoeffs:
            if k in self.coeffs:
                self.coeffs[k] = self.coeffs[k]-bcoeffs[k]
            else:
                self.coeffs[k] = -1*bcoeffs[k]
        if len(self.coeffs) == 2:
            return """Solve for x:
"""+beq+" = "+aeq
        else:
            return """Put the following equation into standard/normal form and enter
the coefficients into the calculator under their usual variable names:
"""+beq+" = "+aeq
    def check(self, answer):
        if self.Hook.debug:
            print(self.coeffs)
        if len(self.coeffs) == 2:
            b = float(self.coeffs[0])
            m = float(self.coeffs[1])
            if m == 0:
                return answer == ""
            else:
                return round(self.Hook.Hook.calc(answer),6) == round(-b/m,6)
        elif len(self.coeffs) == 3:
            c = float(self.coeffs[0])
            b = float(self.coeffs[1])
            a = float(self.coeffs[2])
            out = True
            ratio = None
            if a == 0:
                out = out and self.Hook.Hook.calc("a") == a
            else:
                ratio = self.Hook.Hook.calc("a")/a
            if b == 0:
                out = out and self.Hook.Hook.calc("b") == b
            elif ratio == None:
                ratio = self.Hook.Hook.calc("b")/b
            else:
                out = out and self.Hook.Hook.calc("b")/b == ratio
            if c == 0:
                out = out and self.Hook.Hook.calc("c") == c
            elif ratio == None:
                ratio = self.Hook.Hook.calc("c")/c
            else:
                out = out and self.Hook.Hook.calc("c")/c == ratio
            if ratio == 0 or ratio == matrix(0):
                return False
            else:
                return out

class exponents(object):
    def new(self):
        self.answer = 0
        out = "x^a = ("
        stop = self.Hook.gen.chooseint(4)+2
        for x in xrange(1, stop):
            exp = self.Hook.gen.chooseint(13)
            if self.Hook.gen.getbool():
                secexp = self.Hook.gen.chooseint(9)
                self.answer += exp*secexp
                out += "(x^"+str(exp)+")^"+str(secexp)+" * "
            else:
                self.answer += exp
                out += "x^"+str(exp)+" * "
        out = out[:-3]+") / ("
        stop = self.Hook.gen.chooseint(3)+2
        for x in xrange(1, stop):
            exp = self.Hook.gen.chooseint(13)
            if self.Hook.gen.getbool():
                secexp = self.Hook.gen.chooseint(9)
                self.answer -= exp*secexp
                out += "(x^"+str(exp)+")^"+str(secexp)+" * "
            else:
                self.answer -= exp
                out += "x^"+str(exp)+" * "
        out = out[:-3]+")"
        return "Solve for a:\n"+out
    def check(self, answer):
        if self.Hook.debug:
            print(self.answer)
        return self.Hook.Hook.calc(answer) == self.answer

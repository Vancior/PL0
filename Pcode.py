class PcodeMachine:
    pc = 0
    base = 0
    top = 0
    s = list()
    codes = list()
    count = 0

    def __init__(self, codes, count):
        self.codes = codes
        self.count = count

    def get_var(self, lvl, op):
        lvl = int(lvl)
        b = self.base
        while lvl is not 0:
            b = self.s[b]
            lvl -= 1
        return self.s[b + int(op)]

    def set_var(self, lvl, op, value):
        lvl = int(lvl)
        b = self.base
        while lvl is not 0:
            b = self.s[b]
            lvl -= 1
        self.s[b + int(op)] = value

    def jmp(self, lvl, op):
        self.pc = int(op)
        return True

    def int(self, lvl, op):
        self.top += int(op)
        if self.top > len(self.s):
            self.s.extend([0 for i in range(self.top - len(self.s))])
        # print('stack size: ' + str(len(self.s)))

    def lod(self, lvl, op):
        # print('lod' + lvl + op + ' top ' + str(self.top))
        self.s.append(self.get_var(lvl, op))
        self.top += 1

    def sto(self, lvl, op):
        # print('sto' + lvl + op)
        self.set_var(lvl, op, self.s.pop())
        self.top -= 1
        # print(self.s)

    def opr(self, lvl, op):
        if getattr(self, 'opr' + op)() is True:
            return True

    def opr0(self):
        b = self.s[self.base + 1]
        self.pc = self.s[self.base + 2]
        # print('top ' + str(self.top) + 'size ' + str(len(self.s)) + ' base '+str(self.base))
        while self.top > self.base:
            self.s.pop()
            self.top -= 1
        self.base = b
        return True

    def opr1(self):
        self.s[self.top - 1] = -self.s[self.top - 1]

    def opr2(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(a1 + a2)
        self.top -= 1

    def opr3(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(a1 - a2)
        self.top -= 1

    def opr4(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(a1 * a2)
        self.top -= 1

    def opr5(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 / a2))
        self.top -= 1

    def opr8(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 == a2))
        self.top -= 1

    def opr9(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 != a2))
        self.top -= 1

    def opr10(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 < a2))
        self.top -= 1

    def opr11(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 >= a2))
        self.top -= 1

    def opr12(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 > a2))
        self.top -= 1

    def opr13(self):
        a2 = self.s.pop()
        a1 = self.s.pop()
        self.s.append(int(a1 <= a2))
        self.top -= 1

    def lit(self, lvl, op):
        self.s.append(int(op))
        self.top += 1

    def jpc(self, lvl, op):
        self.top -= 1
        if self.s.pop() is 0:
            self.jmp(lvl, op)
            return True

    def wrt(self, lvl, op):
        print('output: ' + str(self.s.pop()))
        self.top -= 1

    def red(self, lvl, op):
        print('input: ', end='')
        num = input()
        self.set_var(lvl, op, int(num))

    def cal(self, lvl, op):
        lvl = int(lvl)
        b = self.base
        while lvl is not 0:
            lvl -= 1
            b = self.s[b]
        self.s.append(b)
        self.s.append(self.base)
        self.s.append(self.pc + 1)
        self.base = self.top
        # print(self.s)
        self.jmp(lvl, op)
        return True

    def exe(self):
        self.s.append(-1)
        self.s.append(-1)
        self.s.append(-1)

        while -1 < self.pc < self.count:
            # print(self.pc)
            ins = self.codes[self.pc].split()
            fct = ins[0]
            lvl = ins[1]
            op = ins[2]

            if getattr(self, fct.lower())(lvl, op) is not True:
                self.pc += 1

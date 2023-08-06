# Numtmath Module 1.6 (Functional Paradigm Version)
#
# Module for working with several number theory concepts

# Alphabeth for visual base representation up to base 36
# To use higher bases you can add your own symbols for digit representation using morealph
# Or Use nonsymb = 1 parameter to return list of corresponding "number in digit"

# To make functions that use prime numbers work faster you can use your own txt-file lists
# of prime numbers or use primes from file froms website https://primes.utm.edu
# To Use Multiple txt files add to function that uses primes to parameter file like this
# file=["primes1.txt", "primes2.txt" and etc], type=1
alph = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def __initHelp():
    from sys import executable

    ppath = executable
    ppath = ppath[0:len(ppath) - 10]
    ppath += "\\Lib\\numtmath.py"
    f = open(ppath, "r")

    phelpArr = []
    while True:
        proto = f.readline()
        if proto == "":
            break
        elif proto[0:3] == "def" and proto[5] != "_":
            phelpArr.append(proto[4:len(proto) - 2])
        elif proto[0:2] == "#-":
            phelpArr.append("")
            phelpArr.append(proto[3:len(proto) - 1])

    f.close()
    return phelpArr

# Type 0 - Listed Primes By \n
# Type 1 - For Files From https://primes.utm.edu and http://www.primos.mat.br/2T_en.html
#- Function for getting primes from files for use in prime related functions


def getPrimesFromFile(files, type = 0):

    primeArr = []
    for i in range(len(files)):
        f = open(files[i], "r")

        while True:
            pprimeArr = f.readline()
            if pprimeArr == "":
                break
            if type == 0:
                primeArr.append(int(pprimeArr))
            else:
                protoOne = ""
                for j in range(len(pprimeArr)):
                    if pprimeArr[j] == "T":
                        break

                    if pprimeArr[j] != " " and pprimeArr[j] != "	" \
                    and pprimeArr[j] != "\n":
                        protoOne += pprimeArr[j]
                    elif protoOne != "":
                        primeArr.append(int(protoOne))
                        protoOne = ""

        f.close()

    return primeArr

#- Main Functions


def help():

    helpArr = ["Number Theory Math Module"]
    pHelpArr = __initHelp()
    helpArr += pHelpArr

    for i in helpArr:
        print(i)


def basechange(n, frombase = 10, tobase = 2, nonsymb = 0, morealph = ""):

    def toint(n, frombase, local_alph):
        res = 0
        inv_n = n[::-1]
        for i in range(len(n)):
            res += local_alph.index(inv_n[i]) * (frombase ** i)
        return res

    local_alph = alph
    local_alph += morealph

    n = str(n)
    int_n = toint(n, frombase, local_alph)

    if n == "0" or n == "":
        return "0"
    if tobase == 1:
        if nonsymb:
            print("0" * n)
        else:
            return "0" * n
        return None

    if not nonsymb:
        res = ""
    elif nonsymb or tobase > len(local_alph):
        res = []

    r = 0

    while tobase ** r <= int_n:
        r += 1
    r -= 1

    pres = 0
    while r > -1:
        if int_n - tobase ** r >= 0:
            pres += 1
            int_n -= tobase ** r
            continue
        if nonsymb:
            res.append(pres)
        else:
            res += local_alph[pres]
        r -= 1
        pres = 0

    return res


def primes(n, amount = 0):

    arr = [2]

    if amount:
        rangeArr = [3]
    else:
        rangeArr = list(range(3, n + 1))
    for i in rangeArr:
        if amount:
            rangeArr.append(i + 1)
            if len(arr) == n:
                break

        isPrime = True
        if i < 6 or (i % 6 == 1 or i % 6 == 5):
            for k in arr:
                if i % k == 0:
                    isPrime = False
                    break
            if isPrime:
                arr.append(i)
        
    return arr


def factorize(n, arr = [], radical = 0):

    res = []

    half_n = int(n / 2)
    customPrimes = True

    if arr != []:
        primeArr = arr
    else:
        primeArr = primes(half_n)
        customPrimes = False

    for i in range(len(primeArr)):
        if n == 1:
            break
        if customPrimes and primeArr[i] > half_n:
            break

        while n % primeArr[i] == 0:
            n = int(n / primeArr[i])
            if not radical or res.count(primeArr[i]) == 0:
                res.append(primeArr[i])

    if len(res) == 0:
        res.append(n)

    return res


def obvprime(tocheck, arr = [], show = 0):
    try:
        tocheck[0]
    except TypeError:
        proto = tocheck
        tocheck = []
        tocheck.append(proto)
    else:
        tocheck = list(tocheck)

    if arr != []:
        primeArr = arr
    else:
        primeArr = primes(max(tocheck))

    tocheck_mem = list(tocheck)
    arr = []
    for i in range(len(tocheck)):
        arr.append([])
    for i in range(len(tocheck)):
        for j in range(len(primeArr)):
            if tocheck[i] % primeArr[j] == 0:
                arr[i].append(primeArr[j])
                tocheck[i] /= primeArr[j]
    tocheck = list(tocheck_mem)

    res = [0] * len(tocheck)
    for i in range(len(tocheck)):
        for j in range(tocheck[i]):
            for k in range(len(arr[i])):
                if j % arr[i][k] == 0:
                    res[i] += 1
                    break

    C = []
    for i in range(len(tocheck)):
        C.append(len(arr[i]) / (((tocheck[i] - res[i]) ** 2) / tocheck[i]))

    if show:
        skipArr = [0] * 3
        skipArr[0] = len(str(max(tocheck)))
        skipArr[1] = len(str(max(tocheck) - max(res)))
        skipArr[2] = 8
    else:
        resArr = []

    for i in range(len(tocheck)):
        per = res[i] / tocheck[i]
        if show:
            print(str(tocheck[i]) + " " * (skipArr[0] - len(str(tocheck[i])) + 1)
                + str(tocheck[i] - res[i]) + " " * (skipArr[1] - len(str(tocheck[i] - res[i])) + 1)
                + str(round(per * 100, 5)) + "% " + " " * (skipArr[2] - len(str(round(per * 100, 5))))
                + str(round(C[i], 5))
            )
        else:
            resArr = [tocheck[i], tocheck[i] - res[i], res[i] / tocheck[i], C[i]]

    if not show:
        return resArr


def rootpat(n, powroot = 2, show = 0, process = 0, arr = []):

    def dividers(num, primes, sqVal):

        for n in primes:
            if n > num:
                break
            while num % n == 0:
                sqVal[primes.index(n)] += 1
                num /= n

        return sqVal

    def check_rep(sqArr, powroot):

        for n in range(len(sqArr)):
            while sqArr[n] > powroot - 1:
                sqArr[n] -= powroot

        return sqArr

    def show_root(sqArr, n, powroot, primes):
        print(str(n) + " => ", end="")
        if powroot == 2:
            print("sqrt(", end="")
        else:
            print(str(powroot) + "root(", end="")

        mid_str = ""
        
        for n in range(len(sqArr)):
            if sqArr[n] > 0:
                mid_str += str(primes[n])
                if sqArr[n] > 1:
                    mid_str += "^" + str(sqArr[n]) 
                mid_str += " * "
            
        n = 0
        mid_str = list(mid_str) 
        while n <3: # less than 3 with love
            mid_str.pop(len(mid_str) - 1)
            n += 1
        
        mid_str = "".join(mid_str)
        print(mid_str, end="")
        print(")")

    def ret_sqrt(sqArr, primes):
        retArr = []

        for i in range(len(sqArr)):
            retArr += [primes[i]] * sqArr[i]

        return retArr

    if arr != []:
        primeArr = arr
    else:
        primeArr = primes(n)
    sqArr = [0] * len(primeArr)
    resArr = []

    for i in range(2, n + 1):
        sqArr = dividers(i, primeArr, sqArr)
        sqArr = check_rep(sqArr, powroot)
        if process and show:
            show_root(sqArr, i, powroot, primeArr)
        elif process:
            resArr.append(ret_sqrt(sqArr, primeArr))

    if process:
        return resArr
    else:
        return ret_sqrt(sqArr, primeArr)


def udiv(n, k, base = 10, morealph = "", nonsymb = False, show = 0):
    if n < 1 or k < 1:
        print("Error. Invalid Params.")
        return ""

    resArr = ["", 0, 0]
    local_alph = alph + morealph
    if base > len(local_alph):
        nonsymb = True
        resArr = [[], 0, 0]

    if nonsymb and show:
        print("Error. Can't Show When base is larger then alphabet")
        return ""

    mem_n = n

    #print("Check1")

    big_num = 0

    res = []
    ost_1 = []
    ost_2 = []
    stop_this = False
    stop_this_special = False
    counter = 0
    # Before Start, Check if n in n/k is bigger than k
    if n >= k:
        while n >= k:
            #print("Check3")
            n -= k
            big_num += 1
    big_num = basechange(big_num, 10, base, morealph=morealph, nonsymb=nonsymb)
    # main alg.
    # We know that it's smaller. but to do ultradivision we add basenumber to n
    # We have to add 0 if we've added basenumber twice or more
    #
    #
    if n < k and n != 0:
        while not stop_this:
            #print("Check4")
            if n < k:
                if counter > 0:
                    for j in range(len(ost_1)):
                        #print("Check5")
                        if n == ost_1[j] and n * base == ost_2[j]:
                            stop_this = True
                            break
                    if not stop_this:
                        res.append("0")
                        ost_1.append(n)
                        ost_2.append(n * base)
                n *= base
                counter += 1
                continue

            # Second Part
            # Subtracting from fraction
            counter = 0
            i = 1
            if stop_this:
                break
            while True:
                #print("Check6")
                if n - k * i == 0:
                    res.append(str(i))
                    stop_this_special = True
                    break
                elif n - k * i < 0:
                    i -= 1
                    proto_ost_1 = n
                    n = n - k * i
                    proto_ost_2 = n
                    j = 0
                    while j < len(ost_1):
                        #print("Check7")
                        if proto_ost_1 == ost_1[j] and proto_ost_2 == ost_2[j]:
                            stop_this = True
                            break
                        j += 1
                    if not stop_this:
                        res.append(str(i))
                        ost_1.append(proto_ost_1)
                        ost_2.append(proto_ost_2)
                    break
                i += 1
            if stop_this_special:
                res.append("0")
                j = len(res) - 1
                break
    else:
        res.append("0")
        j = 0

    if nonsymb:
        resArr[0].append(int(big_num))
    elif show == 0 and not nonsymb:
        resArr[0] += big_num
        resArr[0] += "."
    elif show:
        print(str(mem_n) + " / " + str(k) + " = ", end = '')
        print(str(big_num) + ".", end = '')

    i = 0
    per_amount = 0
    while i < len(res):
        #print("Check8")
        if i == j:
            per_amount = i
            if show == 0 and not nonsymb:
                resArr[0] += "("
            elif show:
                print("(", end = '')
        if nonsymb:
            resArr[0].append(int(res[i]))
        elif show == 0 and not nonsymb:
            resArr[0] += local_alph[int(res[i])]
        else:
            print(str(local_alph[res[i]]), end = '')
        i += 1
    if show == 0 and not nonsymb:
        resArr[0] += ")"
    elif show:
        print(")", end = '')
    post_per_amount = i - per_amount

    if show == 0:
        resArr[1] = post_per_amount
        resArr[2] = j
        return resArr
    else:
        print("\n")
        print("Length of a period: " + str(post_per_amount))
        print("")


def sigmaf(n, bases = 10, morealph = "", show = 0):
    from math import sqrt as _sqrt

    local_alph = alph

    resArr = [[], [], ""]

    if morealph != 0:
        local_alph += morealph
        
    k = n ** 2

    bitline = ""

    count = 0
    for base in range(2, bases + 1):

        res = basechange(k, 10, base)

        suma = 0
        i = 0
        while len(res) != i:
            j = 0
            while local_alph[j] != res[i]:
                j += 1
            suma += j
            i += 1

        if show == 0:
            resArr[0].append(res)
            resArr[1].append(suma)
        else:
            print("Base " + str(base) + " = " + res + " | Sum is " + str(suma), end='')
        if _sqrt(suma).is_integer():
            if show == 1:
                print(" = " + str(int(_sqrt(suma))) + "^2 TRUE")
            count += 1
            bitline += '1'
        else:
            bitline += '0'
            if show == 1:
                print(" FALSE")
        base += 1
        
    if show == 0:
        resArr[2] = bitline
        return resArr
    else:
        print("")
        print(bitline)
        print("")
        print("True for " + str(count) + " bases")


def sigmamatrix(n, bases = 10, morealph = "", base1 = 0, show = 0):
    from math import sqrt

    local_alph = alph
    local_alph += morealph
    
    arr = sigmaf(n, bases)
    
    bitline = arr[2]

    if show:
        print(n ** 2)
        print("")

    if base1:
        i = 0
        print("Base 1")
        while i < n:
            print("0 " * n)
            i += 1
        print("\n")

    resArr = []
    maxLenNum = 1

    for i in range(bases - 1):
        if bitline[i] == "1":
            if show:
                print("Base " + str(i + 2))

            count = 0
            protoResArr = []
            for j in range(len(arr[0][i])):
                if local_alph.index(arr[0][i][j]) > 0:
                    for k in range(local_alph.index(arr[0][i][j])):
                        lenNum = len(str(len(arr[0][i]) - j - 1))
                        if lenNum > maxLenNum:
                            maxLenNum = lenNum
                        if show:
                            print((" " * (maxLenNum - lenNum)) +
                                  str(len(arr[0][i]) - j - 1), end=" ")
                        else:
                            protoResArr.append(int(len(arr[0][i]) - j - 1))
                        count += 1
                        if count == int(sqrt(arr[1][i])):
                            count = 0
                            if show:
                                print("") # newline
            if show:
                print("\n")
            resArr.append(protoResArr)
        elif not show:
            resArr.append([])

    if not show:
        return resArr


def contfrac(inp, a = 0, simple = 0):

    def conttosimple(pat):
        if len(pat) == 1:
            return [pat[0], 1]

        resArr = [0, 0]
        pat = pat[::-1]

        i = 0
        while i < len(pat):
            if i == 0:
                resArr[0] = pat[i] * pat[i + 1] + 1
                resArr[1] = pat[i]
                i += 1
            else:
                resArr = resArr[::-1]
                resArr[0] = pat[i] * resArr[1] + resArr[0]
            i += 1

        return resArr

    inpBool = True
    try:
        inp[0]
    except TypeError:
        inpBool = False

    res = []
    if inpBool and not simple:
        res = 0

        res = conttosimple(inp)
        res = res[0] / res[1]
    elif not inpBool:

        if a == 0:
            a = 10

        for i in range(a):
            if i == 0:
                res.append(int(inp))
            else:
                if inp == 0:
                    break
                res.append(int(1 / inp))
                inp = 1 / inp
            inp -= res[i]
    else:
        if inpBool:
            res = conttosimple(inp)
        else:
            res = conttosimple(res)

    return res


def deafbus(n, steps, showproc = 0, stopfor = 0.5):
    from random import randint as _randint
    from os import system as _system
    from time import sleep as _sleep
    
    def showfunc(n, bus, road, stop, avr, step):
        _system("cls")

        print(step)
        print("")
        print("Bus = [ ", end="")
        for i in range(n):
            print(str(bus[i]) + " ", end="")
        print("] Sum = " + str(sum(bus)))
        print("")

        print("Road")
        for i in range(n):
            if i == stop:
                print(" * ", end="")
            else:
                print("   ", end="")
            for j in range(len(road[i])):
                print(str(road[i][j]) + " ", end="")
            print("")

        print("Avarage num of passangers " + str(avr))
        _sleep(stopfor)
    
    bus = [0] * n
    road = []
    # two-dimentional road array made this way because of junk data
    for i in range(n):
        road.append([])

    stepsRes = 0
    avr = 0
    goback = False 

    i = 0
    for step in range(steps):
        if showproc:
            showfunc(n, bus, road, i, avr, step)

        if not goback and i == n - 1 or goback and i == 0:
            goback = not goback

        road[_randint(0, n - 1)].append(_randint(0, n - 1))
        _sleep(0.01)

        if road[i] is not None:
            for j in range(len(road[i])):
                bus[road[i][j]] += 1
            road[i] = []

        if bus[i] > 0:
            bus[i] = 0
        stepsRes += sum(bus)
        avr = stepsRes / (steps + 1)

        if goback:
            i -= 1
        else:
            i += 1

    return avr


def metanum(num, meta, show = 0):
    num = str(num)

    try:
        meta[0]
    except TypeError:
        proto = str(meta)
        meta = []
        meta.append(proto)
    else:
        meta = list(meta)
        # Sorted to make search quicker. Explained below
        sorted(meta)
        for i in range(len(meta)):
            meta[i] = str(meta[i])

    filecheck = num[::-1]
    if filecheck[:4] == "txt.":
        f = open(num, "r")
        num = f.read()
        f.close()

    resArr = [None] * len(meta)

    for i in range(len(meta)):

        showArr = []
        count = 0
        startnum = 0
        showJ = 0
        # Depending no i starting point will be chosen for quicker search
        # Because, for example, there can not be 100 in a number before 10
        # Or 1359 before 135 a etc
        for j in range(i):
            if (meta[j])[:len(meta[i])] == meta[i]:
                startnum = j
                break

        for j in range(startnum, len(num)):

            if meta[i][count] == num[j]:
                count += 1
                if show:
                    showArr.append(num[j])
            else:
                showJ = j
                count = 0
                showArr = []

            if count == len(meta[i]):
                resArr[i] = j
                break
        if show:
            print(num[:showJ] + "[" + "".join(showArr) + "]", end="")
            print("")
            print(resArr[i])


    if not show:
        return resArr

#- Sequence/Small Functions


def product(list):
    res = 1

    for i in range(len(list)):
        res *= list[i]

    return res


def fibbseq(a = 10):
    fibb = [0, 1]

    for i in range(a):
        fibb.append(fibb[i] + fibb[i + 1])

    return fibb


def powseq(n, a = 10, inv_n = False):
    res = []

    for i in range(1, a + 1):
        if inv_n:
            res.append(pow(n, i))
        else:
            res.append(pow(i, n))

    return res


def disintseq(seq, show = 0):
    seq = list(seq)

    usedLen = len(seq) - 1
    resLen = int((usedLen * (usedLen + 1)) / 2)

    res = [seq]
    pres = []
    count = 0
    countneed = len(seq) - 1
    for i in range(resLen):
        pres.append(res[len(seq) - (countneed + 1)][count + 1] -
                    res[len(seq) - (countneed + 1)][count])
        if count + 1 == countneed:
            res.append(pres)
            pres = []
            count = 0
            countneed -= 1
        else:
            count += 1

    if show:
        for i in range(len(res)):
            for j in range(len(res[i])):
                print(str(res[i][j]) + " ", end="")
            print("")
    else:
        return res

# Generalization of Collatz Conjecture
# g(n) = a * n + b = i (mod P)
# See: http://people.cs.uchicago.edu/~simon/RES/collatz.pdf


def gencollatz(n, a = [0.5, 3], b = [0, 1], top = 0, checkForCicle = 0):
    isTop = False
    if top != 0:
        isTop = True

    if len(a) == len(b):
        P = len(a)
    else:
        print("Error. a and b params must be same len")
        return 0

    res = [[], 0]
    res[0].append(n)

    am = 0
    while n != 1:
        toStop = False
        if isTop:
            if am == top:
                break
        if checkForCicle:
            for i in range(len(res[0]) - 1):
                if res[0][i] == n:
                    toStop = True
                    break
        if toStop:
            break

        for i in range(len(a)):
            if n % P == i:
                n = n * a[i] + b[i]
                break
        res[0].append(int(n))
        am += 1

    res[1] = am
    return res


def riemannzeta(n, a, giveall = 0):
    zetares = [[], 0]

    for i in range(1, a):
        zetares[1] += 1 / (i ** n)
        if giveall:
            zetares[0].append(zetares[1])

    if giveall:
        return zetares
    return zetares[1]


def revtaxi(n, am = 2, r = 2):

    lastres = []
    num = [1] * am
    isRes = False

    def raiseNumSystem(num, numToRaise):
        num[numToRaise] += 1
        for i in range(numToRaise + 1, am):
            num[i] = num[numToRaise]

        return num

    numRaise = am - 1
    while numRaise > -1:
        res = 0
        for i in range(am):
            res += (num[i] ** r)

        if res == n:
            lastres.append(num.copy())
        if res > n:
            numRaise -= 1
        else:
            numRaise = am - 1
        num = raiseNumSystem(num, numRaise)

    return lastres


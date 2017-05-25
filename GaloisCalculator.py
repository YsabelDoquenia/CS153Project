import sys

#prints array of coefficients into a polynomial
def printEquation(coeff):
    for a in range(len(coeff)-1,-1,-1):
		if a==0:
			print "+", str(coeff[a]),
		elif a==len(coeff)-1:
			print str(coeff[a])+ "(x^" + str(a) + ")",
		else:
			print "+", str(coeff[a]) + "(x^" + str(a) + ")",
    return

#input validation for polynomial
def coeffValidation(coeff):
    if len(coeff)==0:
        print "no input"
        sys.exit()

    for b in coeff:
        if b.isdigit()==0:
			print "input not an integer"
			sys.exit()
    return

#input validation for irreducible polynomial
def binaryValidation(binary):
    if len(binary)==0:
        print "no input"
        sys.exit()

    for c in binary:
		if not(c=="0" or c=="1"):
			print "input not binary"
			sys.exit()		
    return

#removes leftmost zeroes coefficients in polynomial
def removeZero(coeff):
    while coeff and coeff[len(coeff)-1] == 0:
        coeff.pop()
    if coeff == []:
        coeff.append(0)
    return coeff

#adds or subtracts two polynomials
def addSubtract(a,b):
    
    #initializes array for sum or difference
    result=[]

    #solves for the sum or difference
    for d in range(len(a)):
        result.append(int(a[d])^int(b[d]))

	#formats a for printing
	a2=a[:]
	a2=removeZero(a2)
	a2.reverse()
    a2=' '.join(str(d) for d in a2)

	#formats b for printing
    b2=b[:]
    b2=removeZero(b2)
    b2.reverse()
    b2=' '.join(str(d) for d in b2)
        
	#formats sum or difference for printing
    result2=result[:]
    result2.reverse()
    result2=' '.join(str(d) for d in result2)

    #computes for length to be used in formatting the output
    length=len(result2)*2

    #prints the solution
    print ('{0:>{1}}'.format(a2, length))
    print ('{0:>{1}}'.format(b2, length))
    print "xor"+ "_"*(length-3)
    print ('{0:>{1}}'.format(result2, length)), "\n"

    #returns the sum or difference
    return result

#xor for modulo arithmetic
def xorUniLen(a, b):
    result=[]

    for e in range(1, len(b)):
        if a[e]==b[e]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

#solves for the remainder
def modulo(dividend, divisor):
	
	#checks if value of dividend is less than value of divisor
    if int(dividend,2)<=int(((len(divisor)-1)*"1"),2):
        return dividend

    #divides the dividend by the divisor
    divisorLen = len(divisor)
    part = dividend[0 : divisorLen]
    while divisorLen < len(dividend):
        if part[0]=='1':
            part=xorUniLen(divisor, part) + dividend[divisorLen]
        else:   
            part=xorUniLen('0'*divisorLen, part) + dividend[divisorLen]
        divisorLen+=1
    if part[0]=='1':
        part=xorUniLen(divisor, part)
    else:
        part=xorUniLen('0'*divisorLen, part)

	#returns the remainder
    return part

#multiplies two numbers bitwise
def multiplyBitwise(multiplicand, multiplier, irreducible):
	reversedMultiplier=reversed("{0:b}".format(multiplier))
	
	#multiplies the two numbers bitwise and formats them in base 2
	productsToXor=[(multiplicand<<i)*int(bit) for i, bit in enumerate(reversedMultiplier)]
	productsToXor=[format(productsToXor[x], "b") for x in range(len(productsToXor))]
	
	#xors the lines of product and formats them in base 2 to get the final product
	result=int(productsToXor[0],2)
	for f in range(1, len(productsToXor)):
		result=result^(int(productsToXor[f], 2))
	result=format(result, "b")

	#reduces the product
	result=modulo(result, irreducible)

	#returns the product
	return result 

#multiplies two polynomials
def multiply(multiplicand, multiplier, irreducible):
    
    #initializes array for product
    result=[]

    #removes leftmost zeroes 
    multiplicand=removeZero(multiplicand)
    multiplier=removeZero(multiplier)
    
    #formats multiplicand for printing
    multiplicand2=multiplicand[:]
    multiplicand2.reverse()
    multiplicand2=' '.join(str(g) for g in multiplicand2)

    #formats multiplier for printing
    multiplier2=multiplier[:]
    multiplier2.reverse()
    multiplier2=' '.join(str(g) for g in multiplier2)

    #reverses order for easier multiplication
    multiplicand.reverse()

    #multplies the polynomials
    products=[]
    for lierInd in range(len(multiplier)):
        products.append([])
        for licandInd in range(len(multiplicand)):
            products[lierInd].append(int(multiplyBitwise(multiplier[lierInd], multiplicand[licandInd], irreducible), 2))
        for counter in range(lierInd):
            products[lierInd].append(0)

    #computes for length to be used in formatting the output
    length=((len(products[len(products)-1])*2)-1)*2

    #prints the solution
    print ('{0:>{1}}'.format(multiplicand2, length))
    print ('{0:>{1}}'.format(multiplier2, length))
    print "x"+ "_"*(length-1)
    for line in products:
        line=' '.join(str(g) for g in line)
        print('{0:>{1}}'.format(line, length))
    print "xor"+ "_"*(length-3)

    #makes sure the lines of products have the same size
    for columnInd in range(len(products)):
        products[columnInd].reverse()
        for g in xrange(len(products[len(products)-1])-len(products[columnInd])):
            products[columnInd].append(0)    

    #xors the lines of product
    for g in range(len(products[len(products)-1])):
        result.append(products[0][g])
        for h in range(1, len(products)):
            result[g]=result[g]^products[h][g]

    #formats product for printing
    result2=result[:]
    result2.reverse()
    result2=' '.join(str(g) for g in result2)

    #prints the remainder
    print ('{0:>{1}}'.format(result2, length)), "\n"

    #returns the product
    return result
        
#divides two polynomials
def divide(dividend, divisor, irreducible):
    
    #formats dividend for printing
    dividendOrig=dividend[:]
    dividendOrig=removeZero(dividendOrig)
    dividendOrig.reverse()
    dividendOrig=' '.join(str(g) for g in dividendOrig)

    #formats divisor for printing
    divisorOrig=divisor[:]
    divisorOrig=removeZero(divisorOrig)
    divisorOrig.reverse()
    divisorOrig=' '.join(str(g) for g in divisorOrig)

    #computes for length to be used in formatting the output
    length=len(dividendOrig)*2

    #makes copes of dividend and divisor and removes leftmost zeroes
    dividend=dividend[:]
    divisor=divisor[:]
    dividend=removeZero(dividend)
    divisor=removeZero(divisor)
    if len(dividend)>=len(divisor):
        diffLen=len(dividend)-len(divisor)
        divisor=[0]*diffLen+divisor
    else:
        return [0], dividend

    #prints the solution
    print " "*len(divisorOrig), "_"*length
    print divisorOrig, ")"+('{0:>{1}}'.format(dividendOrig, length-1))

    quotient=[]
    divisorPart=float(divisor[len(divisor)-1])
    for i in xrange(diffLen+1):
        quotientPart=dividend[len(dividend)-1]/divisorPart
        quotient.insert(0, quotientPart)
        if quotientPart!=0:
        	
        	#multiplies the part of quotient to dividend
            d=[int(multiplyBitwise(int(quotientPart), j, irreducible), 2) for j in divisor]
            
            #xors product
            dividend=[j^k for j, k in zip(dividend, d)]

        dividend.pop()
        divisor.pop(0)

    	#formats d for printing
        d2=d[:]
        d2.reverse()
        d2=' '.join(str(g) for g in d2)
        
	    #formats dividend for printing
        dividend2=dividend[:]
        dividend2.reverse()
        dividend2=' '.join(str(g) for g in dividend2)

    	#prints the solution
        print " "*len(divisorOrig), ('{0:>{1}}'.format(d2, length)), "\tQ=[" + str(int(quotientPart)) + "]"
        print " "*len(divisorOrig), "xor"+"_"*(length-3)
        print " "*len(divisorOrig), ('{0:>{1}}'.format(dividend2, length))
    
    quotient=[int(quotient[l]) for l in range(len(quotient))]
    dividend=removeZero(dividend)
    
    #formats quotient for printing
    quotient2=quotient[:]
    quotient2.reverse()
    quotient2=' '.join(str(g) for g in quotient2)
    
	#prints the quotient and remainder
    print "\n"," "*len(divisorOrig), quotient2, "remainder", dividend2,"\n"

    #retturns the quotient and remainder
    return quotient, dividend

def galoisCalculator():
	print "Galois Field Calculator: "
	#input getting, validation, and formatting for polynomials
	AxStr=raw_input("input A(x): ")
	# AxStr="1 0 7 6" #test data
	AxArr=AxStr.split()
	coeffValidation(AxArr)
	AxArr=map(int, AxArr)
	AxArr.reverse()
	Ax=AxArr[:]

	BxStr=raw_input("input B(x): ")
	# BxStr="1 6 3" #test data
	BxArr=BxStr.split()
	coeffValidation(BxArr)
	BxArr=map(int, BxArr)
	BxArr.reverse()
	Bx=BxArr[:]

	PxStr=raw_input("input P(x): ")
	# PxStr="1 0 1 1" #test data
	PxArr=PxStr.split()
	binaryValidation(PxArr)
	PxArr=map(int, PxArr)
	irreducible=''.join([str(x) for x in PxArr])

	if len(AxArr)>len(BxArr):
		for m in xrange(len(AxArr)-len(BxArr)):
			BxArr.append(0)	
	elif len(AxArr)<len(BxArr):
		for n in xrange(len(BxArr)-len(AxArr)):
			AxArr.append(0)

	#prints A and B
	print "\n", "A(x) =",
	printEquation(removeZero(Ax))
	print "\n", "B(x) =", 
	printEquation(removeZero(Bx))
	print 

	#input getting and validation for operator and solving for solution
	Result=[]
	op=raw_input("\ninput operation [+, -, x, /]: ")
	print 
	if not(op=="+" or op=="-" or op=="x" or op=="/"):
		print "input not operation"
		sys.exit()
	elif op=="+":
		Result=addSubtract(AxArr,BxArr)
		print "A(x) + B(x) =", 
		printEquation(removeZero(Result))
	elif op=="-":
		Result=addSubtract(AxArr,BxArr)
		print "A(x) - B(x) =", 
		printEquation(removeZero(Result))
	elif op=="x":
		Result=multiply(AxArr, BxArr, irreducible)
		print "A(x) x B(x) =", 
		printEquation(removeZero(Result))
	else:
		Result, Remainder=divide(AxArr, BxArr, irreducible)
		print "A(x) / B(x) =", 
		printEquation(removeZero(Result))
		print "remainder", 
		printEquation(removeZero(Remainder))

galoisCalculator()
close=raw_input("\n\nPress any key to exit")

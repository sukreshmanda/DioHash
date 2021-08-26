def dio128(text):
	return DioHashGen.dio128(text)
	
def dio256(text):
	return DioHashGen.dio256(text)

def dio512(text):
	return DioHashGen.dio512(text)
	
'''
	Diophantine is a class that holds the methods to encrypt the block 
	DioHashGen is a hashing class that uses Diophantine to generate a fixed length hash
	DioHashGenDigest is a class that is used to hold hash and print it in hexadecimal values
'''
class Diophantine:
	def __init__(self):
		self.error512bit = [7991590464102700538016803728265574033508963419690358323494598456057559374405435353559091933298276062628651569134596234376322910925441582926210600144944331,			11809832619586756526954249559371746436528431273139600375368976133146945383528295915655142356218600537774726760626255472472679966063758049694648684345853438,	13118985682899543011471564343190407891927667246125977131626165426584269326588351721750502260137645800131689799513730538622596866676040561679885733543275824]
		
		self.error256bit = [99166598358548718087598233042355901690601093114326574646807270256671086949907,
							106446256821792692211201767963948321933157535761523723855972807442084413545950,
							21092548417009999164762991407874004996240339622881057660190499063107261810881]
							
		self.error128bit = [171439610939273906313104041256502705599,
							310779508129353015119452370658369948582,
							284258345208273711794377222192950695752]
		
		self.encryptLookpup = {}
	
	def genSign(self, num):
		if(num % 3 == 2):
			return -num
		else:
			return num
			
	def cipherGen(self, first, second, third, k):
		n = 0
		error = None
		
		if(k == 512):
			error = self.error512bit
		elif(k == 256):
			error = self.error256bit
		else:
			error = self.error128bit
		n = k
		
		self.n = (1<<n) -1
		self.n_squared = (1<<(n*2))
		
		first %= self.n
		second %= self.n
		third %= self.n
		
		first = self.genSign(first)
		second = self.genSign(second)
		third = self.genSign(third)
			
		some = first+error[0]
		some = (some*(first+error[0]))%self.n_squared
		some = (some*(first+error[0]))%self.n_squared
		
		some = (some*(second+error[1]))%self.n_squared
		some = (some*(second+error[1]))%self.n_squared
		
		some = (some*(third+error[2]))%self.n_squared
		some = (some*(third+error[2]))%self.n_squared
		return some % self.n_squared
	
	def encipher(self, num, key, val):
		
		k = str(num)
		if(len(k) == 1):
			res_first = k
			res_second = "0"
		else:
			res_first, res_second = k[:len(k)//2], k[len(k)//2:]
		cip = self.cipherGen(int(res_first), -int(res_second), key, val)
		return cip
	
	def encipher1024(self, num, key):
		try:
			return self.encryptLookpup[str(num)+str(key)+str(512)]
		except:
			self.encryptLookpup[str(num)+str(key)+str(512)] = self.encipher(num, key, 512)
			return self.encryptLookpup[str(num)+str(key)+str(512)]
			
	def encipher512(self, num, key):
		try:
			return self.encryptLookpup[str(num)+str(key)+str(256)]
		except:
			self.encryptLookpup[str(num)+str(key)+str(256)] = self.encipher(num, key, 256)
			return self.encryptLookpup[str(num)+str(key)+str(256)]
		
	def encipher256(self, num, key):
		try:
			return self.encryptLookpup[str(num)+str(key)+str(128)]
		except:
			self.encryptLookpup[str(num)+str(key)+str(128)] = self.encipher(num, key, 128)
			return self.encryptLookpup[str(num)+str(key)+str(128)]

	def samplePlot():
		b = Diophantine()
		i = 0
		dic = {}
		x = []
		y = []
		while(i < 2**6):
			cip = b.encipher512(i, 1000)
			try:
				print(dic[i])
				break
			except:
				x.append(i)
				y.append(cip)
				print(cip)
				dic[i] = cip
				i+=1

		import matplotlib.pyplot as plt
		plt.scatter(x, y)
		plt.title('scatter plot of first 2^11 numbers')
		plt.show()
		
class DioHashGenDigest:
	def __init__(self, num):
		self._num = num
		
		val = str(hex(self._num))
		rem = len(val[2:])%32
		if(rem != 0):
			val = val[:2]+("0"*(32-rem))+val[2:]
		self._hexDigest = val
		
	def hexdigest(self):
		return self._hexDigest
		
class DioHashGen:
	hashLookup = {}
	numLookup = {}
	textLoopup = {}
	textBinaryLookup = {}
	jk = 0
	key256 = "56452847317470847780420846729267947979707761347141850011287957615499295455963"
	key512 = "6175309401099161027430394617385645136469765382081345148304962668068071414557710687298189822728381307577020131366933028844681775228434920174247030551479261"
	key1024 = "102075845507873469859778814765300515743286545404539510706589284426012831965769040834968913537510758939973911178393190877935127913303894146815063536414783241954479067149764571464189258159689223439846870497625403894592136961755623393099663998351055324008943168430854230979120951539053847914558345556450664190412"
	
	def textToBinary(text):
		if(len(text) == 1):
			return format(ord(text), '08b')
		try:
			return DioHashGen.textBinaryLookup[text]
		except:
			DioHashGen.textBinaryLookup[text] = format(ord(text[0]), '08b')+DioHashGen.textToBinary(text[1:])
			return DioHashGen.textBinaryLookup[text]
			
	def preprocess(text, num):
		res = DioHashGen.textToBinary(text)
				
		size = len(res)

		appendsize = size+64
		remaining = appendsize % num
		
		if(remaining != 0):
			res += "1"
			res += "0"*(num-remaining-1)
			
		res+=format(size, '064b')
		return res
		
	def DioHashGen(text, size):
		
		block = Diophantine()
		try:
			bits = DioHashGen.textLoopup[text+str(size)]
		except:
			bits = DioHashGen.preprocess(text, size)
			DioHashGen.textLoopup[text+str(size)] = bits
		
		if(size == 256):
			key = DioHashGen.key256
		elif(size == 512):
			key = DioHashGen.key512
		else:
			key = DioHashGen.key1024

		i = 0
		
		while(i<len(bits)):
			sample = bits[i:i+size]
			if(size == 256):
				try:
					key = DioHashGen.hashLookup[str(sample)+str(key)]
				except:
					key = block.encipher256(int(key), int(sample, 2))
					DioHashGen.hashLookup[str(sample)+str(key)] = key
			elif(size == 512):
				try:
					key = DioHashGen.hashLookup[str(sample)+str(key)]
				except:
					key = block.encipher512(int(key), int(sample, 2))
					DioHashGen.hashLookup[str(sample)+str(key)] = key
			else:
				try:
					key = DioHashGen.hashLookup[str(sample)+str(key)]
					DioHashGen.jk+=1
				except:
					key = block.encipher1024(int(key), int(sample, 2))
					DioHashGen.hashLookup[str(sample)+str(key)] = key
			i+=size
			
		return key
		
	def dio128(text):
		try:
			final = DioHashGen.numLookup[text+"256"]
		except:
			final = DioHashGen.DioHashGen(text, 256)
			DioHashGen.numLookup[text+"256"] = final
		return DioHashGenDigest(int(format(final, '0256b')[:128], 2))
		
	def dio256(text):
		try:
			final = DioHashGen.numLookup[text+"512"]
		except:
			final = DioHashGen.DioHashGen(text, 512)
			DioHashGen.numLookup[text+"512"] = final
		return DioHashGenDigest(int(format(final, '0512b')[:256], 2))
	
	def dio512(text):
		try:
			final = DioHashGen.numLookup[text+"1024"]
		except:
			final = DioHashGen.DioHashGen(text, 1024)
			DioHashGen.numLookup[text+"1024"] = final		
		return DioHashGenDigest(int(format(final, '01024b')[:512], 2))
	
	def sample1000Hashes():
		from datetime import datetime
		j = "a"
		dic = {}
		for i in range(7000):
			k = DioHashGen.dio512(j).hexdigest()
			try:
				print(dic[k], j)
				print("Found collision")
				return
			except:
				dic[k] = j
			j+="a"
if(__name__ == '__main__'):
	print(dio512("sukresh").hexdigest())

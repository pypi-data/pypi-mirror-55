class Submarine:

	'''
		---------------------
		Test Documentation

		นี่คือโปรแกรมสำหรับเรือดำน้ำ
		---------------------
	'''

	def __init__(self,price=15000,budget=100000):
		self.captain = 'Prawit'
		self.sub_name = 'Uncle I'
		self.price = price #Million
		self.kilo = 0
		self.budget = budget
		self.totalcost = 0

	def Missile(self):
		print('We are Department of Missile')

	def Calcommission(self):
		'''นี่ือฟังชั่นว่าลุงวิศวกร ได้คอมมิชชั่นเท่าไหร่'''
		pc = 10 # 10%
		percent = self.price * (pc/100)
		print('Loong! You got: {:,.2f} Million Baht'.format(percent))

	def Goto(self,enemypoint,distance):
		print(f"Let's go to {enemypoint} Distance: {distance} KM")
		self.kilo = self.kilo + distance
		#self.kilo += distance  #เขียนแบบย่อ
		self.Fuel()

	def Fuel(self):
		deisel = 20 # 20 baht/litre
		cal_feul_cost = self.kilo * deisel
		print('Current Fuel Cost: {:,d} Baht'.format(cal_feul_cost))
		self.totalcost += cal_feul_cost

	@property
	def BudgetRemaining(self):
		remaining = self.budget - self.totalcost
		print('Budget Remaining: {:,.2f} Baht'.format(remaining))
		return remaining


class ElectricSubmarine(Submarine):

	def __init__(self,price=10000,budget=400000):
		self.sub_name = 'Uncle III'
		self.battery_distance = 100000
		super().__init__(price,budget)

	def Battery(self):
		allbattery = 100
		calculate = (self.kilo / self.battery_distance) * 100	
		print('We have Battery Remaining: {}%'.format(allbattery-calculate))

	def Fuel(self):
		kilawattcost = 5 # 20 baht/litre
		cal_feul_cost = self.kilo * kilawattcost
		print('Current Power Cost: {:,d} Baht'.format(cal_feul_cost))
		self.totalcost += cal_feul_cost

if __name__ == '__main__':

	tesla = ElectricSubmarine(40000,2000000)
	print(tesla.captain)
	print(tesla.budget)
	tesla.Goto('Japan',10000)
	print(tesla.BudgetRemaining)
	tesla.Battery()

	print('----------------------')

	kongtabbok = Submarine(40000,2000000)
	print(kongtabbok.captain)
	print(kongtabbok.budget)
	kongtabbok.Goto('Japan',10000)
	print(kongtabbok.BudgetRemaining)


'''
kongtabreuw = Submarine(64561) #กองทัพเรือ
kongtabreuw.Missile()
print('Captain name: ',kongtabreuw.captain,kongtabreuw.sub_name)
print(kongtabreuw.sub_name)
print('----------------')
print(kongtabreuw.kilo)
kongtabreuw.Goto('China',7000)
print(kongtabreuw.kilo)
kongtabreuw.Fuel()
current_budget = kongtabreuw.BudgetRemaining
print(current_budget * 0.2)

kongtabreuw.Calcommission()
####################################3
print('------Submarine 2-----')
kongtabbok = Submarine(70000)
print('Before...')
print(kongtabbok.captain)
print('After...')
kongtabbok.captain = 'Srivara'
print(kongtabbok.captain)
'''
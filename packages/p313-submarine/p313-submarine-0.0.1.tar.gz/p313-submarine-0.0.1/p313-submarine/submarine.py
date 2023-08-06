# submarine.py

class Submarine:
    '''
    ------------------------
    Test Documentation...
    นี่คือโปรแกรมสำหรับเรือดำน้ำ
    ------------------------
    '''

    def __init__(self, price=15000, budget=100000):
        self.captain = 'Prawit'
        self.sub_name = 'Uncle I'
        self.price = price # Million
        self.kilo = 0
        self.budget = budget
        self.totalcost = 0
    
    def missile(self):
        print('We are Department of Missile')

    def calCommision(self):
        '''นี่คือฟังก์ชั่นลุงวิศกร ได้คอมมิชชั่นกี่บาท'''
        pc = 10 # 10%
        percent = self.price * (pc/100)
        print('Loong! Yot got: {} Million Baht'.format(percent))

    def goto(self, enemypoint, distance):
        print(f'Let\'s go to {enemypoint} Distance: {distance} km.')
        self.kilo = self.kilo + distance
        self.fuel()
        # self.kilo += distance

    def fuel(self):
        deisel = 20 # 20 baht/litre
        cal_fuel_cost = self.kilo * deisel
        print('Current Fuel Cost: {:,d} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

    @property
    def budgetRemaining(self):
        remaining = self.budget - self.totalcost
        print('Budget Remaining: {:,.2f} Baht'.format(remaining))
        return remaining

# inheritance from 'Submarine'
class ElectricSubmarine(Submarine):
    def __init__(self, price=15000, budget=100000):
        super().__init__(price, budget)
        self.battery_distance = 100000
        # Submarine can go out 100000 km/100 percent
        self.sub_name = 'Uncle III'

    def battery(self):
        allBattery = 100 # 100%
        calculate = (self.kilo/self.battery_distance)*100
        print('We have Battery Remaining: {}%'.format(allBattery-calculate))

    def fuel(self):
        kilowatCost = 5
        cal_fuel_cost = self.kilo * kilowatCost
        print('Current Power Cost: {:,d} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

# print(__name__)
# ถ้าเรียกใช้ไฟล์นี้ตรง ๆ __name__ จะเท่ากับ __main__
# แต่ถ้า import ไฟล์นี้ __name__ จะเท่ากับ ชื่อไฟล์ (submarine) ซึ่งจะทำให้เงื่อนไขไม่เป็นจริง แล้วคำสั่งใน if จะไม่ทำงาน
if __name__ == '__main__':
    tesla = ElectricSubmarine(40000, 2000000)
    print(tesla.captain)
    print(tesla.budget)
    tesla.goto('Japan', 10000)
    print(tesla.budgetRemaining)
    tesla.battery()

    print('---------------------')

    kongtabbok = Submarine(40000, 2000000)
    print(kongtabbok.captain)
    print(kongtabbok.budget)
    kongtabbok.goto('Japan', 10000)
    print(kongtabbok.budgetRemaining)

    '''
    print('-------Sub No.1----')
    kongtabreuw = Submarine(65400) # กองทับเรือ
    print(kongtabreuw.captain)
    print(kongtabreuw.sub_name)
    print('-------------------')
    print(kongtabreuw.kilo)
    kongtabreuw.goto('Chaina', 7000)
    print(kongtabreuw.kilo)
    kongtabreuw.fuel()
    current_budget = kongtabreuw.budgetRemaining
    print(current_budget * 0.2)

    kongtabreuw.calCommision()
    ###############################
    print('-------Sub No.2----')
    kongtabbok = Submarine(70000)
    print('Before...')
    print(kongtabreuw.captain)
    print('After...')
    kongtabbok.captain = 'Srivara'
    print(kongtabbok.captain)
    '''
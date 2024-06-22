from enum import Enum
import locale

def format_value(value):
    value = float(value)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    v = locale.format_string('%.2f', value, grouping=True)
    return f"R$ {v}"

class Bank:
  def __init__(self, name, interest, acf, cesh):
    self.name = name
    self.interest = interest
    self.acf = acf
    self.cesh = cesh 

  def get_interest(self, financing_value):
      return financing_value * self.interest / 12 

  def check_health(self):
    print(self.name, "Health Checked")
    print("Interest: ", self.interest)
    print("Acf: ", self.acf)
    print("Cesh: ", self.cesh.a, self.cesh.b, self.cesh.c, self.cesh.d)

  def get_cesh(self, financing_value, age):
    tax = (((self.cesh.a * (age ** 3) + self.cesh.b * (age ** 2) + self.cesh.c * age + self.cesh.d) / 100) / 12)
    return tax * financing_value;

  def simulate(self, amortization, financing_value, age):
    return "{:.2f}".format(amortization + self.get_interest(financing_value) + self.get_cesh(financing_value, age) + self.acf)

  def simulate_all_installments(self, financing_value, installments_number, age):
    amortization = financing_value / installments_number
    if age + (installments_number / 12) > 80:
      raise ValueError("The age of the customer plus the number of installments cannot exceed 80 years")

    res = []
    for i in range(1, installments_number + 1):
      if i == 1:
        simulate_value = float(self.simulate(amortization, financing_value, age))
        res.append([str(i), simulate_value])
      else:
        if i % 12 == 0:
          age += 1
          
        self.financing_value = float("{:.2f}".format(financing_value - amortization))
        simulate_value = float(self.simulate(amortization, financing_value, age))
        res.append([str(i), simulate_value])
    return res

class Cesh:
  def __init__(self, a, b, c, d):
    self.a = a 
    self.b = b 
    self.c = c 
    self.d = d 

class Banks(Enum):
    ITAU = Bank("Itau", 0.1099, 25, Cesh(0.0001, -0.0094, 0.2779, -2.0777))
    BRADESCO = Bank("Bradesco", 0.1169, 25, Cesh(0.0001, -0.0053, 0.0995, 0.4195))
    SANTANDER = Bank("Santander", 0.1229, 25, Cesh(0.0001, -0.0034, 0.0547, 0.1826))
    CAIXA = Bank("Caixa", 0.1115, 25, Cesh(0.0002, -0.0182, 0.4512, -2.5685))
    INTER = Bank("Inter", 0.1180, 25, Cesh(0.0001, -0.0034, 0.0547, 0.1826))

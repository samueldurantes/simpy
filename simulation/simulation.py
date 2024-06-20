from enum import Enum
from simulation.simulators.itau import Itau

SupportedBanks = Enum('Banks', ['ITAU'])

class Simulation:
  def __init__(self, bank: str, financing_value: float, installments_number: int, age: int):
    self.bank = bank.upper()
    self.financing_value = financing_value
    self.installments_number = installments_number
    self.age = age

  def run(self):
    if self.bank == SupportedBanks.ITAU.name:
      itau = Itau(self.financing_value, self.installments_number, self.age, "Personnalité")

      try:
          i = itau.simulate_all_installments()
          installments = list(map(lambda i: {"installment": i[0], "value": i[1]}, i))

          return {
              "bank": self.bank,
              "financing_value": self.financing_value,
              "installments_number": self.installments_number,
              "age": self.age,
              "installments": installments,
          }, 200
      except ValueError as error:
          return {"error": str(error)}, 400
    else:
      return {"error": "Bank not supported"}, 400

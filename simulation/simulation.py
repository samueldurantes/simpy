from enum import Enum
from simulation.simulators.itau import Itau
from simulation.bradesco.bradesco import Bradesco

class SupportedBanks(Enum):
    ITAU = Itau
    BRADESCO = Bradesco

class Simulation:
  def __init__(self, bank: str, financing_value: float, installments_number: int, age: int):
    self.bank = bank.upper()
    self.financing_value = financing_value
    self.installments_number = installments_number
    self.age = age

  def run(self):
      try:
        bank = SupportedBanks[self.bank].value(self.financing_value, self.installments_number, self.age, "Personnalité")
      except ValueError:
        return {"error": str(f"Bank '{self.bank}' is not supported.")}, 400

      try:
          i = bank.simulate_all_installments()
          installments = list(map(lambda i: {"installment": i[0], "value": i[1]}, i))

          return {
              "bank": self.bank, "financing_value": self.financing_value,
              "installments_number": self.installments_number,
              "age": self.age,
              "installments": installments,
          }, 200
      except ValueError as error:
          return {"error": str(error)}, 400

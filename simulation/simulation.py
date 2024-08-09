from simulation.banks.banks import Banks

class Simulation:
  def __init__(self, bank: str, financing_value: float, installments_number: int, age: int):
    self.bank = bank
    self.financing_value = financing_value
    self.installments_number = installments_number
    self.age = age

  def run(self):
      try:
        bank = Banks[self.bank.upper()].value
      except KeyError:
        return {"error": str(f"Bank '{self.bank}' is not supported. Access '/banks' to see valid bank keys")}, 400

      try:
        i = bank.simulate_all_installments(self.financing_value, self.installments_number, self.age)
        installments = list(map(lambda i: {"installment": i[0], "value": i[1]}, i))

        return {
            "bank": bank.name, 
            "financing_value": self.financing_value,
            "amortization": bank.modality,
            "installments_number": self.installments_number,
            "age": self.age,
            "anual_fee": bank.fee,
            "anual_cet": bank.interest,
            "installments": installments,
        }, 200
      except ValueError as error:
        return {"error": str(error)}, 400

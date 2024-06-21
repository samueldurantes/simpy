import locale

def format_value(value):
    value = float(value)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    v = locale.format_string('%.2f', value, grouping=True)
    return f"R$ {v}"

class Bradesco:
  def __init__(self, financing_value, installments_number, age, segment):
    self.financing_value = financing_value
    self.installments_number = installments_number
    self.age = age
    self.segment = segment

    self.amortization = float("{:.3f}".format(financing_value / installments_number))

  def get_interest(self):
      return self.financing_value * (0.1169 / 12)

  def get_cesh(self):
    a = 9.6117e-5;
    b = -5.3393e-3;
    c = 9.9455e-2;
    d = 0.4195;
    tax = (((a * (self.age ** 3) + b * (self.age ** 2) + c * self.age + d) / 100) / 12)
    return tax * self.financing_value;

  def simulate(self):
    interest = self.get_interest()
    cesh = self.get_cesh()
    tac = 25
    return "{:.2f}".format(self.amortization + interest + cesh + tac)

  def simulate_all_installments(self):
    if self.age + (self.installments_number / 12) > 80:
      raise ValueError("The age of the customer plus the number of installments cannot exceed 80 years")

    res = []
    for i in range(1, self.installments_number + 1):
      if i == 1:
        simulate_value = float(self.simulate())
        res.append([str(i), simulate_value])
      else:
        if i % 12 == 0:
          self.age += 1
          
        self.financing_value = float("{:.2f}".format(self.financing_value - self.amortization))
        simulate_value = float(self.simulate())
        res.append([str(i), simulate_value])
    return res

# Debug tools

# def print_table(dados):
#   # Convert all elements to strings
#   dados_str = [[str(celula) for celula in linha] for linha in dados]
#   larguras = [max(map(len, coluna)) for coluna in zip(*dados_str)]
#   linha_superior = '+-{}-+'.format('-+-'.join('-'*largura for largura in larguras))
#   print(linha_superior)
#   for linha in dados_str:
#     print('| {} |'.format(' | '.join(str(celula).ljust(largura) for largura, celula in zip(larguras, linha))))
#     print(linha_superior)

# if __name__ == '__main__':
#   i = Itau(1000000, 240, 20, "Personnalité")
#   a = i.simulate_all_installments()
#   b = list(map(lambda x: x[1], a))
#   c = functools.reduce(operator.add, b)

#   table = [["N˚ da Parcela", "Valor total da parcela"]] + a
#   print_table(table)

import locale

def format_value(value):
    value = float(value)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    v = locale.format_string('%.2f', value, grouping=True)
    return f"R$ {v}"

class Itau:
  def __init__(self, financing_value, installments_number, age, segment):
    self.financing_value = financing_value
    self.installments_number = installments_number
    self.age = age
    self.segment = segment

    self.amortization = float("{:.3f}".format(financing_value / installments_number))

  def get_interest(self):
    match self.segment:
      case "Personnalité":
        return self.financing_value * (0.8325 / 100)
      case "Private":
        return self.financing_value * (0.824166667 / 100)
      case "Uniclass":
        return self.financing_value * (0.874166667 / 100)
      case "Agências":
        return self.financing_value * ((10.4724245 / 12) / 100)
      case _:
        return self.financing_value * (0.915833333 / 100)

  def get_mip(self):
    d = {
      18: 0.0103100000, 19: 0.0103100000, 20: 0.0103100000, 21: 0.0103100000,
      22: 0.0103100000, 23: 0.0103100000, 24: 0.0103100000, 25: 0.0103100000,
      26: 0.0103100000, 27: 0.0103100000, 28: 0.0103100000, 29: 0.0103100000,
      30: 0.0103100000, 31: 0.0158100000, 32: 0.0161200000, 33: 0.0164500000,
      34: 0.0168300000, 35: 0.0174600000, 36: 0.0247700000, 37: 0.0258900000,
      38: 0.0273000000, 39: 0.0290300000, 40: 0.0311400000, 41: 0.0319800000,
      42: 0.0318500000, 43: 0.0348600000, 44: 0.0382900000, 45: 0.0421300000,
      46: 0.0491200000, 47: 0.0539800000, 48: 0.0591700000, 49: 0.0647200000,
      50: 0.0705800000, 51: 0.0801300000, 52: 0.0869200000, 53: 0.0940300000,
      54: 0.1015400000, 55: 0.1095200000, 56: 0.1324200000, 57: 0.1427500000,
      58: 0.1539400000, 59: 0.1663700000, 60: 0.1804400000, 61: 0.2376400000,
      62: 0.2602300000, 63: 0.2863100000, 64: 0.3162500000, 65: 0.3503300000,
      66: 0.3499300000, 67: 0.3503000000, 68: 0.3663200000, 69: 0.4076700000,
      70: 0.4536600000, 71: 0.4522000000, 72: 0.5028300000, 73: 0.5586700000,
      74: 0.6204800000, 75: 0.6892600000, 76: 0.8086700000, 77: 0.8984100000,
      78: 1.0616500000, 79: 1.1588600000, 80: 1.2868200000,
    }

    return self.financing_value * (d[self.age] / 100)

  def simulate(self):
    interest = self.get_interest()
    mip = self.get_mip()
    dfi = 83.10
    tac = 25
    return "{:.2f}".format(self.amortization + interest + mip + dfi + tac)

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
        else:
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

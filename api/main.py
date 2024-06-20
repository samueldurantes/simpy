from flask import Flask, request, jsonify
from pydantic import BaseModel, validator, ValidationError
# from simulation.simulation import Simulation

app = Flask(__name__)

class SimulationParams(BaseModel):
    bank: str
    financing_value: float
    installments_number: int
    age: int
    
    @validator('financing_value')
    def validate_financing_value(cls, v):
        if v < 100000: 
            raise ValueError('Financing value must be greater than 100000')
        return v

    @validator('installments_number')
    def validate_installments_number(cls, v):
        if v not in [60, 90, 120, 150, 180, 240, 360, 420]:
            raise ValueError('Invalid installments number, must be one of 60, 90, 120, 150, 180, 240, 360, 420')
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 80:
            raise ValueError('Age must be between 18 and 80')
        return v

@app.route("/simulations")
def simulations():
  bank = request.args.get('bank')
  financing_value = request.args.get('financing_value')
  installments_number = request.args.get('installments_number')
  age = request.args.get('age')

  if not bank or not financing_value or not installments_number or not age:
    return jsonify({"error": "It's necessary specify all these parameters: bank, financing_value, installments_number, age"}), 400

  try:
    simulation_params = SimulationParams(
      bank=bank,
      financing_value=financing_value,
      installments_number=installments_number,
      age=age
    )
  except ValidationError as e:
    return jsonify({"error": e.errors()[-1]['msg']}), 400
  
  # simulation = Simulation(
  #   bank=simulation_params.bank,
  #   financing_value=simulation_params.financing_value,
  #   installments_number=simulation_params.installments_number,
  #   age=simulation_params.age
  # )

  # result, code = simulation.run()

  return jsonify({"hello": 'world'}), 200

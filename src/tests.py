import main
from service import DataBrokerService

main.validate_inputs(['PACIENTES', 'PRESTADORES'])

f = DataBrokerService()
ret = main.process_response(f.fetch(['PACIENTES', 'PRESTADORES']), 200)
print(ret)


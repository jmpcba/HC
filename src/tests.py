from services import DataBrokerService

service = DataBrokerService()
service.fetch_tables(('PRESTADORES',))
a = service.response.service_response
print(str(a))

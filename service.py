from api import API
import re

class SPService:
    """
    Conecta com o webservice do Detran-SP.
    """

    def __init__(self, **kwargs):
        """
        Construtor.
        """

        self.params = kwargs
        self.params["license_plate"] = self.convert_license_plate(self.params["license_plate"])
   
    def get_json_response(self, method):
        """
        Pega a resposta da requisição em json.
        """
        api = API(self.params["license_plate"], self.params["renavam"], method)
        return api.fetch()
    
    def convert_license_plate(self,license_plate):
        """
        Retorna a placa do padrão MERCOSUL convertida para o padrão antigo
        ou a placa original caso a placa fornecida esteja no formato incorreto
        """
        letter_position_to_change = 4
        if(re.match("[A-Z]{3}[0-9][A-Z][0-9]{2}",license_plate)):
            fifth_letter = license_plate[letter_position_to_change]
            switcher = {
                "A": "0",
                "B": "1",
                "C": "2",
                "D": "3",
                "E": "4",
                "F": "5",
                "G": "6",
                "H": "7",
                "I": "8",
                "J": "9",
            }
            new_letter = switcher.get(fifth_letter)
            if(new_letter != None):
                converted_license_plate = license_plate[:letter_position_to_change] + new_letter + license_plate[letter_position_to_change+1:]
                return converted_license_plate
        return license_plate


    def debt_search(self):
        """
        Pega os débitos de acordo com a opção passada.
        """
        if self.params['debt_option'] == 'ticket':
            response_json = self.get_json_response("ConsultaMultas")

        elif self.params['debt_option'] == 'ipva':
            response_json = self.get_json_response("ConsultaIPVA")

        elif self.params['debt_option'] == 'dpvat':
            response_json = self.get_json_response("ConsultaDPVAT")

        elif self.params['debt_option'] == 'licensing':
            response_json = self.get_json_response("ConsultaLicenciamento")
                
        elif self.params['debt_option'] == 'all':
            response_json_tickets = self.get_json_response("ConsultaMultas")
            response_json_ipva = self.get_json_response("ConsultaIPVA")
            response_json_dpvat = self.get_json_response("ConsultaDPVAT")
            response_json_licensing= self.get_json_response("ConsultaLicenciamento")           
        else:
            raise Exception("opção inválida")

        if(self.params['debt_option'] == 'all'):
            debts = {
            'IPVAs': response_json_ipva.get('IPVAs') or {},
            'DPVATs': response_json_dpvat.get('DPVATs') or {},
            'Multas': response_json_tickets.get('Multas') or {},
            'Licenciamento': response_json_licensing or {},
            }
        else:
            debts = {
            'IPVAs': response_json.get('IPVAs') or {},
            'DPVATs': response_json.get('DPVATs') or {},
            'Multas': response_json.get('Multas') or {},
            'Licenciamento': response_json or {},
        }
        


        for debt in debts:
            if debts[debt] == {}:
                debts[debt] = None

        return debts

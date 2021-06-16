from flask import Flask , request
import json
import sys
from service import SPService
from myparser import SPParser

"""
flask run
"""
app = Flask("MyApi")
@app.route("/consultar-debitos", methods=["POST"])
def consultar_debitos():

    request_json = request.get_json()
    debt_option = request_json.get('debt_option')
    license_plate = request_json.get("license_plate")
    renavam = request_json.get("renavam")

    if(debt_option == None):
        return json.dumps("debt_option não informado", ensure_ascii=False)
    elif(license_plate == None):
        return json.dumps("license_plate não informado", ensure_ascii=False)
    elif(renavam == None):   
        return json.dumps("renavam não informado", ensure_ascii=False)

    service = SPService(
        license_plate=license_plate,
        renavam=renavam,
        debt_option=debt_option
    )
    try:
        search_result = service.debt_search()
    except Exception as exc:
        return json.dumps(str(exc), ensure_ascii=False)

    parser = SPParser(search_result)

    if debt_option == "ticket":
        result = parser.collect_ticket_debts()
    elif debt_option == "ipva":
        result = parser.collect_ipva_debts()
    elif debt_option == "dpvat":
        result = parser.collect_insurance_debts()
    elif debt_option == "licensing":
        result = parser.collect_licensing_debts()
    elif debt_option == "all":
        result = parser.collect_all_debts()
    else:
        return json.dumps("debt_option inválido",ensure_ascii=False)

    return json.dumps(result, indent=4, ensure_ascii=False)
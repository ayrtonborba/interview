from service import SPService
import pytest

def test_search_ticket_not_found_plate():
    service = SPService(
        license_plate="license_plate",
        renavam="renavam",
        debt_option="ticket"
    )
    with pytest.raises(Exception,match=r"veículo não encontrado") as excinfo:
        result = service.debt_search() 

def test_search_ticket_found_plate():
    service = SPService(
        license_plate="ABC1234",
        renavam="11111111111",
        debt_option="ticket"
    )
    result = service.debt_search() 
    assert len(result) == 4


def test_wrongly_formatted_license_plate_conversion():
    original_license_plate = "A1BCC34"
    service = SPService(
        license_plate=original_license_plate,
        renavam="11111111111",
        debt_option="all"
    )
    converted_plate = service.convert_license_plate(original_license_plate)
    assert converted_plate == "A1BCC34"

def test_well_formatted_license_plate_conversion():
    original_license_plate = "ABC1C34"
    service = SPService(
        license_plate=original_license_plate,
        renavam="11111111111",
        debt_option="all"
    )
    converted_plate = service.convert_license_plate(original_license_plate)
    assert converted_plate == "ABC1234"

def test_search_licensing():
    original_license_plate = "ABC1C34"
    service = SPService(
        license_plate=original_license_plate,
        renavam="11111111111",
        debt_option="licensing"
    )
    result = service.debt_search()
    assert len(result) == 4

def test_search_all_debts():
    service = SPService(
        license_plate="ABC1234",
        renavam="11111111111",
        debt_option="all"
    )
    result = service.debt_search()
    assert len(result) == 4

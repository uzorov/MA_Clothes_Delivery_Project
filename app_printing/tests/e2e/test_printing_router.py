# import time
# import pytest
# import requests
# from uuid import UUID, uuid4
# from datetime import datetime
#
# from app.models.printing import Printing, PrintingStatuses
#
# time.sleep(5)
# base_url = 'postgresql://postgres:password@actual_pr678-postgres-printing-1:5433/api'
#
#
# @pytest.fixture(scope='session')
# def first_printing_data() -> tuple[UUID, datetime]:
#     return (uuid4(), datetime.now())
#
#
# @pytest.fixture(scope='session')
# def second_printing_data() -> tuple[UUID, datetime]:
#     return (uuid4(), datetime.now())
#
#
# def test_get_printings_empty() -> None:
#     assert requests.get(f'{base_url}/printing').json() == []
#
#
# def test_add_printing_first_success(
#         first_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id, date = first_printing_data
#     printing = Printing.model_validate(requests.post(f'{base_url}/printing', json={
#         'id': printing_id.hex,
#         'date': str(date)
#     }).json())
#     assert printing.id == printing_id
#     assert printing.status == PrintingStatuses.AWAITING
#     assert printing.date == date
#
#
# def test_add_printing_first_repeat_error(
#         first_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id, date = first_printing_data
#     result = requests.post(f'{base_url}/printing', json={
#         'id': printing_id.hex,
#         'date': str(date)
#     })
#
#     assert result.status_code == 400
#
#
# def test_cancel_printing_not_found() -> None:
#     result = requests.post(f'{base_url}/printing/{uuid4()}/cancel')
#
#     assert result.status_code == 404
#
#
# def test_finish_printing_not_found() -> None:
#     result = requests.post(f'{base_url}/printing/{uuid4()}/finish')
#
#     assert result.status_code == 404
#
#
# def test_begin_printing_not_found() -> None:
#     result = requests.post(f'{base_url}/printing/{uuid4()}/begin')
#
#     assert result.status_code == 404
#
#
# def test_cancel_printing_success(
#         first_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id, date = first_printing_data
#     printing = Printing.model_validate_json(requests.post(
#         f'{base_url}/printing/{printing_id}/cancel').text)
#
#     assert printing.id == printing_id
#     assert printing.date == date
#     assert printing.status == PrintingStatuses.CANCELED
#
#
# def test_finish_printing_status_error(
#         first_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id = first_printing_data[0]
#     result = requests.post(f'{base_url}/printing/{printing_id}/finish')
#
#     assert result.status_code == 400
#
#
# def test_begin_printing_status_error(
#         first_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id = first_printing_data[0]
#     result = requests.post(f'{base_url}/printing/{printing_id}/begin')
#
#     assert result.status_code == 400
#
#
# def test_add_printing_second_success(
#         second_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id, date = second_printing_data
#     printing = Printing.model_validate(requests.post(f'{base_url}/printing', json={
#         'id': printing_id.hex,
#         'date': str(date)
#     }).json())
#     assert printing.id == printing_id
#     assert printing.status == PrintingStatuses.AWAITING
#     assert printing.date == date
#
#
# def test_get_printings_full(
#         first_printing_data: tuple[UUID, datetime],
#         second_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printings = [Printing.model_validate(
#         d) for d in requests.get(f'{base_url}/printing').json()]
#     assert len(printings) == 2
#     assert printings[0].id == first_printing_data[0]
#     assert printings[1].id == second_printing_data[0]
#
#
# def test_begin_printing_success(
#         second_printing_data: tuple[UUID, datetime]
# ) -> None:
#     printing_id, date = second_printing_data
#     printing = Printing.model_validate_json(requests.post(
#         f'{base_url}/printing/{printing_id}/begin').text)
#     assert printing.id == printing_id
#     assert printing.status == PrintingStatuses.IN_PROCESS
#     assert printing.date == date

# from pact import *
#
#
# @base_uri('localhost:1234')
# @service_consumer('Library App')
# @has_pact_with('Books Service')
# class TestBooksService():
#
#     expected_response = {
#         'status': 200,
#         'headers': {'Content-Type': 'application/json'},
#         'body': {
#             'id': '123',
#             'title': 'A Fortune-Teller Told Me'
#         }
#     }
#
#     @given('some books exist')
#     @upon_receiving('a request for a book')
#     @with_request({'method': 'get', 'path': '/books/123'})
#     @will_respond_with(expected_response)
#     def test_get_book(self):
#         pass

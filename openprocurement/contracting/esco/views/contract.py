# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    context_unpack,
    json_view
)

from openprocurement.contracting.api.utils import (
    contractingresource,
    save_contract
)
from openprocurement.contracting.core.utils import apply_patch
from openprocurement.contracting.core.validation import (
    validate_patch_contract_data,
    validate_contract_update_not_in_allowed_status,
)
from openprocurement.contracting.common.views.contract import (
    ContractResource as BaseContractResource,
)
from openprocurement.contracting.esco.validation import (
    validate_terminate_contract_amount_paid,
    validate_update_contract_start_date,
    validate_update_contract_end_date
)

from openprocurement.contracting.esco.utils import update_milestones_dates_and_statuses


@contractingresource(name='esco:Contract',
                     path='/contracts/{contract_id}',
                     contractType='esco',
                     description="Contract")
class ContractResource(BaseContractResource):
    """ ESCO Contract Resource """

    @json_view(content_type="application/json", permission='edit_contract',
               validators=(validate_patch_contract_data,
                           validate_contract_update_not_in_allowed_status,
                           validate_terminate_contract_amount_paid,
                           validate_update_contract_start_date,
                           validate_update_contract_end_date))
    def patch(self):
        """Esco Contract Edit (partial)

        For example here is how procuring entity can change number of items to be procured and total Value of a tender:

        .. sourcecode:: http

            PATCH /contracts/de46983cea7945939bae90862d54693f HTTP/1.1
            Host: example.com
            Accept: application/json

            {
                "data": {
                    "period": {
                        u'endDate': '2029-04-27T09:58:56.919991+03:00',
                        u'startDate': u'2018-04-27T09:58:56.919991+03:00'
                    }
                }
            }

        And here is the response to be expected:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            {
            u'data': {
               u'NBUdiscountRate': 0.135,
               u'amountPaid': {u'amount': 100000.0,
                               u'currency': u'UAH',
                               u'valueAddedTaxIncluded': True},
               u'awardID': u'29c01dd058c347f38e381f13d4a6a118',
               u'changes': [{u'date': u'2018-04-27T09:59:02.794216+03:00',
                             u'id': u'78679cfa4c544b5db8069e4e8999a491',
                             u'rationale': u'\u043f\u0440\u0438\u0447\u0438\u043d\u0430 \u0437\u043c\u0456\u043d\u0438 \u0443\u043a\u0440',
                             u'rationaleTypes': [u'itemPriceVariation'],
                             u'rationale_en': u'change cause en',
                             u'status': u'pending'}],
               u'contractID': u'UA-2017-11-21-001567-c-a1',
               u'contractNumber': u'17',
               u'contractType': u'esco',
               u'dateModified': u'2018-04-27T10:02:21.499264+03:00',
               u'dateSigned': u'2018-04-27T09:58:56.919991+03:00',
               u'description': u'',
               u'id': u'de46983cea7945939bae90862d54693f',
               u'items': [{u'additionalClassifications': [{u'description': u'\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435 \u043d\u043e\u0440\u043c\u044b \u0438 \u0434\u0440\u0443\u0433\u043e\u0435',
                                                           u'id': u'000',
                                                           u'scheme': u'specialNorms'}],
                           u'classification': {u'description': u'\u041d\u0435 \u0432\u0456\u0434\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0435 \u0432 \u0456\u043d\u0448\u0438\u0445 \u0440\u043e\u0437\u0434\u0456\u043b\u0430\u0445',
                                               u'id': u'99999999-9',
                                               u'scheme': u'\u0414\u041a021'},
                           u'deliveryAddress': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                u'locality': u'\u0421\u0443\u043c\u0438',
                                                u'postalCode': u'40007',
                                                u'region': u'\u0421\u0443\u043c\u0441\u044c\u043a\u0430 \u043e\u0431\u043b.',
                                                u'streetAddress': u'\u041e\u0445\u0442\u0438\u0440\u0441\u044c\u043a\u0430, 21'},
                           u'description': u'\u0415\u041d\u0435\u0440\u0433\u043e\u0441\u0435\u0440\u0432\u0456\u0441 \u0431\u0443\u0434\u0456\u0432\u043b\u0456 \u041a\u043e\u043c\u0443\u043d\u0430\u043b\u044c\u043d\u043e\u0457 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u0438 \u0421\u0443\u043c\u0441\u044c\u043a\u0430 \u0437\u0430\u0433\u0430\u043b\u044c\u043d\u043e\u043e\u0441\u0432\u0456\u0442\u043d\u044f \u0448\u043a\u043e\u043b\u0430 \u0406-\u0406\u0406\u0406 \u0441\u0442\u0443\u043f\u0435\u043d\u0456\u0432 \u2116 26 \u043c. \u0421\u0443\u043c\u0438, \u0421\u0443\u043c\u0441\u044c\u043a\u043e\u0457 \u043e\u0431\u043b\u0430\u0441\u0442\u0456',
                           u'description_en': u'Energy service of the public institution building of Sumy secondary school Nr 26',
                           u'id': u'660e66a4ffd0486f8f90041f36105f05'}],
               u'milestones': [{u'amountPaid': {u'amount': 100000.0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.922929+03:00',
                                u'dateModified': u'2018-04-27T09:59:00.931103+03:00',
                                u'description': u'Milestone #1 of year 2018',
                                u'id': u'0458c0495691406bb6a01f98b2aa2429',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2018-04-27T09:58:56.919991+03:00'},
                                u'sequenceNumber': 1,
                                u'status': u'pending',
                                u'title': u'Milestone #1 of year 2018',
                                u'value': {u'amount': 0,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923050+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923050+03:00',
                                u'description': u'Milestone #2 of year 2019',
                                u'id': u'cf3fec09adcf405a8629e7912006c20b',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2019-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 2,
                                u'status': u'scheduled',
                                u'title': u'Milestone #2 of year 2019',
                                u'value': {u'amount': 164677.28,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923203+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923203+03:00',
                                u'description': u'Milestone #3 of year 2020',
                                u'id': u'17b94728909040ffa2a73c5d2ecd96b8',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2020-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 3,
                                u'status': u'scheduled',
                                u'title': u'Milestone #3 of year 2020',
                                u'value': {u'amount': 207592.22,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923341+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923341+03:00',
                                u'description': u'Milestone #4 of year 2021',
                                u'id': u'1d9de5c307284ce19e0035ef25e0a42f',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2021-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 4,
                                u'status': u'scheduled',
                                u'title': u'Milestone #4 of year 2021',
                                u'value': {u'amount': 207592.22,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923480+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923480+03:00',
                                u'description': u'Milestone #5 of year 2022',
                                u'id': u'04747c0d72444a8a8dfa602bb5c7e7c1',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2022-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 5,
                                u'status': u'scheduled',
                                u'title': u'Milestone #5 of year 2022',
                                u'value': {u'amount': 207592.22,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923622+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923622+03:00',
                                u'description': u'Milestone #6 of year 2023',
                                u'id': u'0f844c8a686e491b81ef701543a43831',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2023-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 6,
                                u'status': u'scheduled',
                                u'title': u'Milestone #6 of year 2023',
                                u'value': {u'amount': 207592.22,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923757+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923757+03:00',
                                u'description': u'Milestone #7 of year 2024',
                                u'id': u'833977506d0c49afbd071c81b69d5acd',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2024-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 7,
                                u'status': u'scheduled',
                                u'title': u'Milestone #7 of year 2024',
                                u'value': {u'amount': 207592.22,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.923892+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.923892+03:00',
                                u'description': u'Milestone #8 of year 2025',
                                u'id': u'38a931d02bf24bbca30f60ac1e527a96',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2025-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 8,
                                u'status': u'scheduled',
                                u'title': u'Milestone #8 of year 2025',
                                u'value': {u'amount': 35262.24,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.924039+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.924039+03:00',
                                u'description': u'Milestone #9 of year 2026',
                                u'id': u'143506651440433c8162283e930114ee',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2026-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 9,
                                u'status': u'scheduled',
                                u'title': u'Milestone #9 of year 2026',
                                u'value': {u'amount': 0,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.924145+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.924145+03:00',
                                u'description': u'Milestone #10 of year 2027',
                                u'id': u'04db12f9015a400eb04bbfafc8a2367c',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2027-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 10,
                                u'status': u'scheduled',
                                u'title': u'Milestone #10 of year 2027',
                                u'value': {u'amount': 0,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.924249+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.924249+03:00',
                                u'description': u'Milestone #11 of year 2028',
                                u'id': u'7e31a15694ff494eb04e728937aec0dc',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2028-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 11,
                                u'status': u'scheduled',
                                u'title': u'Milestone #11 of year 2028',
                                u'value': {u'amount': 0,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}},
                               {u'amountPaid': {u'amount': 0,
                                                u'currency': u'UAH',
                                                u'valueAddedTaxIncluded': True},
                                u'date': u'2018-04-27T09:58:56.924352+03:00',
                                u'dateModified': u'2018-04-27T09:58:56.924352+03:00',
                                u'description': u'Milestone #12 of year 2029',
                                u'id': u'd981d1e2389f4ccabe676cca228d3205',
                                u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                                            u'startDate': u'2029-01-01T00:00:00+02:02'},
                                u'sequenceNumber': 12,
                                u'status': u'scheduled',
                                u'title': u'Milestone #12 of year 2029',
                                u'value': {u'amount': 0,
                                           u'currency': u'UAH',
                                           u'valueAddedTaxIncluded': True}}],
               u'owner': u'broker',
               u'period': {u'endDate': u'2029-04-27T09:58:56.919991+03:00',
                           u'startDate': u'2018-04-27T09:58:56.919991+03:00'},
               u'procuringEntity': {u'additionalContactPoints': [{u'name': u'\u0414\u0435\u0440\u0436\u0430\u0432\u043d\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0456\u043d\u043d\u044f \u0441\u043f\u0440\u0430\u0432\u0430\u043c\u04382',
                                                                  u'telephone': u'0440000001'}],
                                    u'address': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                                 u'locality': u'',
                                                 u'postalCode': u'',
                                                 u'region': u'',
                                                 u'streetAddress': u'01004, \u043c.\u041a\u0438\u0457\u0432, \u0411\u0415\u0421\u0421\u0410\u0420\u0410\u0411\u0421\u042c\u041a\u0410 \u041f\u041b\u041e\u0429\u0410, \u0431\u0443\u0434\u0438\u043d\u043e\u043a 9/1 \u0411, \u043e\u0444\u0456\u0441 2'},
                                    u'contactPoint': {u'availableLanguage': u'en',
                                                      u'email': u'e.zhogan@ksteplo.com.ua',
                                                      u'name': u'\u0422\u041e\u0412\u0410\u0420\u0418\u0421\u0422\u0412\u041e \u0417 \u041e\u0411\u041c\u0415\u0416\u0415\u041d\u041e\u042e \u0412\u0406\u0414\u041f\u041e\u0412\u0406\u0414\u0410\u041b\u042c\u041d\u0406\u0421\u0422\u042e "\u0404\u0412\u0420\u041e\u041f\u0415\u0419\u0421\u042c\u041a\u0410 \u0415\u041d\u0415\u0420\u0413\u041e\u0421\u0415\u0420\u0412\u0406\u0421\u041d\u0410 \u041a\u041e\u041c\u041f\u0410\u041d\u0406\u042f"',
                                                      u'telephone': u'+380933907440'},
                                    u'identifier': {u'id': u'40957551',
                                                    u'legalName': u'\u0422\u041e\u0412\u0410\u0420\u0418\u0421\u0422\u0412\u041e \u0417 \u041e\u0411\u041c\u0415\u0416\u0415\u041d\u041e\u042e \u0412\u0406\u0414\u041f\u041e\u0412\u0406\u0414\u0410\u041b\u042c\u041d\u0406\u0421\u0422\u042e "\u0404\u0412\u0420\u041e\u041f\u0415\u0419\u0421\u042c\u041a\u0410 \u0415\u041d\u0415\u0420\u0413\u041e\u0421\u0415\u0420\u0412\u0406\u0421\u041d\u0410 \u041a\u041e\u041c\u041f\u0410\u041d\u0406\u042f"',
                                                    u'scheme': u'UA-EDR'},
                                    u'name': u'\u0422\u041e\u0412\u0410\u0420\u0418\u0421\u0422\u0412\u041e \u0417 \u041e\u0411\u041c\u0415\u0416\u0415\u041d\u041e\u042e \u0412\u0406\u0414\u041f\u041e\u0412\u0406\u0414\u0410\u041b\u042c\u041d\u0406\u0421\u0422\u042e "\u0404\u0412\u0420\u041e\u041f\u0415\u0419\u0421\u042c\u041a\u0410 \u0415\u041d\u0415\u0420\u0413\u041e\u0421\u0415\u0420\u0412\u0406\u0421\u041d\u0410 \u041a\u041e\u041c\u041f\u0410\u041d\u0406\u042f"'},
               u'status': u'active',
               u'suppliers': [{u'address': {u'countryName': u'\u0423\u043a\u0440\u0430\u0457\u043d\u0430',
                                            u'locality': u'',
                                            u'postalCode': u'',
                                            u'region': u'',
                                            u'streetAddress': u'01004, \u043c.\u041a\u0438\u0457\u0432, \u0411\u0415\u0421\u0421\u0410\u0420\u0410\u0411\u0421\u042c\u041a\u0410 \u041f\u041b\u041e\u0429\u0410, \u0431\u0443\u0434\u0438\u043d\u043e\u043a 9/1 \u0411, \u043e\u0444\u0456\u0441 2'},
                               u'contactPoint': {u'email': u'e.zhogan@ksteplo.com.ua',
                                                 u'name': u'\u0422\u041e\u0412\u0410\u0420\u0418\u0421\u0422\u0412\u041e \u0417 \u041e\u0411\u041c\u0415\u0416\u0415\u041d\u041e\u042e \u0412\u0406\u0414\u041f\u041e\u0412\u0406\u0414\u0410\u041b\u042c\u041d\u0406\u0421\u0422\u042e "\u0404\u0412\u0420\u041e\u041f\u0415\u0419\u0421\u042c\u041a\u0410 \u0415\u041d\u0415\u0420\u0413\u041e\u0421\u0415\u0420\u0412\u0406\u0421\u041d\u0410 \u041a\u041e\u041c\u041f\u0410\u041d\u0406\u042f"',
                                                 u'telephone': u'+380933907440'},
                               u'identifier': {u'id': u'40957551',
                                               u'legalName': u'\u0422\u041e\u0412\u0410\u0420\u0418\u0421\u0422\u0412\u041e \u0417 \u041e\u0411\u041c\u0415\u0416\u0415\u041d\u041e\u042e \u0412\u0406\u0414\u041f\u041e\u0412\u0406\u0414\u0410\u041b\u042c\u041d\u0406\u0421\u0422\u042e "\u0404\u0412\u0420\u041e\u041f\u0415\u0419\u0421\u042c\u041a\u0410 \u0415\u041d\u0415\u0420\u0413\u041e\u0421\u0415\u0420\u0412\u0406\u0421\u041d\u0410 \u041a\u041e\u041c\u041f\u0410\u041d\u0406\u042f"',
                                               u'scheme': u'UA-EDR'},
                               u'name': u'\u0422\u041e\u0412\u0410\u0420\u0418\u0421\u0422\u0412\u041e \u0417 \u041e\u0411\u041c\u0415\u0416\u0415\u041d\u041e\u042e \u0412\u0406\u0414\u041f\u041e\u0412\u0406\u0414\u0410\u041b\u042c\u041d\u0406\u0421\u0422\u042e "\u0404\u0412\u0420\u041e\u041f\u0415\u0419\u0421\u042c\u041a\u0410 \u0415\u041d\u0415\u0420\u0413\u041e\u0421\u0415\u0420\u0412\u0406\u0421\u041d\u0410 \u041a\u041e\u041c\u041f\u0410\u041d\u0406\u042f"'}],
               u'tender_id': u'4f90c49aa1684769b9a41c8196d875fe',
               u'title': u'New Title',
               u'value': {u'amount': 1237900.62,
                          u'amountPerformance': 447361.33,
                          u'annualCostsReduction': [0,
                                                    178997.04,
                                                    225643.72,
                                                    225643.72,
                                                    225643.72,
                                                    225643.72,
                                                    225643.72,
                                                    225643.72,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47,
                                                    141782.47],
                          u'contractDuration': {u'days': 310, u'years': 6},
                          u'currency': u'UAH',
                          u'valueAddedTaxIncluded': True,
                          u'yearlyPaymentsPercentage': 0.92}
                          }
            }

        """
        if 'period' in self.request.validated['data'] and \
                self.context.period.endDate.isoformat() != self.request.validated['data']['period']['endDate']:
            update_milestones_dates_and_statuses(self.request)
        contract = self.request.validated['contract']
        apply_patch(self.request, save=False, src=self.request.validated['contract_src'])

        # validate_terminate_contract_without_amountPaid(self.request)

        if save_contract(self.request):
            self.LOGGER.info('Updated contract {}'.format(contract.id),
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'contract_patch'}))
            return {'data': contract.serialize('view')}

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APIClient

from afi_backend.tickets.api.views import TicketViewSet
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


# class TestTicketDetailView:
#     def test_get_ticket(self):
#         factory = APIRequestFactory()
#         ticket = TicketFactory()
#         ticket.save()
#         test_user = UserFactory()

#         request = factory.get("/api/tickets/")
#         force_authenticate(request, test_user)
#         view = TicketViewSet.as_view(actions={'get': 'list'})
#         response = view(request)
#         breakpoint()
#         # d = {
#         #     'results': [],
#         #     'meta': {
#         #         'pagination':
#         #         OrderedDict([('page', 1), ('pages', 1), ('count', 0)])
#         #     },
#         #     'links':
#         #     OrderedDict([
#         #         ('first',
#         #          'http://testserver/api/tickets/30?page%5Bnumber%5D=1'),
#         #         ('last',
#         #          'http://testserver/api/tickets/30?page%5Bnumber%5D=1'),
#         #         ('next', None), ('prev', None)
#         #     ])
#         # }
#         assert False

#         # assert response.data == {"payment_url": test_url}

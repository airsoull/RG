# standar libraries
import json

# django
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

# models
from api.models import Currency


class ScraperAPI(View):
    def get(self, *args, **kwargs):
        return JsonResponse(Currency.get_currencies_serializer())

    def post(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body)
            return JsonResponse(
                Currency.create_currency_from_coinmarketcap(data=data)
            )
        except Exception as e:
            return HttpResponseBadRequest(
                json.dumps({'error': str(e)}),
                content_type='application/json'
            )

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

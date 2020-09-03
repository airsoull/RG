# standar libraries
import json

# django
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# models
from api.models import Currency


class ScraperAPI(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return JsonResponse(Currency.get_currencies_serializer())

    def post(self, *args, **kwargs):
        try:
            data = self.get_data()
            return JsonResponse(
                Currency.create_currency_from_coinmarketcap(data=data)
            )
        except Exception as e:
            return self.get_bad_request(e)

    def put(self, *args, **kwargs):
        try:
            data = self.get_data()
            return JsonResponse(
                Currency.update_frequency(data=data)
            )
        except Exception as e:
            return self.get_bad_request(e)

    def delete(self, *args, **kwargs):
        pass

    def get_data(self):
        return json.loads(self.request.body)

    def get_bad_request(self, error):
        return HttpResponseBadRequest(
            json.dumps({'error': str(error)}),
            content_type='application/json'
        )

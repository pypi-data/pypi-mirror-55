__all__ = [
    'GenericInitiatePaymentView',
    'InitiatePaymentView'
]
from django.shortcuts import render, Http404
from django.conf import settings as django_settings
from django.views import View

from paytm import conf as paytm_conf


class GenericInitiatePaymentView(View):
    conf = paytm_conf

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    def get_merchant_credentials(self):
        """
        :return: dict({
            MID
            WEBSITE
            INDUSTRY_TYPE_ID
        })
        """

        return self.conf.merchant_credentials

    def get_channel(self):
        """
        :return: str('WEB' | 'WAP')
        """
        return 'WEB'

    def get_payload(self):
        pass

    def post(self, request):
        self.request = request

        return render(request, 'paytm/checkout/redirect.html', self.get_payload())


class InitiatePaymentView(GenericInitiatePaymentView):
    """Wrapper for testing"""

    def get(self, request):
        if not django_settings.DEBUG:
            raise Http404

        return render(request, 'paytm/checkout/index.html')

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.management import call_command
from .models import Ovpn
import ipgetter


class VPNActivateView(View):
    def get(self, request, pk):
        Ovpn.objects.exclude(pk=pk).update(activated=False)
        Ovpn.objects.filter(pk=pk).update(activated=True)
        call_command("supervisor", **{'ctl-command': ('restart', 'openvpn')})
        return HttpResponse("OK")


class VPNStatusView(View):
    def get(self, request):
        """Returns data about the currently configured vpn."""
        return JsonResponse({
            'current_ip': ipgetter.myip()
        })

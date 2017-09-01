from django.views.generic import TemplateView
import os
from django.shortcuts import HttpResponse
import json
import requests
import openpyxl



class WebHookView(TemplateView):
    template_name = 'rh/personal/administrativos/lista.html'
    permission_required = "permisos_sican.rh.cargos.ver"


    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.mode') == 'subscribe' and request.GET.get('hub.verify_token') == os.getenv('VALIDATION_TOKEN'):
            return HttpResponse(request.GET.get('hub.challenge'),status=200)
        else:
            return HttpResponse(status=404)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if data['object'] == 'page':
            for entry in data['entry']:
                id = entry['id']
                time = entry['time']
                for message_object in entry['messaging']:
                    if 'message' in message_object.keys():
                        sender_id = message_object['sender']['id']
                        recipient_id = message_object['recipient']['id']
                        message = message_object['message']
                        if 'text' in message.keys():
                            response = {
                                'recipient': {
                                    'id': sender_id
                                },
                                'message': {
                                    'text': message['text']
                                }
                            }
                            self.call_send_api(response,os.getenv('VALIDATION_TOKEN'))

                    else:
                        pass
        return HttpResponse(status=200)

    def call_send_api(self,json,token):
        rqs = requests.post('https://graph.facebook.com/v2.7/me/messages',params={'access_token':token},json=json)
        return rqs.status_code
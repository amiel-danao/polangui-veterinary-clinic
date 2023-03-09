from django.contrib import admin

CONTEXT = {
        'app_id': '55aa17c02cfc41958055ed6a536863ff',
        'app_certificate': '2a15df662d744f43b794971028e9ba4a'
    }


def global_context(request):
    return CONTEXT
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import resolve_url as r
from .forms import SubscriptionsForm
from django.core import mail

from .models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)
    return empty_form(request)

def empty_form(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionsForm()})


def create(request):
    form = SubscriptionsForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)
    #context= dict(nome='Jocsã Kesley', cpf='08838184429', telefone='84996203426', email='jocsadm@gmail.com')
    # Send email
    _send_mail('Confirmação de inscrição', settings.DEFAULT_FROM_EMAIL, subscription.email, 'subscriptions/subscription_email.txt', {'subscription': subscription})
    template_name = 'subscriptions/subscription_email.txt'

    return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))




def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [to, from_,])

def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request,
                  'subscriptions/subscription_detail.html',
                  {'subscription': subscription})

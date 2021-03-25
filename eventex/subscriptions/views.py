from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SubscriptionsForm
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.
def subscription(request):
    if request.method == "POST":
        return create(request)
    else:
        return new(request)
def create(request):
    form = SubscriptionsForm(request.POST)
    if not form.is_valid():
        return render(request, "subscriptions/subscription_form.html", {'form': form})
    _send_email("Confirmação da Incrição", "jocsadm@gmail.com", form.cleaned_data['email'], "subscriptions/subscription_body.txt", form.cleaned_data)
    messages.success(request, "Inscrição realizada com sucesso!")
    return HttpResponseRedirect("/inscricao/")


def new(request):
    return render(request, "subscriptions/subscription_form.html", {'form': SubscriptionsForm()})

def _send_email(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
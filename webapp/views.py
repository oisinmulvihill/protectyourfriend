import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages

from webapp.forms import QuoteForm
from api.models import Breed
from api.models import PolicyType
from api.pricing import generate_price


def index(request):
    """Home and call to action to get quote.
    """
    log = logging.getLogger(__name__)

    template = loader.get_template('index.html')
    log.debug('Hello!')

    return HttpResponse(template.render(dict(), request))


def handle_quote(request):
    """Show quote form or the results of a quote.

    Potentially the customer can jump to pay or save as next locations.

    """
    log = logging.getLogger(__name__)
    result = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuoteForm(request.POST)
        if form.is_valid():
            policy_type = form.cleaned_data['policy_type']
            species = form.cleaned_data['species']
            name = form.cleaned_data['breed']
            age = form.cleaned_data['age']
            excess = form.cleaned_data['excess']
            excess = excess if excess else 0
            breed = Breed.get(species, name)
            policy = PolicyType.get(policy_type)

            if not policy:
                error = f'We do not cover the policy {policy_type}.'
                messages.error(request, error)
                log.error(error)

            elif not breed:
                error = f'We do not cover the breed {species} {name}.'
                messages.error(request, error)
                log.error(error)

            else:
                policy_price = generate_price(
                    policy.base_price,
                    breed.risk_gradient,
                    age,
                    excess
                )
                message = (
                    f'We will cover your friend for {policy_price}p per month.'
                )
                messages.success(request, message)
                log.debug(message)

                # The quote
                result = policy_price

    else:
        # Blank for default:
        form = QuoteForm()

    return render(request, 'quote_form.html', {
        'form': form,
        'quote_result': result
    })

import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from webapp.forms import QuoteForm


def index(request):
    """
    """
    log = logging.getLogger(__name__)

    template = loader.get_template('index.html')
    log.debug('Hello!')

    return HttpResponse(template.render(dict(), request))


def handle_quote(request):
    """
    """
    result = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuoteForm(request.POST)
        if form.is_valid():
            # work out price
            result = 'success'

    else:
        # Blank for default:
        form = QuoteForm()

    return render(request, 'quote_form.html', {
        'form': form,
        'quote_result': result
    })

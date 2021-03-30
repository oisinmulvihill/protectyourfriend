import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from webapp.forms import QuoteForm


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
    result = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuoteForm(request.POST)
        if form.is_valid():
            # work out price
            result = dict(
                outcome='ok', price_quote='£wx.yz'
            )

    else:
        # Blank for default:
        form = QuoteForm()

    return render(request, 'quote_form.html', {
        'form': form,
        'quote_result': result
    })

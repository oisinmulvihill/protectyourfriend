import logging

from django.core.management.base import BaseCommand, CommandError

from webapp.app_logging import log_setup
from api.models import PolicyType
from api.models import Breed


policy_types = [
    dict(name='annual', base_price=200),
    dict(name='lifetime', base_price=400),
    dict(name='preexisting', base_price=600),
]

breeds = [
    dict(species='cat', name="american_curl", risk_gradient=1),
    dict(species='cat', name="american_short_hair", risk_gradient=1),
    dict(species='cat', name="bombay", risk_gradient=3),
    dict(species='cat', name="british_short_hair", risk_gradient=2),
    dict(species='cat', name="persian", risk_gradient=3),
    dict(species='dog', name="border_collie", risk_gradient=1),
    dict(species='dog', name="dalmation", risk_gradient=1),
    dict(species='dog', name="miniature_schnauzer", risk_gradient=3),
    dict(species='dog', name="shiba_Inu", risk_gradient=2),
    dict(species='dog', name="west_highland_white", risk_gradient=1),
]


class Command(BaseCommand):
    help = 'Create fixture data for demo or testing'

    def handle(self, *args, **options):
        log_setup()

        log = logging.getLogger(__name__)

        log.debug("Adding policy type fixtures if not present.")
        for ptype in policy_types:
            if PolicyType.get(ptype['name']) is None:
                log.debug(f"Adding policy:{ptype['name']}")
                PolicyType.add(ptype['name'], ptype['base_price'])

        log.debug("Adding policy type fixtures if not present.")
        for breed in breeds:
            if Breed.get(breed['species'], breed['name']) is None:
                log.debug(f"Adding breed:{breed['name']}")
                Breed.add(
                    breed['species'], breed['name'], breed["risk_gradient"]
                )

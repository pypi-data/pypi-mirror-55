from unittest.mock import patch
from unittest import skip
from collections import namedtuple
from django.test import TestCase
from django.core import mail
from django.conf import settings
from shopify_sync.models import Session as SyncSession
import shopify
from .utils import AbandonedCheckoutHandler
from .models import AbandonedCheckout


class IntegrationTestCase(TestCase):
    """ Requires actual shopify site connection """

    @skip("Requires shopify account")
    def test_get_carts(self):
        handler = AbandonedCheckoutHandler()
        handler.process_abandoned_carts()
        self.assertGreaterEqual(len(mail.outbox), 1)

    @skip("Requires shopify account")
    def test_usage_with_django_shopify_sync(self):
        site = settings.SHOPIFY_ABANDONED_CHECKOUT_SITE
        token = settings.SHOPIFY_ABANDONED_CHECKOUT_TOKEN
        SyncSession.objects.create(site=site, token=token)

        with self.settings(SHOPIFY_ABANDONED_CHECKOUT_SITE=None):
            handler = AbandonedCheckoutHandler()
            handler.process_abandoned_carts()


class AbandonedCartTestCase(TestCase):
    def fake_find(limit, updated_at_min, updated_at_max):
        Response = namedtuple(
            'Response', ['email', 'user_email', 'id', 'abandoned_checkout_url'])
        return [Response('test@example.com', 'test@example.com', '11769580683366', 'https://checkout.revo.com/2279276646/checkouts/04048e7588a7040551c6c440d781c748/recover?key=bcb376debc69f092fd53a144163e7c28')]

    @patch.object(shopify.Checkout, 'find', fake_find)
    def test_process_abandoned_carts(self):
        handler = AbandonedCheckoutHandler()
        handler.process_abandoned_carts()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(AbandonedCheckout.objects.count(), 1)

    @patch.object(shopify.Checkout, 'find', fake_find)
    def test_process_duplicate_carts(self):
        AbandonedCheckout.objects.create(
            checkout_id='11769580683366',
            user_email='test@example.com',
            checkout_url='https://checkout.revo.com/2279276646/checkouts/04048e7588a7040551c6c440d781c748/recover?key=bcb376debc69f092fd53a144163e7c28',
        )
        handler = AbandonedCheckoutHandler()
        handler.process_abandoned_carts()
        self.assertEqual(len(mail.outbox), 0)

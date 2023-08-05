from unittest import TestCase
from uw_kws import KWS
from uw_kws.utilities import fdao_kws_override
from restclients_core.exceptions import DataFailureException
import mock


@fdao_kws_override
class KWSTestKeyData(TestCase):
    def test_key_by_id(self):
        kws = KWS()
        key = kws.get_key('ee99defd-baee-43b0-9e1e-f8238dd106bb')
        self.assertEquals(key.algorithm, 'AES128CBC', 'Correct algorithm')
        self.assertEquals(key.cipher_mode, 'CBC', 'Correct cipher mode')
        self.assertEquals(
            key.expiration.isoformat(),
            '2013-04-11T13:44:33.360000', 'Correct expiration')
        self.assertEquals(
            key.key_id,
            'ee99defd-baee-43b0-9e1e-f8238dd106bb', 'Correct key ID')
        self.assertEquals(key.key, 'Uv2JsxggfxF9OQNzIxAzDQ==', 'Correct key')
        self.assertEquals(key.size, 128, 'Correct key size')
        self.assertEquals(key.url, (
            'https://it-wseval1.s.uw.edu/key/v1/encryption/'
            'ee99defd-baee-43b0-9e1e-f8238dd106bb.json'), 'Correct key URL')

    @mock.patch.object(KWS, '_get_resource')
    def test_key_by_url(self, mock_get):
        mock_get.return_value = {}
        kws = KWS()
        url = (
            'https://it-wseval1.s.uw.edu/key/v1/encryption/'
            'ee99defd-baee-43b0-9e1e-f8238dd106bb.json')

        self.assertRaises(KeyError, kws.get_key, **{'url': url})
        mock_get.assert_called_with(url)

    def test_key_by_invalid(self):
        kws = KWS()
        self.assertRaises(TypeError, kws.get_key)

    def test_current_key(self):
        kws = KWS()
        key = kws.get_current_key('uw-student-registration')
        self.assertEquals(key.algorithm, 'AES128CBC', 'Correct algorithm')
        self.assertEquals(key.cipher_mode, 'CBC', 'Correct cipher mode')
        self.assertEquals(
            key.expiration.isoformat(),
            '2013-04-11T13:44:33.360000', 'Correct expiration')
        self.assertEquals(
            key.key_id,
            'ee99defd-baee-43b0-9e1e-f8238dd106bb', 'Correct key ID')
        self.assertEquals(key.key, 'Uv2JsxggfxF9OQNzIxAzDQ==', 'Correct key')
        self.assertEquals(key.size, 128, 'Correct key size')
        self.assertEquals(key.url, (
            'https://it-wseval1.s.uw.edu/key/v1/encryption/'
            'ee99defd-baee-43b0-9e1e-f8238dd106bb.json'), 'Correct key URL')

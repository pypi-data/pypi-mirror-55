from restclients_core import models
import dateutil.parser


class Key(models.Model):
    algorithm = models.CharField(max_length=100)
    cipher_mode = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    key_id = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    size = models.SmallIntegerField()
    url = models.CharField(max_length=1000)

    @staticmethod
    def from_json(data):
        key = Key()
        key.algorithm = data["Algorithm"]
        key.cipher_mode = data["CipherMode"]
        key.expiration = dateutil.parser.parse(data["Expiration"])
        key.key_id = data["ID"]
        key.key = data["Key"]
        key.size = data["KeySize"]
        key.url = data["KeyUrl"]
        return key

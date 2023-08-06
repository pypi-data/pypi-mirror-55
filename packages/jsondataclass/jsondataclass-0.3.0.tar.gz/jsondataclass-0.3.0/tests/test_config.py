from jsondataclass.config import Config
from jsondataclass.serializers import DefaultSerializer


def test_config_defaults():
    config = Config()
    assert config.default_serializer_class is DefaultSerializer

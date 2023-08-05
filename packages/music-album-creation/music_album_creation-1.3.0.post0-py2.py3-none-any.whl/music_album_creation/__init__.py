__version__ = '1.3.0.post0'

import logging.config
from os import path

from .audio_segmentation import AudioSegmenter
from .format_classification import FormatClassifier
from .metadata import MetadataDealer
from .tracks_parsing import StringParser

logging.config.fileConfig(path.join(path.dirname(path.realpath(__file__)), 'logging.ini'), disable_existing_loggers=False)

logger = logging.getLogger(__name__)


__all__ = ['StringParser', 'MetadataDealer', 'FormatClassifier', 'AudioSegmenter']

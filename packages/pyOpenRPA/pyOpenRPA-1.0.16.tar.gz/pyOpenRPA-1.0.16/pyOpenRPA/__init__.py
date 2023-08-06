r"""

The OpenRPA package (from UnicodeLabs)

"""
__version__ = 'v1.0.16'
__all__ = [
    'UIDesktop.py', 'Clipboard', 'IntegrationOrchestrator', 'Window', 'ProcessCommunicator', 'Robot'
]
__author__ = 'Ivan Maslov <ivan.maslov@unicodelabs.ru>'
from . import UIDesktop
from . import Clipboard
from . import IntegrationOrchestrator
from . import Window
from . import ProcessCommunicator
r"""

The OpenRPA package (from UnicodeLabs)

"""
import Version
__version__ = Version.Get("..")
__all__ = [
    'GUI','Clipboard','IntegrationOrchestrator','Window'
]

__author__ = 'Ivan Maslov <ivan.maslov@unicodelabs.ru>'

import GUI
import Clipboard
import IntegrationOrchestrator
import Window
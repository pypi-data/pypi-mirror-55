# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""
Defines reStructuredText directives to simplify documenting AiiDA and its plugins.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from sphinx.errors import ExtensionError


def setup(app):
    """
    Setup function to add the extension classes / nodes to Sphinx.
    """
    import aiida

    from . import process, workchain, calcjob
    try:
        app.setup_extension('sphinxcontrib.details.directive')
    # This is a workaround because this extension doesn't work with Python2.
    except ExtensionError:
        pass

    process.setup_extension(app)
    workchain.setup_extension(app)
    calcjob.setup_extension(app)

    return {'version': aiida.__version__, 'parallel_read_safe': True}

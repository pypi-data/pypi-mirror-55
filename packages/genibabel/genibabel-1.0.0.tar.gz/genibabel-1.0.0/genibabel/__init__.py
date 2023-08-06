# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Package to simplify to create/explore a genetic reference.
The entities available are

    * chromosomes.
    * genes.
    * snps.
    * pathways.
    * cpgs.
    * cpg islands.
"""

from .info import __version__
from .elasticmetagen import MetaGen

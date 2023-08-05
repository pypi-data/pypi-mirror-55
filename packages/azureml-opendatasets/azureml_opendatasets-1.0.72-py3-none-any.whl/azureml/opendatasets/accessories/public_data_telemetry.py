# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Public data telemetry base class."""

from .._utils.telemetry_utils import get_opendatasets_logger


class PublicDataTelemetry:
    """Public data telemetry base class contains telemetry logger for each open datasets."""

    logger = get_opendatasets_logger(__name__)

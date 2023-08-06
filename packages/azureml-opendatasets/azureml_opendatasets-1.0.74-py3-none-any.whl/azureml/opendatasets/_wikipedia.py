# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Wikipedia."""

from azureml.data import FileDataset
from azureml.data._dataset import _DatasetTelemetryInfo
from azureml.core.dataset import Dataset
from azureml.telemetry.activity import ActivityType, log_activity

from ._utils.telemetry_utils import get_run_common_properties
from .accessories.public_data_telemetry import PublicDataTelemetry
from .dataaccess._wikipedia_blob_info import WikipediaBlobInfo


class Wikipedia(PublicDataTelemetry):
    """Wikipedia class."""

    @staticmethod
    def get_file_dataset(enable_telemetry: bool = True) -> FileDataset:
        blobInfo = WikipediaBlobInfo()
        url_paths = blobInfo.get_url()
        if enable_telemetry:
            log_properties = get_run_common_properties()
            log_properties['RegistryId'] = blobInfo.registry_id
            log_properties['Path'] = url_paths
            with log_activity(
                    Wikipedia.logger,
                    'get_file_dataset',
                    ActivityType.PUBLICAPI,
                    custom_dimensions=log_properties):
                ds = Dataset.File.from_files(path=url_paths)
                ds._telemetry_info = _DatasetTelemetryInfo(entry_point='PythonSDK.OpenDataset')
                return ds
        else:
            ds = Dataset.File.from_files(path=url_paths)
            ds._telemetry_info = _DatasetTelemetryInfo(entry_point='PythonSDK.OpenDataset')
            return ds

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""MNIST data."""

from azureml.core import Dataset
from azureml.data import FileDataset, TabularDataset
from azureml.data._dataset import _DatasetTelemetryInfo
from azureml.telemetry.activity import ActivityType, log_activity

from ._utils.telemetry_utils import get_run_common_properties
from .accessories.public_data_telemetry import PublicDataTelemetry
from .dataaccess._mnist_blob_info import MNISTBlobInfo


class MNIST(PublicDataTelemetry):
    """MNIST data class."""

    _blobInfo = MNISTBlobInfo()

    @staticmethod
    def _get_logger_prop(blobInfo: MNISTBlobInfo, dataset_filter: str = 'all'):
        log_properties = get_run_common_properties()
        log_properties['RegistryId'] = blobInfo.registry_id
        log_properties['Path'] = blobInfo.get_data_wasbs_path()
        log_properties['dataset_filter'] = dataset_filter
        return log_properties

    @staticmethod
    def get_tabular_dataset(
            dataset_filter='all',
            enable_telemetry: bool = True) -> TabularDataset:
        _url_path = MNIST._blobInfo.get_csv_url(dataset_filter=dataset_filter)
        if enable_telemetry:
            log_properties = MNIST._get_logger_prop(MNIST._blobInfo, dataset_filter)
            with log_activity(
                    MNIST.logger,
                    'get_tabular_dataset',
                    ActivityType.PUBLICAPI,
                    custom_dimensions=log_properties):
                ds = Dataset.Tabular.from_delimited_files(path=_url_path)
                ds._telemetry_info = _DatasetTelemetryInfo(entry_point='PythonSDK.OpenDataset')
                return ds
        else:
            ds = Dataset.Tabular.from_delimited_files(path=_url_path)
            ds._telemetry_info = _DatasetTelemetryInfo(entry_point='PythonSDK.OpenDataset')
            return ds

    @staticmethod
    def get_file_dataset(
            dataset_filter='all',
            enable_telemetry: bool = True) -> FileDataset:
        _url_path = MNIST._blobInfo.get_raw_url(dataset_filter=dataset_filter)
        if enable_telemetry:
            log_properties = MNIST._get_logger_prop(MNIST._blobInfo, dataset_filter)
            with log_activity(
                    MNIST.logger,
                    'get_file_dataset',
                    ActivityType.PUBLICAPI,
                    custom_dimensions=log_properties):
                ds = Dataset.File.from_files(path=_url_path)
                ds._telemetry_info = _DatasetTelemetryInfo(entry_point='PythonSDK.OpenDataset')
                return ds
        else:
            ds = Dataset.File.from_files(path=_url_path)
            ds._telemetry_info = _DatasetTelemetryInfo(entry_point='PythonSDK.OpenDataset')
            return ds

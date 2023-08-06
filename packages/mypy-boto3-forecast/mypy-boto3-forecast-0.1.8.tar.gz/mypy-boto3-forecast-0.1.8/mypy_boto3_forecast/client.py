from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_dataset(
        self,
        DatasetName: str,
        Domain: str,
        DatasetType: str,
        Schema: Dict[str, Any],
        DataFrequency: str = None,
        EncryptionConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_dataset_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_dataset_import_job(
        self,
        DatasetImportJobName: str,
        DatasetArn: str,
        DataSource: Dict[str, Any],
        TimestampFormat: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_forecast(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_forecast_export_job(
        self, ForecastExportJobName: str, ForecastArn: str, Destination: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_predictor(
        self,
        PredictorName: str,
        ForecastHorizon: int,
        InputDataConfig: Dict[str, Any],
        FeaturizationConfig: Dict[str, Any],
        AlgorithmArn: str = None,
        PerformAutoML: bool = None,
        PerformHPO: bool = None,
        TrainingParameters: Dict[str, Any] = None,
        EvaluationParameters: Dict[str, Any] = None,
        HPOConfig: Dict[str, Any] = None,
        EncryptionConfig: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_dataset_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_dataset_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_forecast(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_forecast_export_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_predictor(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_dataset_import_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_forecast(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_forecast_export_job(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_predictor(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_presigned_url(
        self,
        ClientMethod: str = None,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = None,
        HttpMethod: str = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_accuracy_metrics(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_dataset_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_dataset_import_jobs(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_datasets(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_forecast_export_jobs(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_forecasts(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def list_predictors(
        self, NextToken: str = None, MaxResults: int = None, Filters: List[Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_dataset_group(self) -> None:
        pass

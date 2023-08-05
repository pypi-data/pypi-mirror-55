# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Download and load model explanation configuration."""
from typing import Any, cast, Dict, List, Optional
import logging
import json
import os

from automl.client.core.common import activity_logger, logging_utilities
from automl.client.core.common.exceptions import ConfigException
from azureml.automl.core._downloader import Downloader


class AutoMLModelExplanationConfig:
    """Holder for model explanation configurations."""

    CONFIG_DOWNLOAD_PREFIX = "https://aka.ms/automl-resources/configs/"
    CONFIG_DOWNLOAD_FILE = "model_explanation_config_v1.0.json"
    REMOTE_CONFIG_DOWNLOAD_FILE = "model_explanation_config_v1.1.json"

    DEFAULT_CONFIG_PATH = "../model_explanation_config_v1.0.json"

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger or logging_utilities.get_logger()

    def get_config(self, is_remote: bool = False) -> Dict[str, Any]:
        """Provide configuration."""
        try:
            if is_remote:
                file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX,
                                                self.REMOTE_CONFIG_DOWNLOAD_FILE, os.getcwd())
            else:
                file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX, self.CONFIG_DOWNLOAD_FILE,
                                                os.getcwd())
            if file_path is None:
                raise ConfigException("Configuration url: {prefix}{file_path} is not accessible!.")

            with open(file_path, 'r') as f:
                cfg = json.load(f)  # type: Dict[str, Any]
                self._logger.debug("Successfully downloaded the model explanations from the the remote.")
                return cfg
        except Exception as e:
            self._logger.debug("Exception when trying to load config from the remote: "
                               "{prefix}{file_path} with error {e}".format(prefix=self.CONFIG_DOWNLOAD_PREFIX,
                                                                           file_path=self.CONFIG_DOWNLOAD_FILE,
                                                                           e=e))
            return self.default()

    def default(self) -> Dict[str, Any]:
        """Return the default back up configuration."""
        default_config_path = os.path.abspath(os.path.join(__file__, self.DEFAULT_CONFIG_PATH))
        with open(default_config_path, "r") as f:
            result = json.loads(f.read())  # type: Dict[str, Any]
            self._logger.debug("Read model explanations config from SDK.")
            return result

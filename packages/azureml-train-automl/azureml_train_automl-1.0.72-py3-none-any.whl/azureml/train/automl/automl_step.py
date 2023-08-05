# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""To add a step to run automated machine learning as part of the Azure Machine Learning pipeline."""
from typing import Any, Dict, List, Optional, Tuple
import json
import ntpath
from azureml._execution import _commands
from azureml.core import Experiment
from azureml.core.runconfig import RunConfiguration
from azureml.data import TabularDataset
from azureml.pipeline.core import PipelineStep, PipelineData, TrainingOutput
from azureml.pipeline.core._module_builder import _ModuleBuilder
from azureml.pipeline.core.graph import ParamDef
from azureml.pipeline.core.pipeline_output_dataset import PipelineOutputTabularDataset

from .automlconfig import AutoMLConfig
from azureml.automl.core import dataprep_utilities, dataset_utilities
from .run import AutoMLRun
from ._azureautomlclient import AzureAutoMLClient
from ._azureautomlsettings import AzureAutoMLSettings
from ._environment_utilities import modify_run_configuration
from .exceptions import ConfigException

import os
import logging


class AutoMLStep(PipelineStep):
    """Creates an AutoML step in a Pipeline.

    See an example of using this step in notebook https://aka.ms/pl-automl.

    :param name: Name of the step.
    :type name: str
    :param automl_config: An AutoMLConfig that defines the configuration for this AutoML run. The
        file path specified in the ``data_script`` configuration parameter must end with a file named "get_data.py".
    :type automl_config: azureml.train.automl.AutoMLConfig
    :param inputs: List of input port bindings.
    :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
                  azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
    :param outputs: List of output port bindings.
    :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
    :param script_repl_params: Optional parameters to be replaced in a script.
    :type script_repl_params: dict
    :param allow_reuse: Whether the step should reuse previous results when re-run with the same settings.
        Reuse is enabled by default. If the step contents (scripts/dependencies) as well as inputs and
        parameters remain unchanged, the output from the previous run of this step is reused. When reusing
        the step, instead of submitting the job to compute, the results from the previous run are immediately
        made available to any subsequent steps. If you use Azure Machine Learning datasets as inputs, reuse is
        determined by whether the dataset's definition has changed, not by whether the underlying data has
        changed.
    :type allow_reuse: bool
    :param version: Version.
    :type version: str
    :param hash_paths: List of paths to hash when checking for changes to the step contents.
        If there are no changes detected, the pipeline will reuse the step contents from a previous run.
        All files under ``path`` and the ``data_script`` file specified in
        :class:`azureml.train.automl.AutoMLConfig`
        are hashed except files listed in .amlignore or .gitignore under ``path``.
        This parameter is deprecated and is no longer needed.
    :type hash_paths: list
    :param passthru_automl_config: Whether automl config will be delivered to automl service without parsing.
        It is enabled by default. It can be disabled to use parameter specific operations such as
        parameterization via PipelineParameter.
    :type passthru_automl_config: bool
    """

    DEFAULT_METRIC_PREFIX = 'default_metrics_'
    DEFAULT_MODEL_PREFIX = 'default_model_'
    AUTOML_CONFIG_PARAM_NAME = 'AutoMLConfig'

    _INTERMEDIATE_DATASET = 'intermediate_datasets'

    def __init__(self, name, automl_config, inputs=None, outputs=None, script_repl_params=None,
                 allow_reuse=True, version=None, hash_paths=None, passthru_automl_config=True):
        """Initialize an AutoMLStep.

        :param name: Name of the step.
        :type name: str
        :param automl_config: An AutoMLConfig that defines the configuration for this AutoML run. The
        file path specified in the ``data_script`` configuration parameter must end with a file named "get_data.py".
        :type automl_config: azureml.train.automl.AutoMLConfig
        :param inputs: List of input port bindings.
        :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
                      azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
        :param outputs: List of output port bindings.
        :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
        :param script_repl_params: Optional parameters to be replaced in a script.
        :type script_repl_params: dict
        :param allow_reuse: Whether the step should reuse previous results when re-run with the same settings.
            Reuse is enabled by default. If the step contents (scripts/dependencies) as well as inputs and
            parameters remain unchanged, the output from the previous run of this step is reused. When reusing
            the step, instead of submitting the job to compute, the results from the previous run are immediately
            made available to any subsequent steps. If you use Azure Machine Learning datasets as inputs, reuse is
            determined by whether the dataset's definition has changed, not by whether the underlying data has
            changed.
        :type allow_reuse: bool
        :param version: Version.
        :type version: str
        :param hash_paths: List of paths to hash when checking for changes to the step contents.
            If there are no changes detected, the pipeline will reuse the step contents from a previous run.
            All files under ``path`` and the ``data_script`` file specified in
            :class:`azureml.train.automl.AutoMLConfig`
            are hashed except files listed in .amlignore or .gitignore under ``path``.
            DEPRECATED. This parameter is no longer needed.
        :type hash_paths: list
        :param passthru_automl_config: Whether automl config will be delivered to automl service without parsing.
        It is enabled by default. It can be disabled to use parameter specific operations such as
        parameterization via PipelineParameter.
        :type passthru_automl_config: bool
        """
        if name is None:
            raise ConfigException('name is required')
        if not isinstance(name, str):
            raise ConfigException('name must be a string')

        if automl_config is None:
            raise ConfigException('automl_config is required')
        if not isinstance(automl_config, AutoMLConfig):
            raise ConfigException('Unexpected automl_config type: {}'.format(type(automl_config)))

        PipelineStep._process_pipeline_io(None, inputs, outputs)

        self._allow_reuse = allow_reuse
        self._version = version

        self._params = {}   # type: Dict[str, Any]
        self._pipeline_params_implicit = PipelineStep._get_pipeline_parameters_implicit()
        self._update_param_bindings()

        self._automl_config = automl_config
        self._passthru_automl_config = passthru_automl_config

        self._source_directory = self._automl_config.user_settings['path']

        if hash_paths:
            logging.warning("Parameter 'hash_paths' is deprecated, will be removed. " +
                            "All files under  `path` and the `data_script` file specified " +
                            "in `AutoMLConfig` is hashed except files listed in " +
                            ".amlignore or .gitignore under `path`.")

        self._hash_paths = hash_paths
        if self._hash_paths is None:
            self._hash_paths = []

        self._script_name = None
        if self._automl_config.user_settings["data_script"] is not None:
            ntpath.basename("a/b/c")
            head, tail = ntpath.split(self._automl_config.user_settings["data_script"])
            self._script_name = tail or ntpath.basename(head)
            script_path = os.path.join(self._source_directory, self._script_name)
            self._process_script(script_path, script_repl_params)

        self._default_metrics_output = None
        self._default_model_output = None

        inputs = inputs or []
        inputs = inputs[:]
        AutoMLStep._update_inputs(automl_config, inputs)

        super(AutoMLStep, self).__init__(name=name, inputs=inputs, outputs=outputs)

    def _process_script(self, script_path, script_repl_params):
        import re
        pattern = re.compile(r"@@(?P<param_name>\w+)@@")

        def resolve_input_path(matchobj):
            replacement_str = script_repl_params.get(matchobj.group('param_name'))
            if replacement_str:
                return replacement_str
            else:
                print('found pattern:', matchobj.group('param_name'), ', but no replacement has been provided')

        self._sub_params_in_script(script_path, pattern, resolve_input_path)

    def create_node(self, graph, default_datastore, context):
        """Create a node from this AutoML step and add to the given graph.

        :param graph: The graph object to add the node to.
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore: default datastore
        :type default_datastore: azureml.core.AbstractAzureStorageDatastore, azureml.core.AzureDataLakeDatastore
        :param context: The graph context.
        :type context: _GraphContext

        :return: The created node.
        :rtype: azureml.pipeline.core.graph.Node
        """
        self._default_metrics_output = PipelineData(name=AutoMLStep.DEFAULT_METRIC_PREFIX + self.name,
                                                    datastore=default_datastore,
                                                    pipeline_output_name='_default_metrics_' + self.name,
                                                    training_output=TrainingOutput(type='Metrics'))
        self._default_model_output = PipelineData(name=AutoMLStep.DEFAULT_MODEL_PREFIX + self.name,
                                                  datastore=default_datastore,
                                                  pipeline_output_name='_default_model_' + self.name,
                                                  training_output=TrainingOutput(type='Model'))

        self._default_metrics_output._set_producer(self)
        self._default_model_output._set_producer(self)
        self._outputs.extend([self._default_metrics_output, self._default_model_output])

        hash_paths = [self._source_directory]
        if self._script_name is not None:
            source_directory, hash_paths = self.get_source_directory_and_hash_paths(
                context, self._source_directory, self._script_name, self._hash_paths)

            hash_paths.append(self._automl_config.user_settings["data_script"])

        input_bindings, output_bindings = self.create_input_output_bindings(self._inputs, self._outputs,
                                                                            default_datastore)

        settings = self._get_automl_settings(context)
        self._params.update(settings)

        arguments = self.resolve_input_arguments(self._arguments, self._inputs, self._outputs, self._params)
        if arguments is not None and len(arguments) > 0:
            self._params['Arguments'] = ",".join([str(x) for x in arguments])

        def _get_param_def(param_name):
            is_metadata_param = param_name in AutoMLStep.AUTOML_CONFIG_PARAM_NAME

            if param_name in self._pipeline_params_implicit:
                return ParamDef(param_name,
                                default_value=self._params[param_name],
                                is_metadata_param=is_metadata_param,
                                set_env_var=True,
                                env_var_override="AML_PARAMETER_{0}".format(param_name))
            else:
                return ParamDef(param_name,
                                default_value=self._params[param_name],
                                is_metadata_param=is_metadata_param,
                                is_optional=True)

        param_defs = [_get_param_def(param_name) for param_name in self._params]

        module_def = self.create_module_def(execution_type="AutoMLCloud",
                                            input_bindings=input_bindings,
                                            output_bindings=output_bindings,
                                            param_defs=param_defs,
                                            allow_reuse=self._allow_reuse, version=self._version)

        module_builder = _ModuleBuilder(
            snapshot_root=self._source_directory,
            additional_hash_paths=hash_paths,
            context=context,
            module_def=module_def)

        node = graph.add_module_node(
            self.name,
            input_bindings=input_bindings,
            output_bindings=output_bindings,
            param_bindings=self._params,
            module_builder=module_builder)

        PipelineStep._configure_pipeline_parameters(graph, node,
                                                    pipeline_params_implicit=self._pipeline_params_implicit)

        return node

    def _get_automl_settings(self, context):

        self._automl_config._validate_config_settings()
        self._automl_config._get_remove_fit_params()

        user_settings = self._automl_config.user_settings
        experiment = Experiment(context._workspace, context.experiment_name, _create_in_cloud=False)
        settings_obj = AzureAutoMLSettings(experiment, **user_settings)
        automl_client = AzureAutoMLClient(experiment, settings_obj)

        settings = automl_client.automl_settings.as_serializable_dict()

        # parameters for run configuration
        run_configuration = self._automl_config.fit_params['run_configuration']
        if isinstance(run_configuration, str):
            run_config_object = RunConfiguration.load(
                automl_client.automl_settings.path, run_configuration)
        else:
            run_config_object = run_configuration

        try:
            settings['MLCComputeType'] = self._automl_config.fit_params['compute_target'].type
        except KeyError:
            raise ConfigException('compute_target is not provided to AutoMLConfig')
        except AttributeError:
            raise ConfigException('compute_target is not an object of ComputeTarget.')

        run_config_object = modify_run_configuration(automl_client.automl_settings,
                                                     run_config_object,
                                                     automl_client.logger)
        run_config_params = self._get_runconfig_as_dict(run_config_object)

        X = self._automl_config.fit_params.get('X', None)
        y = self._automl_config.fit_params.get('y', None)
        X_valid = self._automl_config.fit_params.get('X_valid', None)
        y_valid = self._automl_config.fit_params.get('y_valid', None)
        sample_weight = self._automl_config.fit_params.get('sample_weight', None)
        sample_weight_valid = self._automl_config.fit_params.get('sample_weight_valid', None)
        cv_splits_indices = self._automl_config.fit_params.get('cv_splits_indices', None)
        training_data = self._automl_config.fit_params.get('training_data', None)
        validation_data = self._automl_config.fit_params.get('validation_data', None)

        dataset_utilities.ensure_saved(
            context._workspace, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            sample_weight_valid=sample_weight_valid, training_data=training_data, validation_data=validation_data
        )
        dataset_utilities.collect_usage_telemetry(
            compute=run_configuration.target,
            spark_context=self._automl_config.user_settings.get('spark_context', None),
            X=X, y=y, sample_weight=sample_weight,
            X_valid=X_valid, y_valid=y_valid, sample_weight_valid=sample_weight_valid,
            training_data=training_data, validation_data=validation_data
        )

        X, y, sample_weight, X_valid, y_valid, sample_weight_valid = dataset_utilities.convert_inputs(
            X, y, sample_weight,
            X_valid, y_valid, sample_weight_valid
        )
        training_data, validation_data = dataset_utilities.convert_inputs_dataset(
            training_data, validation_data
        )

        X, y, sample_weight, X_valid, y_valid, sample_weight_valid, training_data, validation_data = \
            self._handle_intermediate_dataset(
                settings, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
                sample_weight_valid=sample_weight_valid, training_data=training_data, validation_data=validation_data
            )

        if training_data is not None:
            dataprep_json = dataprep_utilities.\
                get_dataprep_json_dataset(training_data=training_data,
                                          validation_data=validation_data)
        else:
            dataprep_json = dataprep_utilities.get_dataprep_json(X=X, y=y,
                                                                 sample_weight=sample_weight,
                                                                 X_valid=X_valid,
                                                                 y_valid=y_valid,
                                                                 sample_weight_valid=sample_weight_valid,
                                                                 cv_splits_indices=cv_splits_indices)

        if dataprep_json is not None:
            # escape quotations in json_str before sending to jasmine
            dataprep_json = dataprep_json.replace('\\', '\\\\').replace('"', '\\"')

        if self._passthru_automl_config:
            # CreateParentRunDto which will be passed through Jasmine
            parent_run_dto = automl_client._create_parent_run_dto(run_configuration, dataprep_json)
            automl_client._validate_remote_input(parent_run_dto)

            settings[AutoMLStep.AUTOML_CONFIG_PARAM_NAME] = json.dumps(parent_run_dto.as_dict())
            logging.info('passthru automl config: ', settings[AutoMLStep.AUTOML_CONFIG_PARAM_NAME])

        # parameters for CreateParentRunDto
        timeout = None
        if automl_client.automl_settings.iteration_timeout_minutes:
            timeout = automl_client.automl_settings.iteration_timeout_minutes * 60
        settings['max_time_seconds'] = timeout
        settings['target'] = run_config_object.target
        settings['targettype'] = 'mlc'
        settings['num_iterations'] = automl_client.automl_settings.iterations
        settings['training_type'] = None
        settings['acquisition_function'] = None
        settings['metrics'] = 'accuracy'
        settings['primary_metric'] = automl_client.automl_settings.primary_metric
        settings['train_split'] = automl_client.automl_settings.validation_size
        settings['acquisition_parameter'] = 0.0
        settings['num_cross_validation'] = automl_client.automl_settings.n_cross_validations
        settings['data_prep_json_string'] = dataprep_json
        settings['enable_subsampling'] = automl_client.automl_settings.enable_subsampling

        settings.update(run_config_params)

        # reformatting list to comma separated string for backend until we have comprehensive solution
        for key in ['whitelist_models', 'blacklist_models', 'DockerArguments', 'SparkRepositories']:
            value = settings.get(key, None)
            if isinstance(value, list):
                settings[key] = ",".join([str(x) for x in value])

        return settings

    def _get_runconfig_as_dict(self, run_config=None):
        """Set runconfig for AutoML step.

        :param run_config: run config object
        :type run_config: RunConfiguration

        :return: run config params
        :rtype: Dictionary
        """
        if not isinstance(run_config, RunConfiguration):
            raise ConfigException('run_configuration is required')

        spark_maven_packages = []
        for package in run_config.environment.spark.packages:
            package_dict = {'artifact': package.artifact, 'group': package.group, 'version': package.version}
            spark_maven_packages.append(package_dict)

        spark_configuration = ';'.join(["{0}={1}".format(key, val) for key, val
                                        in run_config.spark.configuration.items()])

        environment_variables = ';'.join(["{0}={1}".format(key, val) for key, val
                                          in run_config.environment.environment_variables.items()])

        serialized = _commands._serialize_run_config_to_dict(run_config)

        conda_dependencies = None
        try:
            conda_dependencies = serialized['environment']['python']['condaDependencies']
        except KeyError:
            pass

        docker_arguments = None
        if len(run_config.environment.docker.arguments) > 0:
            docker_arguments = ",".join([str(x) for x in run_config.environment.docker.arguments])

        run_config_params = {'Script': run_config.script,
                             'Framework': run_config.framework,
                             'Communicator': run_config.communicator,
                             'DockerEnabled': run_config.environment.docker.enabled,
                             'BaseDockerImage': run_config.environment.docker.base_image,
                             'SharedVolumes': run_config.environment.docker.shared_volumes,
                             'DockerArguments': docker_arguments,
                             'SparkRepositories': run_config.environment.spark.repositories,
                             'SparkMavenPackages': spark_maven_packages,
                             'SparkConfiguration': spark_configuration,
                             'InterpreterPath': run_config.environment.python.interpreter_path,
                             'UserManagedDependencies': run_config.environment.python.user_managed_dependencies,
                             'MaxRunDurationSeconds': run_config.max_run_duration_seconds,
                             'EnvironmentVariables': environment_variables,
                             'PrecachePackages': run_config.environment.spark.precache_packages,
                             'HistoryOutputCollection': run_config.history.output_collection,
                             'NodeCount': run_config.node_count,
                             'YarnDeployMode': run_config.hdi.yarn_deploy_mode,
                             'CondaDependencies': json.dumps(conda_dependencies),
                             'MpiProcessCountPerNode': run_config.mpi.process_count_per_node,
                             'TensorflowWorkerCount': run_config.tensorflow.worker_count,
                             'TensorflowParameterServerCount': run_config.tensorflow.parameter_server_count,
                             'AMLComputeName': run_config.amlcompute._name,
                             'AMLComputeVmSize': run_config.amlcompute.vm_size,
                             'AMLComputeVmPriority': run_config.amlcompute.vm_priority,
                             'AMLComputeLocation': None,
                             'AMLComputeRetainCluster': run_config.amlcompute._retain_cluster,
                             'AMLComputeNodeCount': run_config.amlcompute._cluster_max_node_count,
                             'SourceDirectoryDataStore': run_config.source_directory_data_store,
                             'DirectoriesToWatch': run_config.history.directories_to_watch
                             }

        return run_config_params

    def _update_param_bindings(self):
        for pipeline_param in self._pipeline_params_implicit.values():
            if pipeline_param.name not in self._params:
                self._params[pipeline_param.name] = pipeline_param
            else:
                raise Exception('Parameter name {0} is already in use'.format(pipeline_param.name))

    @staticmethod
    def _update_inputs(automl_config, inputs):
        settings = automl_config.user_settings
        existing_tabular_input_names = set([
            dataset.input_name for dataset in
            filter(lambda input: isinstance(input, PipelineOutputTabularDataset), inputs)
        ])

        for arg in ['X', 'y', 'sample_weight', 'X_valid', 'y_valid', 'sample_weight_valid', 'training_data'
                    'validation_data']:
            arg_value = settings.get(arg, None)

            if not isinstance(arg_value, PipelineOutputTabularDataset) and not isinstance(arg_value, TabularDataset):
                continue

            if arg in existing_tabular_input_names:
                continue

            inputs.append(arg_value.as_named_input(arg))

    def _handle_intermediate_dataset(self, settings, X=None, y=None, sample_weight=None, X_valid=None,
                                     y_valid=None, sample_weight_valid=None, training_data=None, validation_data=None):
        updated_args = []   # type: List[Optional[Any]]
        args = [
            ('X', X), ('y', y), ('sample_weight', sample_weight), ('X_valid', X_valid), ('y_valid', y_valid),
            ('sample_weight_valid', sample_weight_valid), ('training_data', training_data),
            ('validation_data', validation_data)
        ]    # type: List[Tuple[str, Any]]
        for arg_name, arg_value in args:
            if isinstance(arg_value, PipelineOutputTabularDataset):
                if self._passthru_automl_config:
                    raise ConfigException('passthru_automl_config should be set to False when constructing the '
                                          'AutoMLStep to use PipelineOutputTabularDataset.')

                updated_args.append(None)
                settings[AutoMLStep._INTERMEDIATE_DATASET] = \
                    [*settings.get(AutoMLStep._INTERMEDIATE_DATASET, []), arg_name]
            else:
                updated_args.append(arg_value)

        if AutoMLStep._INTERMEDIATE_DATASET in settings:
            settings[AutoMLStep._INTERMEDIATE_DATASET] = ';'.join(settings[AutoMLStep._INTERMEDIATE_DATASET])

        return updated_args


class AutoMLStepRun(AutoMLRun):
    """
    AutoMLStepRun is AutoMLRun with additional supports from StepRun.

    As AutoMLRun this class can be used to manage, check status, and retrieve run details
    once a AutoML run is submitted. In addition this class can be used to get default outputs
    of AutoMLStep via StepRun.
    For more details on AutoMLRun and StepRun:
    :class:`azureml.train.automl.run.AutoMLRun`,
    :class:`azureml.pipeline.core.StepRun`

    :param step_run: The step run object which created from pipeline.
    :type step_run: azureml.pipeline.core.StepRun
    """

    def __init__(self, step_run):
        """
        Initialize a automl Step run.

        :param step_run: The step run object which created from pipeline.
        :type step_run: azureml.pipeline.core.StepRun
        """
        self._step_run = step_run

        super(self.__class__, self).__init__(step_run._context._experiment, step_run._run_id)

    def get_default_metrics_output(self):
        """
        Return default metrics output of current run.

        :return: Default metrics output of current run.
        :rtype: azureml.pipeline.core.StepRunOutput
        """
        default_metrics_output_name = AutoMLStep.DEFAULT_METRIC_PREFIX + self._step_run._run_name
        return self._step_run.get_output(default_metrics_output_name)

    def get_default_model_output(self):
        """
        Return default model output of current run.

        :return: Default model output of current run.
        :rtype: azureml.pipeline.core.StepRunOutput
        """
        default_model_output_name = AutoMLStep.DEFAULT_MODEL_PREFIX + self._step_run._run_name
        return self._step_run.get_output(default_model_output_name)

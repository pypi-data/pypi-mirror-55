import datetime
import re

from airflow import DAG
from airflow.operators import BaseOperator

from dagster import ExecutionTargetHandle, RunConfig, check, seven
from dagster.core.execution.api import create_execution_plan
from dagster.core.instance import DagsterInstance

from .compile import coalesce_execution_steps
from .operators.docker_operator import DagsterDockerOperator
from .operators.python_operator import DagsterPythonOperator

DEFAULT_ARGS = {
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': datetime.timedelta(0, 300),
    'start_date': datetime.datetime(1900, 1, 1, 0, 0),
}

# Airflow DAG names are not allowed to be longer than 250 chars
AIRFLOW_MAX_DAG_NAME_LEN = 250


def _make_dag_description(pipeline_name):
    return '''Editable scaffolding autogenerated by dagster-airflow from pipeline {pipeline_name}
    '''.format(
        pipeline_name=pipeline_name
    )


def _rename_for_airflow(name):
    '''Modify pipeline name for Airflow to meet constraints on DAG names:
    https://github.com/apache/airflow/blob/1.10.3/airflow/utils/helpers.py#L52-L63

    Here, we just substitute underscores for illegal characters to avoid imposing Airflow's
    constraints on our naming schemes.
    '''
    return re.sub(r'[^\w\-\.]', '_', name)[:AIRFLOW_MAX_DAG_NAME_LEN]


def _make_airflow_dag(
    handle,
    pipeline_name,
    environment_dict=None,
    mode=None,
    instance=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
    operator=DagsterPythonOperator,
):
    check.inst_param(handle, 'handle', ExecutionTargetHandle)
    check.str_param(pipeline_name, 'pipeline_name')
    environment_dict = check.opt_dict_param(environment_dict, 'environment_dict', key_type=str)
    mode = check.opt_str_param(mode, 'mode')
    # Default to use the (persistent) system temp directory rather than a seven.TemporaryDirectory,
    # which would not be consistent between Airflow task invocations.
    instance = (
        check.inst_param(instance, 'instance', DagsterInstance)
        if instance
        else DagsterInstance.get(fallback_storage=seven.get_system_temp_directory())
    )

    # Only used for Airflow; internally we continue to use pipeline.name
    dag_id = check.opt_str_param(dag_id, 'dag_id', _rename_for_airflow(pipeline_name))

    dag_description = check.opt_str_param(
        dag_description, 'dag_description', _make_dag_description(pipeline_name)
    )
    check.subclass_param(operator, 'operator', BaseOperator)

    # black 18.9b0 doesn't support py27-compatible formatting of the below invocation (omitting
    # the trailing comma after **check.opt_dict_param...) -- black 19.3b0 supports multiple python
    # versions, but currently doesn't know what to do with from __future__ import print_function --
    # see https://github.com/ambv/black/issues/768
    # fmt: off
    dag_kwargs = dict(
        {'default_args': DEFAULT_ARGS},
        **check.opt_dict_param(dag_kwargs, 'dag_kwargs', key_type=str)
    )
    # fmt: on

    op_kwargs = check.opt_dict_param(op_kwargs, 'op_kwargs', key_type=str)

    dag = DAG(dag_id=dag_id, description=dag_description, **dag_kwargs)

    pipeline = handle.build_pipeline_definition()

    if mode is None:
        mode = pipeline.get_default_mode_name()

    execution_plan = create_execution_plan(
        pipeline, environment_dict, run_config=RunConfig(mode=mode)
    )

    tasks = {}

    coalesced_plan = coalesce_execution_steps(execution_plan)

    for solid_handle, solid_steps in coalesced_plan.items():

        step_keys = [step.key for step in solid_steps]

        # We separately construct the Airflow operators here with the appropriate args, because if
        # Airflow gets extraneous args/kwargs it emits a warning every time it parses the DAG (and
        # future Airflow versions will mark this a failure).
        # see https://github.com/ambv/black/issues/768
        # fmt: off
        if operator == DagsterPythonOperator:
            task = operator(
                handle=handle,
                pipeline_name=pipeline_name,
                environment_dict=environment_dict,
                mode=mode,
                task_id=solid_handle,
                step_keys=step_keys,
                dag=dag,
                instance_ref=instance.get_ref(),
                **op_kwargs
            )
        else:
            task = operator(
                pipeline_name=pipeline_name,
                environment_dict=environment_dict,
                mode=mode,
                task_id=solid_handle,
                step_keys=step_keys,
                dag=dag,
                instance_ref=instance.get_ref(),
                **op_kwargs
            )
        # fmt: on

        tasks[solid_handle] = task

        for solid_step in solid_steps:
            for step_input in solid_step.step_inputs:
                for key in step_input.dependency_keys:
                    prev_solid_handle = execution_plan.get_step_by_key(key).solid_handle.to_string()
                    if solid_handle != prev_solid_handle:
                        tasks[prev_solid_handle].set_downstream(task)

    return (dag, [tasks[solid_handle] for solid_handle in coalesced_plan.keys()])


def make_airflow_dag(
    module_name,
    pipeline_name,
    environment_dict=None,
    mode=None,
    instance=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
):
    check.str_param(module_name, 'module_name')

    handle = ExecutionTargetHandle.for_pipeline_module(module_name, pipeline_name)

    return _make_airflow_dag(
        handle=handle,
        pipeline_name=pipeline_name,
        environment_dict=environment_dict,
        mode=mode,
        instance=instance,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
    )


def make_airflow_dag_for_handle(
    handle,
    pipeline_name,
    environment_dict=None,
    mode=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
):
    return _make_airflow_dag(
        handle=handle,
        pipeline_name=pipeline_name,
        environment_dict=environment_dict,
        mode=mode,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
    )


def make_airflow_dag_containerized(
    module_name,
    pipeline_name,
    image,
    environment_dict=None,
    mode=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
):
    check.str_param(module_name, 'module_name')

    handle = ExecutionTargetHandle.for_pipeline_module(module_name, pipeline_name)

    op_kwargs = check.opt_dict_param(op_kwargs, 'op_kwargs', key_type=str)
    op_kwargs['image'] = image
    return _make_airflow_dag(
        handle=handle,
        pipeline_name=pipeline_name,
        environment_dict=environment_dict,
        mode=mode,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
        operator=DagsterDockerOperator,
    )


def make_airflow_dag_containerized_for_handle(
    handle,
    pipeline_name,
    image,
    environment_dict=None,
    mode=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
):
    op_kwargs = check.opt_dict_param(op_kwargs, 'op_kwargs', key_type=str)
    op_kwargs['image'] = image
    return _make_airflow_dag(
        handle=handle,
        pipeline_name=pipeline_name,
        environment_dict=environment_dict,
        mode=mode,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
        operator=DagsterDockerOperator,
    )


def make_airflow_dag_kubernetized(
    module_name,
    pipeline_name,
    image,
    namespace,
    environment_dict=None,
    mode=None,
    dag_id=None,
    dag_description=None,
    dag_kwargs=None,
    op_kwargs=None,
):
    from .operators.kubernetes_operator import DagsterKubernetesPodOperator

    check.str_param(module_name, 'module_name')

    handle = ExecutionTargetHandle.for_pipeline_module(module_name, pipeline_name)

    # See: https://github.com/dagster-io/dagster/issues/1663
    op_kwargs = check.opt_dict_param(op_kwargs, 'op_kwargs', key_type=str)
    op_kwargs['image'] = image
    op_kwargs['namespace'] = namespace

    return _make_airflow_dag(
        handle=handle,
        pipeline_name=pipeline_name,
        environment_dict=environment_dict,
        mode=mode,
        dag_id=dag_id,
        dag_description=dag_description,
        dag_kwargs=dag_kwargs,
        op_kwargs=op_kwargs,
        operator=DagsterKubernetesPodOperator,
    )

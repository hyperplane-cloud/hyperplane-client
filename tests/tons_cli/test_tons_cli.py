import json
import logging
from unittest.mock import patch
from click.testing import CliRunner
from tons_cli.__main__ import cli
from hyperplane_definitions.job_consts import JOB_CANCELLED_BY_USER


def test_cli_get_token_from_env():
    runner = CliRunner()
    test_token_value = 'FakeTokenValue'
    with (
        patch("tons_cli.common.get_path_to_conf_dir", return_value="."),
        runner.isolated_filesystem(),
    ):
        result = runner.invoke(cli, args=['token', 'get'], env={'HYPERPLANE_API_TOKEN': test_token_value})
        assert result.exit_code == 0
        assert test_token_value == result.output.strip()


def test_cli_set_token_to_config():
    runner = CliRunner()
    test_token_value = 'FakeTokenValue'
    with (
        patch("tons_cli.common.get_path_to_conf_dir", return_value="."),
        runner.isolated_filesystem(),
    ):
        logging.getLogger().setLevel(logging.ERROR)
        result = runner.invoke(cli, args=['token', 'set', test_token_value], env={})
        assert result.exit_code == 0
        assert "Token saved!" == result.output.strip()
        result = runner.invoke(cli, args=['token', 'get'], env={})
        assert result.exit_code == 0
        assert test_token_value == result.output.strip()


def test_job():
    runner = CliRunner()
    logging.getLogger().setLevel(logging.ERROR)
    instance_type = "t2.medium"
    repo_name = "tests-repo"
    repo_url = f"https://github.com/hyperplane-cloud/{repo_name}"
    job_name = f"CLI - {repo_name}"
    # Run job
    job_run_args = [
        'job', 'create',
        "--repo", repo_url,
        "--instance-type", instance_type,
    ]
    result_run = runner.invoke(cli, args=job_run_args)
    assert result_run.exit_code == 0
    result_run_json = json.loads(result_run.output.strip())
    job_id = result_run_json['job_id']
    # Abort it immediately
    result_abort = runner.invoke(cli, args=['job', 'abort', job_id])
    assert result_abort.exit_code == 0
    assert f"Job {job_id} aborted" == result_abort.output.strip()
    # Get job and see it is canceled
    result_get = runner.invoke(cli, args=['job', 'get', job_id])
    assert result_get.exit_code == 0
    job_dict_s = result_get.output.strip()
    job_dict = json.loads(job_dict_s)
    assert job_dict['ID'] == job_id
    assert job_dict['job_status'] == JOB_CANCELLED_BY_USER
    assert job_dict['git_repo_url'] == repo_url
    assert job_dict['instance_type'] == instance_type
    # Get all jobs and find the canceled job
    result_all = runner.invoke(cli, args=['job', 'all'])
    assert result_all.exit_code == 0
    result_all_s = result_all.output.strip()
    result_all_lines = result_all_s.split('\n')
    expected_job_line = f"Job {job_id} [{JOB_CANCELLED_BY_USER}] {job_name} on {instance_type}"
    assert any(line.strip() == expected_job_line for line in result_all_lines) 


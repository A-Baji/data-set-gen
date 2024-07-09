from json import dumps, loads

from pytest import mark
from . import expected_values
from .conftest import CHANNEL_ID, USER


def test_cli_help(script_runner):
    cli = script_runner.run(["discordai_modelizer", "-h"])
    assert cli.success
    assert "usage: discordai_modelizer [-h] [-V] {model,job} ..." in cli.stdout

    assert "DiscordAI Modelizer CLI" in cli.stdout
    assert "positional arguments:" in cli.stdout
    assert "{model,job}" in cli.stdout
    assert "option" in cli.stdout
    assert "-h, --help     show this help message and exit" in cli.stdout
    assert "-V, --version  show program's version number and exit" in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_model_list(script_runner, command):
    cli = script_runner.run([command, "model", "list"])
    assert cli.success
    for o in expected_values.list_module_expected:
        assert o in loads(cli.stdout)


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_training(script_runner, command, default_file_output):
    cli = script_runner.run(
        [
            command,
            "model",
            "create",
            "-c",
            f"{CHANNEL_ID}",
            "-u",
            f"{USER}",
            "-o",
            "BAD_KEY",
            "-b",
            "babbage",
        ]
    )
    assert not cli.success
    assert "INFO: Starting OpenAI fine-tune job..." in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_model_list_full(script_runner, command):
    cli = script_runner.run([command, "model", "list", "--full"])
    assert cli.success
    for o in expected_values.list_module_expected_full:
        assert o in loads(cli.stdout)


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_delete_model(script_runner, command):
    cli = script_runner.run([command, "model", "delete", "-m", "whisper-1"])
    assert (
        "Are you sure you want to delete this model? This action is not reversable. Y/N: "
        in cli.stdout
    )


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_job_list(script_runner, command):
    cli = script_runner.run([command, "job", "list"])
    assert cli.success
    assert dumps(expected_values.list_job_expected, indent=4) in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_job_list_full(script_runner, command):
    cli = script_runner.run([command, "job", "list", "--full"])
    assert cli.success
    assert dumps(expected_values.list_job_expected_full, indent=4) in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_job_info(script_runner, command):
    cli = script_runner.run(
        [command, "job", "info", "-j", "ftjob-i2IyeV2xbLCSrYq45kTKSdwE"]
    )
    assert cli.success
    assert dumps(expected_values.job_info_expected, indent=4) in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_job_events(script_runner, command):
    cli = script_runner.run(
        [command, "job", "events", "-j", "ftjob-i2IyeV2xbLCSrYq45kTKSdwE"]
    )
    assert cli.success
    assert dumps(expected_values.job_events_expected, indent=4) in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_job_cancel(script_runner, command):
    cli = script_runner.run(
        [command, "job", "cancel", "-j", "ftjob-i2IyeV2xbLCSrYq45kTKSdwE"]
    )
    assert cli.success
    assert dumps(expected_values.job_cancel_expected, indent=4) in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_job_cancel(script_runner, command):
    cli = script_runner.run(
        [command, "job", "cancel", "-j", "ftjob-i2IyeV2xbLCSrYq45kTKSdwE"]
    )
    assert cli.success
    assert dumps(expected_values.job_cancel_expected, indent=4) in cli.stdout


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_model_bad_args(script_runner, command):
    cli = script_runner.run(
        [
            command,
            "model",
        ]
    )
    assert not cli.success
    assert "Must choose a command from `list`, `create`, or `delete`" in cli.stderr


@mark.parametrize("command", ["discordai_modelizer"])
def test_cli_job_bad_args(script_runner, command):
    cli = script_runner.run(
        [
            command,
            "job",
        ]
    )
    assert not cli.success
    assert (
        "Must choose a command from `list`, `info`, `events`, or `cancel`" in cli.stderr
    )

import argparse
import json
from discordai_modelizer import __version__ as version
from discordai_modelizer import customize
from discordai_modelizer import openai as openai_wrapper


def discordai_modelizer():
    parser = argparse.ArgumentParser(
        prog="discordai_modelizer", description="DiscordAI Modelizer CLI"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command = parser.add_subparsers(dest="command")

    model = command.add_parser(
        "model", description="Commands related to your openAI models"
    )
    job = command.add_parser("job", description="Commands related to your openAI jobs")

    model_subcommand = model.add_subparsers(dest="subcommand")
    job_subcommand = job.add_subparsers(dest="subcommand")

    model_list = model_subcommand.add_parser(
        "list", description="List your openAi customized models"
    )
    model_list.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key to list the models for",
    )
    model_list.add_argument(
        "--full",
        action="store_true",
        required=False,
        dest="full",
        help="Return the full details of all the models",
    )

    model_create = model_subcommand.add_parser(
        "create",
        description="Create a new openAI customized model by downloading the specified chat logs, parsing them into a usable dataset, and then training a customized model using openai",
    )
    model_create_required_named = model_create.add_argument_group(
        "required named arguments"
    )
    model_create_required_named.add_argument(
        "-d",
        "--discord-token",
        type=str,
        dest="discord_token",
        help="The discord token for your bot",
    )
    model_create_required_named.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key to use to create the model",
    )
    model_create_required_named.add_argument(
        "-c",
        "--channel",
        type=str,
        dest="channel",
        help="The ID of the discord channel you want to use",
    )
    model_create_required_named.add_argument(
        "-u",
        "--user",
        type=str,
        dest="user",
        help="The username of the discord user you want to use",
    )
    model_create_optional_named = model_create.add_argument_group(
        "optional named arguments"
    )
    model_create_optional_named.add_argument(
        "-b",
        "--base-model",
        choices=["gpt3", "davinci", "babbage", "none"],
        default="none",
        required=False,
        dest="base_model",
        help="The base model to use for customization. If none, then skips training step: DEFAULT=none",
    )
    model_create_optional_named.add_argument(
        "--ttime",
        "--thought-time",
        type=int,
        default=10,
        required=False,
        dest="thought_time",
        help='The maximum amount of time in seconds to consider two individual messages to be part of the same "thought": DEFAULT=10',
    )
    model_create_optional_named.add_argument(
        "--tmax",
        "--thought-max",
        type=int,
        default=None,
        required=False,
        dest="thought_max",
        help="The maximum length in words of each thought: DEFAULT=None",
    )
    model_create_optional_named.add_argument(
        "--tmin",
        "--thought-min",
        type=int,
        default=4,
        required=False,
        dest="thought_min",
        help="The minimum length in words of each thought: DEFAULT=4",
    )
    model_create_optional_named.add_argument(
        "-m",
        "--max-entries",
        type=int,
        default=1000,
        required=False,
        dest="max_entries",
        help="The max amount of entries (by lines) that may exist in the dataset: DEFAULT=1000",
    )
    model_create_optional_named.add_argument(
        "--os",
        "--offset",
        type=int,
        default=0,
        required=False,
        dest="offset",
        help="The offset by line number for where to start selecting lines for the dataset: DEFAULT=0",
    )
    model_create_optional_named.add_argument(
        "-s",
        "--select-mode",
        choices=["sequential", "distributed"],
        default="sequential",
        required=False,
        dest="select_mode",
        help="The method to select lines for the dataset, where `sequential` mode will select lines in chronological order, while `distributed` mode will select an even distribution of lines: DEFAULT=sequential",
    )
    model_create_optional_named.add_argument(
        "--reverse",
        action="store_true",
        required=False,
        dest="reverse",
        help="Reverse the order in which to select lines for the dataset",
    )
    model_create_optional_named.add_argument(
        "--dirty",
        action="store_false",
        required=False,
        dest="dirty",
        help="Skip the clean up step for outputted files",
    )
    model_create_optional_named.add_argument(
        "--redownload",
        action="store_true",
        required=False,
        dest="redownload",
        help="Redownload the discord chat logs",
    )
    model_create_optional_named.add_argument(
        "--use_existing",
        action="store_true",
        required=False,
        dest="use_existing",
        help="Use an existing dataset that may have been manually revised",
    )

    model_delete = model_subcommand.add_parser(
        "delete", description="Delete an openAI customized model"
    )
    model_delete.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the model to delete",
    )
    model_delete.add_argument(
        "-m",
        "--model-id",
        type=str,
        dest="model_id",
        help="Target model id",
    )

    job_list = job_subcommand.add_parser(
        "list", description="List your openAI customization jobs"
    )
    job_list.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key to list the jobs for",
    )
    job_list.add_argument(
        "--full",
        action="store_true",
        required=False,
        dest="full",
        help="Return the full details of all the jobs",
    )

    job_info = job_subcommand.add_parser(
        "info", description="Get an openAI customization job's info"
    )
    job_info.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the job to see the info for",
    )
    job_info.add_argument(
        "-j",
        "--job-id",
        type=str,
        dest="job_id",
        help="Target job id",
    )

    job_events = job_subcommand.add_parser(
        "events", description="Get an openAI customization job's events"
    )
    job_events.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the job to see the events for",
    )
    job_events.add_argument(
        "-j",
        "--job-id",
        type=str,
        dest="job_id",
        help="Target job id",
    )

    job_cancel = job_subcommand.add_parser(
        "cancel", description="Cancel an openAI customization job"
    )
    job_cancel.add_argument(
        "-o",
        "--openai-key",
        type=str,
        dest="openai_key",
        help="The openAI API key associated with the job to cancel",
    )
    job_cancel.add_argument(
        "-j",
        "--job-id",
        type=str,
        dest="job_id",
        help="Target job id",
    )

    args = parser.parse_args()
    if args.command == "model":
        if args.subcommand == "list":
            display(openai_wrapper.list_models(args.openai_key, args.full))
        if args.subcommand == "create":
            customize.create_model(
                args.discord_token,
                args.openai_key,
                args.channel,
                args.user,
                thought_time=args.thought_time,
                thought_max=args.thought_max,
                thought_min=args.thought_min,
                max_entry_count=args.max_entries,
                offset=args.offset,
                select_mode=args.select_mode,
                reverse=args.reverse,
                base_model=args.base_model,
                clean=args.dirty,
                redownload=args.redownload,
                use_existing=args.use_existing,
            )
        if args.subcommand == "delete":
            display(openai_wrapper.delete_model(args.openai_key, args.model_id))
    elif args.command == "job":
        if args.subcommand == "list":
            display(openai_wrapper.list_jobs(args.openai_key, args.full))
        if args.subcommand == "info":
            display(openai_wrapper.get_job_info(args.openai_key, args.job_id))
        if args.subcommand == "events":
            display(openai_wrapper.get_job_events(args.openai_key, args.job_id))
        if args.subcommand == "cancel":
            display(openai_wrapper.cancel_job(args.openai_key, args.job_id))


def display(obj):
    print(json.dumps(obj, indent=4))


if __name__ == "__main__":
    discordai_modelizer()

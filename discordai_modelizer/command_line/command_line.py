import argparse
import json
import os
from discordai_modelizer import __version__ as version
from discordai_modelizer import customize
from discordai_modelizer import openai as openai_wrapper
from discordai_modelizer.command_line import subparsers


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

    subparsers.setup_model_list(model_subcommand)
    subparsers.setup_model_create(model_subcommand)
    subparsers.setup_model_delete(model_subcommand)

    subparsers.setup_job_list(job_subcommand)
    subparsers.setup_job_info(job_subcommand)
    subparsers.setup_job_events(job_subcommand)
    subparsers.setup_job_cancel(job_subcommand)

    args = parser.parse_args()
    if hasattr(args, "openai_key"):
        openai_wrapper.set_openai_api_key(args.openai_key)

    if args.command == "model":
        if args.subcommand == "list":
            display(openai_wrapper.list_models(os.environ["OPENAI_API_KEY"], args.full))
        elif args.subcommand == "create":
            customize.create_model(
                args.channel,
                args.user,
                args.discord_token,
                os.environ["OPENAI_API_KEY"],
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
        elif args.subcommand == "delete":
            display(
                openai_wrapper.delete_model(args.model_id, os.environ["OPENAI_API_KEY"])
            )
        else:
            raise argparse.ArgumentError(
                model_subcommand,
                "Must choose a command from `list`, `create`, or `delete`",
            )
    elif args.command == "job":
        if args.subcommand == "list":
            display(openai_wrapper.list_jobs(os.environ["OPENAI_API_KEY"], args.full))
        elif args.subcommand == "info":
            display(
                openai_wrapper.get_job_info(args.job_id, os.environ["OPENAI_API_KEY"])
            )
        elif args.subcommand == "events":
            display(
                openai_wrapper.get_job_events(args.job_id, os.environ["OPENAI_API_KEY"])
            )
        elif args.subcommand == "cancel":
            display(
                openai_wrapper.cancel_job(args.job_id, os.environ["OPENAI_API_KEY"])
            )
        else:
            raise argparse.ArgumentError(
                job_subcommand,
                "Must choose a command from `info`, `events`, or `cancel`",
            )


def display(obj):
    print(json.dumps(obj, indent=4))


if __name__ == "__main__":
    discordai_modelizer()

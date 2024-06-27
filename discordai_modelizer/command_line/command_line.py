import argparse
import json
from discordai_modelizer import __version__ as version
from discordai_modelizer import customize
from discordai_modelizer import openai as openai_wrapper
from discordai_modelizer import command_line


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

    command_line.subparsers.setup_model_list(model_subcommand)
    command_line.subparsers.setup_model_create(model_subcommand)
    command_line.subparsers.setup_model_delete(model_subcommand)

    command_line.subparsers.setup_job_list(job_subcommand)
    command_line.subparsers.setup_job_info(job_subcommand)
    command_line.subparsers.setup_job_events(job_subcommand)
    command_line.subparsers.setup_job_cancel(job_subcommand)

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

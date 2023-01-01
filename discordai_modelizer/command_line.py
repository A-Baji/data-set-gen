import argparse
from discordai_modelizer import __version__ as version
from discordai_modelizer import customize


def discordai_modelizer():
    parser = argparse.ArgumentParser(
        prog="discordai_modelizer", description="DiscordAI Modelizer CLI")
    parser.add_argument(
        "-V", "--version", action="version", version=f"discordai {version}"
    )
    command = parser.add_subparsers(dest="command")

    openai = command.add_parser("openai", description="OpenAI model customizer and API wrapper")
    openai_subcommand = openai.add_subparsers(dest="subcommand")

    openai_create = openai_subcommand.add_parser(
        "create", description="Create a new custom openAI model"
    )
    openai_create_required_named = openai_create.add_argument_group(
        "required named arguments"
    )
    openai_create_required_named.add_argument(
        "-d", "--discord_token",
        type=str,
        dest='discord_token',
        help="The discord token for your bot",
    )
    openai_create_required_named.add_argument(
        "-o", "--openai_key",
        type=str,
        dest='openai_key',
        help="Your openAI API key",
    )
    openai_create_required_named.add_argument(
        "-c", "--channel",
        type=str,
        dest='channel',
        help="The ID of the discord channel you want to use",
    )
    openai_create_required_named.add_argument(
        "-u", "--user",
        type=str,
        dest='user',
        help="The name#ID of the discord user you want to use",
    )

    openai_create_optional_named = openai_create.add_argument_group("optional named arguments")
    openai_create_optional_named.add_argument(
        "-b", "--base_model",
        choices=["davinci", "curie", "babbage", "ada", "none"],
        default="none",
        required=False,
        dest='base_model',
        help="The base model to use for customization. If none, then skips training step: DEFAULT=none",
    )
    openai_create_optional_named.add_argument(
        "-t", "--thought_time",
        type=int,
        default=10,
        required=False,
        dest='thought_time',
        help="The max amount of time in seconds to consider two individual messages to be part of the same \"thought\": DEFAULT=10",
    )
    openai_create_optional_named.add_argument(
        "-m", "--max_entries",
        type=int,
        default=1000,
        required=False,
        dest='max_entries',
        help="The max amount of entries that may exist in the dataset: DEFAULT=1000",
    )
    openai_create_optional_named.add_argument(
        "-r", "--reduce_mode",
        choices=["first", "last", "middle", "even"],
        default="even",
        required=False,
        dest='reduce_mode',
        help="The method to reduce the entry count of the dataset: DEFAULT=even",
    )
    openai_create_optional_named.add_argument(
        "--clean",
        action='store_true',
        required=False,
        dest='clean',
        help="A flag that can be set to clean up outputted files: DEFAULT=False",
    )
    openai_create_optional_named.add_argument(
        "--redownload",
        action='store_true',
        required=False,
        dest='redownload',
        help="A flag that can be set to redownload the discord chat logs: DEFAULT=False",
    )

    args = parser.parse_args()
    if args.command == "openai":
        if args.subcommand == "create":
            customize.create_model(args.discord_token, args.openai_key, args.channel, args.user,
                                   thought_time=args.thought_time, max_entry_count=args.max_entries,
                                   reduce_mode=args.reduce_mode, base_model=args.base_model, clean=args.clean,
                                   redownload=args.redownload)


if __name__ == "__main__":
    discordai_modelizer()

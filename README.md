# DiscordAI Modelizer
DiscordAI Modelizer is a python package that can generate custom openai models based on a discord user's chat history in a discord channel. It uses [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) to download the logs of a channel. Then, after the logs are processed into a usable dataset, it uses [openAI's API](https://beta.openai.com/docs/introduction) to create a customized model. It also wraps some of the tools from the openAI API to help with managing customizations.

DiscordAI Modelizer is primarily used as a subcomponent of [DiscordAI](https://github.com/A-Baji/discordAI), but may also be used independently.

## Installation
1. Download/clone the source locally
2. Run `pip install <path to source>/.`
3. The source may now be deleted

## Commands
### `discord_modelizer openai create`
This command will download the specified chat logs, parse them into a usable dataset, then create a customized model using openai.
### `discord_modelizer openai list_jobs`
This command will list all of the openai customization jobs associated with a specified api key.
### `discord_modelizer openai list_models`
This command will list all of the openai customized models associated with a specified api key.
### `discord_modelizer openai follow`
This command will output the event stream of a specified customization job process.
### `discord_modelizer openai status`
This command will output the status of a specified customization job.
### `discord_modelizer openai cancel`
This command will cancel a specified customization job.
### `discord_modelizer openai delete`
This command will delete a specified customized model.

## Disclaimer
This application allows users to download the chat history of any channel for which they have permission to invite a bot. It is important to note that this application should only be used with the consent of all members of the channel. Using this application for malicious purposes or without the consent of all members is strictly prohibited.

By using this application, you agree to use it responsibly and in accordance with all applicable laws and regulations. The developers of this application are not responsible for any improper use of the application or any consequences resulting from such use. We strongly discourage using this application for any unethical purposes.
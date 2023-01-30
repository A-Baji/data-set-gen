# DiscordAI Modelizer
DiscordAI Modelizer is a python package that can generate custom openai models based on a discord user's chat history in a discord channel. It uses [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) to download the logs of a channel. Then, after the logs are processed into a usable dataset, it uses [openAI's API](https://beta.openai.com/docs/introduction) to create a customized model. It also wraps some of the tools from the openAI API to help with managing customizations.

DiscordAI Modelizer is primarily used as a subcomponent of [DiscordAI](https://github.com/A-Baji/discordAI), but may also be used independently.

## Installation
`pip install -U git+https://github.com/A-Baji/discordAI-modelizer.git`
### Or
1. Download/clone the source locally
2. Run `pip install -U <path to source>/.`
3. The source may now be deleted

## Commands
### Model
Commands related to your openAI models
#### `discordai_modelizer model list`
List your openAi customized models
#### `discordai_modelizer model create`
Create a new openAI customized model by downloading the specified chat logs, parsing them into a usable dataset, and then training a customized model using openai

For a proper usage, see the [guide](https://github.com/A-Baji/discordAI#create-a-new-customized-openai-model) for DiscordAI.
#### `discordai_modelizer model delete`
Delete an openAI customized model
### Job
Commands related to your openAI jobs
#### `discordai_modelizer job list`
List your openAI customization jobs
#### `discordai_modelizer job follow`
Follow an openAI customization job
#### `discordai_modelizer job status`
Get an openAI customization job's status
#### `discordai_modelizer job cancel`
Cancel an openAI customization job

## Disclaimer
This application allows users to download the chat history of any channel for which they have permission to invite a bot, and then use those logs to create an openai model based on a user's chat messages. It is important to note that this application should only be used with the consent of all members of the channel. Using this application for malicious purposes, such as impersonation, or without the consent of all members is strictly prohibited.

By using this application, you agree to use it responsibly. The developers of this application are not responsible for any improper use of the application or any consequences resulting from such use. We strongly discourage using this application for any unethical purposes.
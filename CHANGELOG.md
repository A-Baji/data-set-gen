# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [1.2.2] - 02-22-2023

### Fixed

- Bug with end of thought punctuation

## [1.2.1] - 02-19-2023

### Fixed

- Bug with min and max thought length

## [1.2.0] - 02-17-2023

### Added

- events flag for job status command
- min and max thought length parameters for model creation

## [1.1.0] - 02-11-2023

### Changed

- Replaced `subprocess` instances with appropriate openAI python API methods

### Removed

- Dataset clean up step with openAI fine tune API

## [1.0.1] - 02-11-2023

### Changed

- Switch to `pathlib` for file path parsing

[1.2.2]: https://github.com/A-Baji/discordAI-modelizer/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/A-Baji/discordAI-modelizer/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/A-Baji/discordAI-modelizer/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/A-Baji/discordAI-modelizer/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/A-Baji/discordAI-modelizer/compare/1.0.0...1.0.1
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- The `host` method 'rotate-api-key' is now available in CLI and SDK to manage hosts
  [cyberark/conjur-api-python3#101](https://github.com/cyberark/conjur-api-python3/issues/101)
- The `user` methods 'rotate-api-key' and 'change-password' are now available in CLI and SDK to manage users
  [cyberark/conjur-api-python3#101](https://github.com/cyberark/conjur-api-python3/issues/101)
- Add ability to get previous variable/secret versions. This is available in both CLI and SDK
  [cyberark/conjur-api-python3#151](https://github.com/cyberark/conjur-api-python3/issues/151)
- The `list` flag constraints are now available in both CLI and SDK to filter resource results
  [cyberark/conjur-api-python3#128](https://github.com/cyberark/conjur-api-python3/issues/91)
- The `login\logout` methods are now available in CLI to login and out of the CLI
  [cyberark/conjur-api-python3#128](https://github.com/cyberark/conjur-api-python3/issues/128)
- The `init` method is now available in CLI to initialize the CLI with the Conjur server
  [cyberark/conjur-api-python3#89](https://github.com/cyberark/conjur-api-python3/issues/89)

### Changed
- CLI command UX has been improved according to UX guidelines
  [cyberark/conjur-api-python3#132](https://github.com/cyberark/conjur-api-python3/issues/132)
  See [design guidelines](https://ljfz3b.axshare.com/#id=x8ktq8&p=conjur_help__init&g=1)
- Update version from 0.x.x to 7.0.0 to prep for the GA release
- Update help screens according to [these guidelines](https://ljfz3b.axshare.com/#id=yokln4&p=conjur_main_help&g=1).
  [cyberark/conjur-api-python3#92](https://github.com/cyberark/conjur-api-python3/issues/92)

## [0.1.1] - 2020-11-05

### Added
- Method `whoami` is now available in both CLI and API (requires Conjur v1.9+).
  [cyberark/conjur-api-python3#68](https://github.com/cyberark/conjur-api-python3/pull/68)

### Changed
- Removed references to `enum.auto` to support Python3.5
  [cyberark/conjur-api-python3#43](https://github.com/cyberark/conjur-api-python3/issues/43)

## [0.1.0] - 2020-01-03
### Added
- Added ability to publish the container to DockerHub
  [cyberark/conjur-api-python3#28](https://github.com/cyberark/conjur-api-python3/issues/28)
- Changed test container to use Ubuntu instead of Alpine

## [0.0.5] - 2019-12-06

### Added
- Added ability to delete policies [cyberark/conjur-api-python3#23](https://github.com/cyberark/conjur-api-python3/issues/23)

## [0.0.4] - 2019-11-21

### Fixed
- Fixed overrides handling of `Client` account param
  [cyberark/conjur-api-python3#21](https://github.com/cyberark/conjur-api-python3/issues/21)
- Fixed running of linter due to `cryptography` upstream bug
- Fixed failing tests when running on different OS YAML parsing libraries

## [0.0.3] - 2019-08-20

### Fixed
- Fixed application of conjurrc overrides of `Client` initialization params
  [cyberark/conjur-api-python3#14](https://github.com/cyberark/conjur-api-python3/issues/14)
- Fixed escaping of `/` in parameters of URL

## [0.0.2] - 2019-05-17

### Changed
- Package prefix changed from `conjur_api_python3` to `conjur`
- Bundle name changed from `conjur-api-python` to `conjur-api`
- CLI renamed from `conjur-py3-cli` to `conjur-cli`

### Added
- Support for returning output from policy changes invocations
- Fatal exception is raised when this module is run on Python2

## [0.0.1] - 2019-05-01
### Added
- The first tagged version.

[Unreleased]: https://github.com/conjurinc/conjur-api-python3/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/conjurinc/conjur-api-python3/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/conjurinc/conjur-api-python3/compare/v0.0.5...v0.1.0
[0.0.5]: https://github.com/conjurinc/conjur-api-python3/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/conjurinc/conjur-api-python3/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/conjurinc/conjur-api-python3/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/conjurinc/conjur-api-python3/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/cyberark/conjur-api-python3/releases/tag/v0.0.1

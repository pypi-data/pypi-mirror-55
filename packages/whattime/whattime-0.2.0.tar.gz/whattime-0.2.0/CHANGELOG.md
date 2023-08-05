# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] – 2019-11-05
### Fixed
* Broken hour ranges for `day_time_info()`

### Added 
* `season_info` function to get info about the season of the date: provides `is_spring`, `is_summer`, `is_autumn`, and `is_winter`.  
This is dependent on the configured hemisphere (see `whattime.Hemisphere` enum).  
Season info properties are also available when using `whattime(date, hemisphere)`.
* Travis CI config

### Changed
* The formerly `whattime(date: datetime)` now takes 2 arguments: the datetime object and a Hemisphere enum 

## [0.1.1] – 2019-10-25
### Fixed
* Update requirements in order to fix vulnerabilities with urllib3 v1.24.1

## [0.1.0] – 2019-03-11
Initial release

[Unreleased]: https://github.com/grammofy/whattime/compare/0.2.0...HEAD
[0.2.0]: https://github.com/grammofy/whattime/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/grammofy/whattime/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/grammofy/whattime/compare/61790defe4d729a105183b9793a12641410fd4a7...0.1.0

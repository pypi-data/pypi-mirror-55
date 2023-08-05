# whattime

[![PyPI version](https://badge.fury.io/py/whattime.svg)](https://badge.fury.io/py/whattime)
[![Build Status](https://travis-ci.org/grammofy/whattime.svg?branch=master)](https://travis-ci.org/grammofy/whattime)

Checking of what kind a datetime object is: it let’s you explore whether a certain datetime object is e.g. a Sunday morning in summer or a Wednesday night in winter. It also consideres hemispheres.

## Getting started

Install it with:

```bash
pip install whattime
```

or 

```bash
pipenv install whattime
```

For quickly getting started, just import the `whattime` function and explore a date’s properties (also see the [Get started example](https://github.com/grammofy/whattime/blob/master/examples/get_started.py)):

```python
from datetime import datetime
from whattime import whattime, Hemisphere

now = datetime.now()
info = whattime(now, Hemisphere.SOUTHERN)

info.is_weekday
info.is_monday
info.is_summer
# ...
```

Besides checking all the time types you can also only check a certain category of types, e.g. info about the current day, or the time within a day seperately (also see the [Single info type example](https://github.com/grammofy/whattime/blob/master/examples/using_certain_descriptors_only.py)).

```python
from datetime import datetime
from whattime import week_info, day_time_info, season_info, Hemisphere

now = datetime.now()

# There will only be properties available concerning the week time info when using week_info():
info = week_info(now)
info.is_weekday
info.is_monday
# ...

# There will only be properties available concerning the day time info when using day_time_info():
info = day_time_info(now)
info.is_afternoon
info.is_evening
# ...

# There will only be properties available concerning the season info when using season_info():
info = season_info(now, Hemisphere.SOUTHERN)
info.is_spring
info.is_summer
# ...
```

## Development

* Check out the repo with `git clone git@github.com:grammofy/whattime.git`.
* To set up the project for development you need to [install Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) and run:  
  ```bash
  pipenv install --dev
  ```
  in order to install the needed development requirements.

* Tests can be run with: 
  ```bash
  python setup.py test
  ```

## Contributing

Bug reports, feature discussions and pull requests are welcome on GitHub at https://github.com/grammofy/whattime. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant Code of Conduct](https://github.com/grammofy/whattime/blob/master/CODE_OF_CONDUCT.md).

Here’s how to contribute:

* Fork it (https://github.com/grammofy/whattime/fork)
* Create your feature branch (`git checkout -b feature/my-new-feature master`)
* Commit your changes (`git commit -am 'Add some feature'`)
* Push to the branch (`git push origin feature/my-new-feature`)
* Create a new Pull Request

Please try to add [Pytest tests](https://pytest.org/en/latest/getting-started.html) along with your new feature. This will ensure that your code does not break existing functionality and that your feature is working as expected.

## License

The software is available as open source under the terms of the [MIT License](https://github.com/grammofy/whattime/blob/master/LICENSE.txt).

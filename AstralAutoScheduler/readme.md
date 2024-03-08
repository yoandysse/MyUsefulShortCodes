# AstralAutoScheduler

AstralAutoScheduler is a Python application that manages cron jobs based on astral times. It uses the astral library to calculate sunrise and sunset times for a given location and sets cron jobs to run at these times.

## Features

- Deletes the previous cron job that has the astral time in its comment.
- Adds a new cron job with the given command to be executed at the given astral time.
- Returns the astral time for the given type (e.g., 'sunset', 'sunrise').
- Adds a daemon job to run this script every day at 00:00.
- Main method to run the scheduler. It checks if a daemon job exists, if not it adds one. It also deletes the previous astral time job and adds a new one.

## Installation

This project requires Python 3 and pip. Once you have these installed, you can install the required packages using:

```bash
pip install -r requirements.txt
```

## Usage

To use this application, you need to create an instance of the `AstralAutoScheduler` class with the necessary parameters. Here is an example:

```python
params = {
    "ciudad": "Madrid",
    "pais": "España",
    "timezone": "Europe/Madrid",
    "latitud": 40.4239885,
    "longitud": -3.6949247,
    "astral_time": "sunset",
    "command": "echo 'Hola Mundo'"
}

scheduler = AstralAutoScheduler(params)
scheduler.run()
```

In this example, a new cron job will be created that echoes 'Hola Mundo' at sunset in Madrid, Spain.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

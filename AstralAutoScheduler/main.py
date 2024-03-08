from crontab import CronTab
import pathlib
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz

class AstralAutoScheduler:
    """
    A class used to manage cron jobs based on astral times.

    ...

    Attributes
    ----------
    route_file : str
        a string representing the absolute path of the current file
    params : dict
        a dictionary containing the parameters for the astral time calculation

    Methods
    -------
    del_previous_astral_time_job():
        Deletes the previous cron job that has the astral time in its comment.
    add_astral_time_job(command: str, astral_time: datetime):
        Adds a new cron job with the given command to be executed at the given astral time.
    get_astral_time(astral_time: str) -> datetime:
        Returns the astral time for the given type (e.g., 'sunset', 'sunrise').
    add_daemon_job():
        Adds a daemon job to run this script every day at 00:00.
    run():
        Main method to run the scheduler. It checks if a daemon job exists, if not it adds one.
        It also deletes the previous astral time job and adds a new one.
    """

    def __init__(self, params):
        """
        Constructs all the necessary attributes for the AstralAutoScheduler object.

        Parameters
        ----------
            params : dict
                a dictionary containing the parameters for the astral time calculation
        """
        self.route_file = pathlib.Path(__file__).resolve()
        self.params = params

    def del_previous_astral_time_job(self):
        """
        Deletes the previous cron job that has the astral time in its comment.
        """
        for job in self.cron:
            if self.params['astral_time'] in job.comment:
                self.cron.remove(job)
                self.cron.write()
                print('Job removed')
                continue

    def add_astral_time_job(self, command, astral_time):
        """
        Adds a new cron job with the given command to be executed at the given astral time.

        Parameters
        ----------
            command : str
                the command to be executed by the cron job
            astral_time : datetime
                the time at which the cron job should be executed
        """
        job = self.cron.new(command=command, comment=self.params['astral_time'])
        job.setall(astral_time)
        self.cron.write()
        print('Job added')

    def get_astral_time(self, astral_time):
        """
        Returns the astral time for the given type (e.g., 'sunset', 'sunrise').

        Parameters
        ----------
            astral_time : str
                the type of astral time to calculate

        Returns
        -------
            datetime
                the calculated astral time
        """
        city = LocationInfo(params['ciudad'], params['pais'], params['latitud'], params['longitud'])
        s = sun(city.observer, date=datetime.now(pytz.timezone(params['timezone'])))
        astral_time = s[astral_time].astimezone(pytz.timezone(params['timezone']))
        return astral_time

    def add_daemon_job(self):
        """
        Adds a daemon job to run this script every day at 00:00.
        """
        command = f'python {self.route_file}'
        job = self.cron.new(command=command)
        job.setall('0 0 * * *')
        self.cron.write()

    def run(self):
        """
        Main method to run the scheduler. It checks if a daemon job exists, if not it adds one.
        It also deletes the previous astral time job and adds a new one.
        """
        print('Hora de Ejecucion:', self.get_astral_time(self.params['astral_time']))

        self.cron = CronTab(user=True)

        # check if daemon job exists
        daemon_exists = False
        for job in self.cron:
            if self.route_file.__str__() in job.command:
                daemon_exists = True
                break
        if not daemon_exists:
            self.add_daemon_job()

        # deletes the previous astral time job
        self.del_previous_astral_time_job()

        # add a new astral time job
        self.add_astral_time_job(self.params['command'], self.get_astral_time(self.params['astral_time']))

        print('AstralAutoScheduler is executed')


if __name__ == '__main__':
    # Define tu ubicación
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
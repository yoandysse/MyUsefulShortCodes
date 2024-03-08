from crontab import CronTab
import pathlib
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz


class AstralAutoScheduler:
    def __init__(self, params):
        self.route_file = pathlib.Path(__file__).resolve()
        self.params = params

    def del_previous_astral_time_job(self):
        for job in self.cron:
            if self.params['astral_time'] in job.comment:
                self.cron.remove(job)
                self.cron.write()
                print('Job removed')
                continue

    def add_astral_time_job(self, command, astral_time):
        job = self.cron.new(command=command, comment=self.params['astral_time'])
        job.setall(astral_time)
        self.cron.write()
        print('Job added')

    def get_astral_time(self, astral_time):
        city = LocationInfo(params['ciudad'], params['pais'], params['latitud'], params['longitud'])
        s = sun(city.observer, date=datetime.now(pytz.timezone(params['timezone'])))
        astral_time = s[astral_time].astimezone(pytz.timezone(params['timezone']))
        return astral_time

    def add_daemon_job(self):
        # daemon job to run this python script every day at 00:00
        command = f'python {self.route_file}'
        job = self.cron.new(command=command)
        job.setall('0 0 * * *')
        self.cron.write()

    def run(self):
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

        # eliminar astral_time job previo
        self.del_previous_astral_time_job()

        # añadir nuevo astral_time job
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


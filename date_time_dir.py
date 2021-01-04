import os
import re


class DateTimeDir:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.entries = [entry for entry in os.scandir(self.dir_name) if entry.is_file()]

    @staticmethod
    def _to_dict(entry):
        return dict(name=entry.name, size=entry.stat().st_size, mtime=entry.stat().st_mtime)

    def get_list(self, filter=""):
        if filter == "":  # Pas de filtre, on liste les jours s'il y en a plus d'un
            days = set(entry.name[3:11] for entry in self.entries)
            if len(days) > 1:
                return dict(type="day", list=sorted(days, key=str))
            else:
                filter = days[0]
        if filter and len(filter) == 8:  # Filtre sur un jour donné, on liste les heures s'il y en a plus d'une
            hours = set(entry.name[3:13] for entry in self.entries if re.match(r"\d\d-" + filter, entry.name))
            if len(hours) > 1:
                return dict(type="hour", list=sorted(hours, key=str))
            else:
                filter = hours[0]
        if filter and len(filter) == 10:  # Liste les fichiers sur une heure donnée d'un jour donné
            filenames = sorted(self.entries, key=lambda e: e.name)
            filenames = [self._to_dict(entry) for entry in filenames if re.match(r"\d\d-" + filter, entry.name)]
            return dict(type="filename", list=filenames)

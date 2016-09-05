import argparse
import os
import re


VIDEO_FILE_EXTS = {'mkv', 'mp4', 'avi', 'flv', 'mpg', 'mpeg', 'wmv', 'webm', 'vob', 'mov', '3gp', 'ogv'}
SUBTITLE_FILE_EXTS = {'srt', 'sub', 'sbv', 'ttxt', 'usf', 'smi'}


class SerieFormater(object):

    SERIE_FILENAME_TEMPLATE = "{serie_name} S{season:02d}E{episode:02d} {episode_name}.{ext}"

    def __init__(self, regexp, serie_name=None, season=None):
        self.regexp = regexp
        self.serie_name = serie_name
        self.season = season

    def format_name(self, old_filename):
        m = self.regexp.match(old_filename)
        if m is None:
            raise ValueError("Unmatched file: {}".format(old_filename))

        episode_number = int(m.group("episode"))
        episode_name = m.group("episode_name")
        file_extension = m.group("ext")
        if self.serie_name is None:
            try:
                self.serie_name = m.group("serie_name")
            except IndexError:
                raise ValueError("Serie name not found")

        if self.season is None:
            try:
                self.season = m.group("season")
            except IndexError:
                raise ValueError("Season number not found")
        new_filename = self.SERIE_FILENAME_TEMPLATE.format(serie_name=self.serie_name,
                                                           season=self.season,
                                                           episode=episode_number,
                                                           episode_name=episode_name,
                                                           ext=file_extension)
        return new_filename


def rename_files(season_folder, regexp, serie_name, season):
    formater = SerieFormater(regexp, serie_name=serie_name, season=season)
    for f in os.listdir(season_folder):
        try:
            new_name = formater.format_name(f)
        except ValueError as e:
            print(e)
        else:
            os.rename(os.path.join(season_folder, f), os.path.join(season_folder, new_name))


def is_video_file(file_name):
    return any(file_name.endswith(ext) for ext in VIDEO_FILE_EXTS)


if __name__ == "__main__":
    got_regexp = re.compile("^Episode\s(?P<episode>\d{1,2})\s\-\s(?P<episode_name>[\w\s',]+)\.(?P<ext>\w+)$")

    parser = argparse.ArgumentParser(description='Rename series files')
    parser.add_argument('--folder', '-f', dest='folder', help='season folder')
    parser.add_argument('--season', '-s', dest='season', type=int, help='season number')
    parser.add_argument('--name', '-n', dest='name', help='serie name')
    args = parser.parse_args()
    rename_files(season_folder=args.folder, regexp=got_regexp, season=args.season, serie_name=args.name)

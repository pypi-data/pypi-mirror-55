import glob
import itertools
import os
from distutils.util import strtobool

import colorama


class SubrenameException(Exception):
    pass


class Subrename:
    sub_extensions = ['srt']
    video_extensions = ['mkv', 'mp4']

    def __init__(self):
        self.run()

    def run(self):
        videos = self._get_video_filenames()
        subs = self._get_sub_filenames()

        if not videos:
            raise SubrenameException("No video files found in this directory.")

        if not subs:
            raise SubrenameException("No subtitles files found in this directory.")

        if len(videos) != len(subs):
            raise SubrenameException(
                f"Found different number of videos ({len(videos)}) and subs ({len(subs)})"
            )

        sub_extension = subs[0].split('.')[-1]

        videos.sort()
        subs.sort()

        new_subs = [
            '.'.join(filename.split('.')[:-1]) + f'.{sub_extension}'
            for filename in videos
        ]

        for sub, new_sub in zip(subs, new_subs):
            self._print_diff(sub, new_sub)

        answer = input("Rename? (Y/n)")
        if answer == '' or strtobool(answer):
            self._rename_files(subs, new_subs)
            print("Done!")

    def _get_video_filenames(self):
        return self._get_filenames_for_extensions(self.video_extensions)

    def _get_sub_filenames(self):
        return self._get_filenames_for_extensions(self.sub_extensions)

    @staticmethod
    def _get_filenames_for_extensions(extensions):
        candidates = [glob.glob(f'./*.{ext}') for ext in extensions]
        candidates.sort(key=lambda c: len(c), reverse=True)
        return next(iter(candidates), [])

    @staticmethod
    def _rename_files(source, dest):
        for s, d in zip(source, dest):
            os.rename(s, d)

    @staticmethod
    def _print_diff(old, new):
        def longest_common_substring(a, b):
            n = len(a)
            m = len(b)

            memo = [[0] * m for _ in range(n)]
            max_ = (0, None)

            def memo_get(i, j):
                return 0 if i < 0 or j < 0 else memo[i][j]

            for i, j in itertools.product(range(n), range(m)):
                if a[i] == b[j]:
                    memo[i][j] = memo_get(i-1, j-1) + 1
                    if max_[0] < memo[i][j]:
                        max_ = (memo[i][j], (i+1, j+1))

            length, pos = max_

            if pos is not None:
                i, j = pos
                return range(i - length, i), range(j - length, j)

            return range(0, 0), range(0, 0)

        old_digits = [(i, c) for i, c in enumerate(old) if c.isdigit()]
        new_digits = [(i, c) for i, c in enumerate(new) if c.isdigit()]

        old_digits_str = ''.join(i[1] for i in old_digits)
        new_digits_str = ''.join(i[1] for i in new_digits)

        if old_digits_str == new_digits_str:
            old_range = range(0, len(old_digits))
            new_range = range(0, len(new_digits))
            special = colorama.Style.BRIGHT + colorama.Fore.GREEN
        else:
            old_range, new_range = longest_common_substring(old_digits_str, new_digits_str)
            special = colorama.Style.BRIGHT + colorama.Fore.BLUE

        old_pos = {x[0] for i, x in enumerate(old_digits) if i in old_range}
        new_pos = {x[0] for i, x in enumerate(new_digits) if i in new_range}

        Subrename._print_name(old, old_pos, special=special)
        print(' --> ', end='')
        Subrename._print_name(new, new_pos, special=special, end='\n')

    @staticmethod
    def _print_name(string, range_,
                    default=colorama.Style.BRIGHT + colorama.Fore.RED,
                    special=colorama.Style.BRIGHT + colorama.Fore.GREEN,
                    reset=colorama.Style.RESET_ALL,
                    end=''):
        def print_(item):
            print(item, end='')

        for i, c in enumerate(string):
            if not c.isdigit():
                print_(reset)
            elif i in range_:
                print_(special)
            else:
                print_(default)
            print_(c)

        print_(reset)
        print('', end=end)

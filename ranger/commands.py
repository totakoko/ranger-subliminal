# -*- coding: utf-8 -*-

from ranger.api.commands import *
from ranger.core.loader import CommandLoader

class sub(Command):
    """:sub [lang=en] [lang2], ...]

    Fetch the subtitles of specific languages for files in the Selection.

    If no argument is given, the language is english.

    "Selection" is defined as all the "marked files" (by default, you
    can mark files with space or v). If there are no marked files,
    use the "current file" (where the cursor is)
    """

    allow_abbrev = False

    def execute(self):
        import os

        cwd = self.fm.thisdir
        cf = self.fm.thisfile
        if not cwd or not cf:
            self.fm.notify("Error: no file selected !", bad=True)
            return
        
        original_path = cwd.path
        files = self.fm.thistab.get_selection()
        languages = self.args[:1]
        if not languages:
            languages = ['en']

        commandLine = ['subliminal', '-l']
        commandLine += languages
        commandLine += ['--']
        commandLine += [f.basename for f in files]
        descr = "Downloading {} subtitle(s)...".format(len(files))

        obj = CommandLoader(args=commandLine , descr=descr)

        def refresh(_):
            cwd = self.fm.env.get_directory(original_path)
            cwd.load_content()
            self.fm.notify("Downloaded {} subtitle(s)".format(len(files)))

        obj.signal_bind('after', refresh)

        self.fm.loader.add(obj) 


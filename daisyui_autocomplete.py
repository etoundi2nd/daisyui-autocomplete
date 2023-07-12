import sublime_plugin
import sublime

from .lib.daisyui_classes import DAISYUI_CLASSES

class remixiconAutocomplete(sublime_plugin.EventListener):
    def __init__(self):

        self.class_completions = [("%s \tDaisyUI" % s, s) for s in DAISYUI_CLASSES]

    def on_query_completions(self, view, prefix, locations):
        jsSources = ["source.js string.quoted", "source.jsx string.quoted", "source.ts string.quoted", "source.tsx string.quoted"]

        matchHTMLString = view.match_selector(locations[0], "text.html string.quoted")
        matchJSString = next(filter(lambda source: view.match_selector(locations[0], source), jsSources), None)

        if matchHTMLString or matchJSString:

            # Cursor is inside a quoted attribute
            # Now check if we are inside the class attribute

            # max search size
            LIMIT  = 250

            # place search cursor one word back
            cursor = locations[0] - len(prefix) - 1

            # dont start with negative value
            start  = max(0, cursor - LIMIT - len(prefix))

            # get part of buffer
            line   = view.substr(sublime.Region(start, cursor))

            # split attributes
            parts  = line.split('=')

            # is the last typed attribute a class attribute?
            if matchHTMLString:
              if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return self.class_completions
            if matchJSString:
              if len(parts) > 1 and parts[-2].strip().endswith("className"):
                return self.class_completions
            if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return self.class_completions

            return []

        else:

            return []

import argparse
import copy

__all__ = ['ParagraphedDescriptionHelpFormatter', 'ParagraphedArgumentDefaultsHelpFormatter']


class ParagraphedDescriptionHelpFormatter(argparse.HelpFormatter):
    @staticmethod
    def _is_iterable(obj):
        return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, frozenset)

    def _format_text(self, text):
        if self._is_iterable(text):
            paragraphs = []
            for paragraph in text:
                paragraphs.append(super()._format_text(paragraph)[0:-2])
            return "\n".join(paragraphs) + "\n\n"
        else:
            return super()._format_text(text)

    def _split_lines(self, text, width):
        if self._is_iterable(text):
            paragraphs = []
            for paragraph in text:
                paragraphs.extend(super()._split_lines(paragraph, width))
            return paragraphs
        else:
            return super()._split_lines(text, width)

    def _expand_help(self, action):
        if self._is_iterable(action.help):
            action_copy = copy.deepcopy(action)
            paragraphs = []
            for paragraph in action.help:
                action_copy.help = paragraph
                paragraphs.append(super()._expand_help(action_copy))
            return paragraphs
        else:
            return super()._expand_help(action)


class ParagraphedArgumentDefaultsHelpFormatter(ParagraphedDescriptionHelpFormatter):
    suppress_none_defaults = True

    def _get_defaults_string(self, action):
        if action.default is not argparse.SUPPRESS and (self.suppress_none_defaults is False or action.default is not None):
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                return "(default: %(default)s)"
        return None

    def _expand_help(self, action):
        default_string = self._get_defaults_string(action)
        if default_string is not None:
            if self._is_iterable(action.help):
                has_default = False
                paragraphs = []
                for paragraph in action.help:
                    paragraphs.append(paragraph)
                    if '%(default)' in paragraph:
                        has_default = True
                if not has_default:
                    action_copy = copy.deepcopy(action)
                    action_copy.help = paragraphs + [default_string]
                    return super()._expand_help(action_copy)
            else:
                action_copy = copy.deepcopy(action)
                action_copy.help += " " + default_string
                return super()._expand_help(action_copy)
        return super()._expand_help(action)


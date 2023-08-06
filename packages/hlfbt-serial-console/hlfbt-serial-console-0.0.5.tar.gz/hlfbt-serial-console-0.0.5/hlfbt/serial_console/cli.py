from typing import *
from .console import Console
from .console.matching import PromptMatcher, MatcherType
from ._argparse import formatter
import argparse
import codecs
import sys
import re


def escaped_str(_str, enc=sys.getdefaultencoding()):
    return codecs.escape_decode(_str.encode(enc))[0].decode(enc)


def get_args():
    parser = argparse.ArgumentParser(
        description='Simple Console Reader is a small utility to send commands to a console over a'
                    'serial connection. It will continue to read until a prompt is detected, or it'
                    'times out (only if a timeout is specified).',
        epilog=['Since most prompts end with a special character (f.i. \'$\', \'#\', \'>\', etc.),'
                'a regular expression for the prompt may put the expression matching this '
                'character (or character group) inside a (non-) capturing group at the end of'
                'the full regular expression. This group will be detected and used to match'
                'first against a given output on the serial connection to speed up prompt'
                'matching.',
                'SCR supports normal capture groups \'(...)\', non-capture groups \'(?:...)\','
                'flag setting groups \'(?[aiLmsux]*-[imsx]+:...)\', and named groups'
                '\'(?P<[^>]+>...)\'. Beware that flag only groups \'(?[aiLmsux]+)\' will be'
                'interpreted as normal capture groups. Putting them at the end of the'
                'pattern will thus break the prompt matching.',
                'Example:',
                'The regular expression \'^[^#$]*(?:[#$]) $\' would start matching everything'
                'until it finds a \'#\' or \'$\' right at the end of a line. SCR will make use of'
                'the \'(?:[#$])\' group and match for \'[#$] $\' first (keeping any extra whitespace'
                'or \\s after it), which will drop any non-matches much faster ([#$] is rather'
                'uncommon compared to [^#$]).'],
        formatter_class=formatter.ParagraphedArgumentDefaultsHelpFormatter
    )
    if parser.prog == '__main__.py':
        parser.prog = 'python3 -m ' + __package__
    parser.add_argument('-d', '--device', default='/dev/ttyS0', help='a serial device')
    parser.add_argument('-b', '--baud', type=int, default=9600, help='the baudrate of the serial device')
    parser.add_argument('-e', '--encoding', default='ascii', help='the encoding to communicate with')
    parser.add_argument('-t', '--timeout', type=float, default=None, help='a timeout to terminate after if no prompt could be detected')
    parser.add_argument('-m', '--map', type=escaped_str, metavar=('CONSOLE', 'LOCAL'), action='append', nargs=2,
                        help=['two sequences which should be mapped during communication from/to the serial device.',
                              'May be specified multiple times.',
                              'Escape sequences will be replaced (i.e. \\n becomes a literal newline).',
                              'LOCAL may be an empty string.'])
    parser.add_argument('-u', '--unbuffered', action='store_true', help='')
    parser.add_argument('-g', '--get-prompt', action='store_true', help='print the parsed prompt after each command execution,'
                                                                        'separated by an End Of Transmission (\\x04) character')
    parser.add_argument('commands', type=escaped_str, metavar='CMD', nargs='+', help='one or multiple commands to send to the console')
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument('-r', '--regex-prompt', metavar='REGEXP', help='a regular expression matching the prompt')
    prompt_group.add_argument('-s', '--substr-prompt', metavar='SUBSTR', help='a substring matching the prompt')
    prompt_group.add_argument('-p', '--prompt', help='a string matching the prompt')

    return parser.parse_args()


def get_console_args(args: argparse.Namespace):
    pattern = args.prompt
    pattern_type = MatcherType.EXACT
    if args.regex_prompt is not None:
        pattern_type = MatcherType.ANCHORED_REGEXP
        pattern = args.regex_prompt
    if args.substr_prompt is not None:
        pattern_type = MatcherType.SUBSTRING
        pattern = args.substr_prompt

    return [PromptMatcher(pattern, matcher_type=pattern_type)]


def get_console_kwargs(args: argparse.Namespace):
    kwargs = {
        'mappings': args.map,
        'encoding': args.encoding,
        'unbuffered': args.unbuffered
    }

    if args.timeout is not None:
        kwargs['timeout'] = args.timeout

    return kwargs


def get_console_open_args(args: argparse.Namespace):
    return [args.device, args.baud]


def print_prompt(prompt: Union[str, Type[re.Match]]):
    if isinstance(prompt, re.Match):
        def p(k, v): print('{}\t{}'.format(k, '' if v is None else v))
        p(0, prompt.group(0))
        for i, grp in enumerate(prompt.groups(), 1):
            p(i, grp)
        for key, grp in prompt.groupdict():
            p(key, grp)
    else:
        print(prompt)


def main():
    status = 0
    args = get_args()
    cli = Console(*get_console_args(args), strip_cmd=True, output_io=sys.stdout, **get_console_kwargs(args))
    cli.open(*get_console_open_args(args))
    for cmd in args.commands:
        try:
            cli.send(cmd)
            if args.get_prompt:
                print('\4')
                print_prompt(cli.prompt)
        except TimeoutError:
            status = 1
            print('\x1b[31mCommand timed out:\x1b[0m \'{}\''.format(cmd.strip()), file=sys.stderr)
            print('\x1b[31mBuffer:\x1b[0m', file=sys.stderr)
            print(cli.buffer, file=sys.stderr)

    sys.exit(status)

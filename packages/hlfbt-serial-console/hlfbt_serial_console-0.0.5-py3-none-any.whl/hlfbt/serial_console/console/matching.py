from typing import *
from enum import Enum
import re

__all__ = []

RE_END_ANCHOR = re.compile(
    r'''
    (?:
        \(  # Group parentheses
            (?:  # Non-capturing, lookahead, named or flagged group specifiers
                \?
                (?:
                    [:=]
                |
                    P<[^>]+>
                |
                    (?: [aiLmsux]*(?: -[imsx]+\: ) )
                )
            )?
            (  # Actual group contents
                (?:  # Any non-escaped character class that may include parentheses or escaped character class brackets
                    (?<! \\ )
                    \[
                    (?: \\\] | [^\]] )*
                    (?<! \\ )\]
                |  # .. Or anything other than parentheses, character class brackets or escaped closing parentheses
                    (?: [^[\]()] | \\\) )*
                )*
            )
        \)
        (  # Spacing patterns between group and end of full expression
            (?:
                (?:  # Any spacing characters or the spacing character class
                    \\s | \s
                )
                (?:  # .. Possibly quantified or optional
                    [+*?]{1,2} | \{[0-9]*,?[0-9]*\}\??
                )?
            )*
            \$?
        )
        $
    )
    ''',
    re.VERBOSE
)


class MatcherType(Enum):
    EXACT = 1
    SUBSTRING = 2
    REGEXP = 3
    ANCHORED_REGEXP = 4


class PromptMatcher(object):
    pattern: Union[str, Tuple[str, str]] = None
    matcher_type: MatcherType = None

    def __init__(self, pattern: str, matcher_type: MatcherType = MatcherType.ANCHORED_REGEXP) -> None:
        self.pattern = pattern
        self.matcher_type = matcher_type
        getattr(self, '__init_' + matcher_type.name.lower() + '__')()
        setattr(self, 'matches', getattr(self, '_matches_' + self.matcher_type.name.lower()))

    def __init_exact__(self) -> None:
        pass

    def __init_substring__(self) -> None:
        pass

    def __init_regexp__(self) -> None:
        self.pattern = re.compile(self.pattern)

    def __init_anchored_regexp__(self) -> None:
        end_anchor = RE_END_ANCHOR.search(self.pattern)
        if end_anchor:
            end_anchor = end_anchor.group(1) + end_anchor.group(2)
            end_anchor += '' if end_anchor.endswith('$') else '$'
            self.pattern = (re.compile(self.pattern), re.compile(end_anchor))
        else:
            self.matcher_type = MatcherType.REGEXP
            self.__init_regexp__()

    def _matches_exact(self, test) -> bool:
        return test == self.pattern

    def _matches_substring(self, test) -> str:
        if self.pattern in test:
            return test

    def _matches_regexp(self, test) -> Type[re.Match]:
        return self.pattern.search(test)

    def _matches_anchored_regexp(self, test) -> Type[re.Match]:
        if self.pattern[1].search(test):
            return self.pattern[0].search(test)


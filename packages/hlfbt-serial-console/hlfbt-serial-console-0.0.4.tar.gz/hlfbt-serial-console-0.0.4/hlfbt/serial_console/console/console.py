from typing import *
from .io import ConsoleIO, SerialConsoleIO
from .matching import PromptMatcher, MatcherType
import io
import os
import time

__all__ = ['Console']


class Mapping(object):
    _from = None
    _from_str = None
    _from_len = 0
    _to = None
    _to_str = None
    _to_len = 0

    def __init__(self, map_from, map_to):
        self._from = list(map_from)
        self._from_str = map_from
        self._from_len = len(map_from)
        self._to = list(map_to)
        self._to_str = map_to
        self._to_len = len(map_to)

    def encode(self, text: str) -> str:
        return text.replace(self._to_str, self._from_str)

    def decode(self, text: str) -> str:
        return text.replace(self._from_str, self._to_str)

    def map_end(self, buffer: List[str], offset: int = 0) -> None:
        s = -self._from_len
        if offset > 0:
            s -= offset
            offset = -offset
        else:
            offset = None
        if buffer[s:offset] == self._from:
            buffer[s:offset] = self._to

    def map_all(self, buffer: List[str]) -> None:
        for i in range(len(buffer) - self._from_len):
            self.map_end(buffer, offset=i)

    def unmap_end(self, buffer: List[str], offset: int = 0) -> None:
        s = -self._to_len
        if offset > 0:
            s -= offset
            offset = -offset
        else:
            offset = None
        if buffer[s:offset] == self._to:
            buffer[s:offset] = self._from

    def unmap_all(self, buffer: List[str]) -> None:
        for i in range(len(buffer) - self._to_len):
            self.unmap_end(buffer, offset=i)


class Console(object):
    matcher: Type[PromptMatcher] = None
    mappings: List[Type[Mapping]] = []
    encoding: str = 'utf-8'
    linesep: str = list(os.linesep)
    unbuffered: bool = False
    timeout: float = -1
    strip_cmd: bool = True
    console_io: Type[ConsoleIO] = SerialConsoleIO
    output_io: Type[io.IOBase] = None

    command = None
    buffer = None
    prompt = None

    def __init__(self, pattern: Union[str, Type[PromptMatcher]],
                 pattern_type: MatcherType = MatcherType.ANCHORED_REGEXP,
                 mappings: List[Tuple[str, str]] = None,
                 encoding: str = encoding,
                 linesep: str = linesep,
                 unbuffered: bool = unbuffered,
                 timeout: float = timeout,
                 strip_cmd: bool = strip_cmd,
                 console_io_class: ClassVar[ConsoleIO] = console_io,
                 output_io: Type[io.IOBase] = output_io):
        if isinstance(pattern, PromptMatcher):
            self.matcher = pattern
        else:
            self.matcher = PromptMatcher(pattern=pattern, matcher_type=pattern_type)
        if mappings is not None:
            for mapping in mappings:
                self.mappings.append(Mapping(*mapping))
        self.encoding = encoding
        self.linesep = list(linesep)
        self.unbuffered = unbuffered
        self.timeout = timeout
        self.strip_cmd = strip_cmd
        self.console_io_class = console_io_class
        self.output_io = output_io

    def open(self, *args, **kwargs):
        io_class = self.console_io_class
        if 'io_class' in kwargs:
            io_class = kwargs['io_class']
            del kwargs['io_class']
        self.console_io = io_class(*args, **kwargs)
        self.console_io.open()

    def close(self):
        if self.console_io is not None:
            self.console_io.close()

    def send(self, command: Union[str, bytes], await_prompt: bool = True, **kwargs):
        if isinstance(command, str):
            for mapping in self.mappings:
                command = mapping.encode(command)
            self.command = command.rstrip()
            command = command.encode(self.encoding)
        self.console_io.write(command)
        if await_prompt:
            return self.await_prompt(**kwargs)

    def await_prompt(self,
                     matcher: Type[PromptMatcher] = None,
                     encoding: str = None,
                     unbuffered: bool = None,
                     timeout: float = None,
                     strip_cmd: bool = None,
                     output_io: Type[io.IOBase] = None) -> Union[None, str]:
        """
        Read from the console until the prompt is encountered.
        If `timeout` is non-negative, a TimeoutError will be raised if no new bytes have been received in `timeout` seconds.
        Returns the output buffer as a str by default if no arguments are provided.
        If `out_io` is set, then nothing is returned.
        Only writes to the output buffer once a linefeed is encountered (identified by `linesep`), unless `unbuffered`
        is True, in which case every character is written.
        Character mappings are not applied to the output IO in unbuffered mode, but are applied before matching for the prompt.
        The fully mapped output buffer is still available in the `buffer` class property.
        The `prompt` class property will be set to the matched prompt on successful matching.

        :param matcher: optional call override
        :param encoding: optional call override
        :param unbuffered: optional call override
        :param timeout: optional call override
        :param strip_cmd: optional call override
        :param output_io: optional call override
        :return: returns the output buffer as a str when `output_io` is None, otherwise None
        :raises TimeoutError: when `timeout` is non-negative and has been reached while waiting for the prompt
        """
        matcher = self.matcher if matcher is None else matcher
        encoding = self.encoding if encoding is None else encoding
        unbuffered = self.unbuffered if unbuffered is None else unbuffered
        timeout = self.timeout if timeout is None else timeout
        strip_cmd = self.strip_cmd if strip_cmd is None else strip_cmd
        output_io = self.output_io if output_io is None else output_io

        self.buffer = ""
        line_buffer = []
        line_count = 0
        prev_available = 0
        last_received_at = time.time()
        return_str = False
        lf_len = len(self.linesep)
        if output_io is None:
            return_str = True
            output_io = io.StringIO()

        while True:
            available = self.console_io.available()
            if available > 0:
                if available >= prev_available and timeout >= 0:
                    last_received_at = time.time()
                prev_available = available
                c = self.console_io.read(1).decode(encoding)
                line_buffer.append(c)
                if unbuffered:
                    output_io.write(c)
                for mapping in self.mappings:
                    mapping.map_end(line_buffer)
                match = matcher.matches(''.join(line_buffer))
                if match:
                    self.prompt = match
                    break
                if line_buffer[-lf_len:] == self.linesep:
                    line_count += 1
                    line_buffer = ''.join(line_buffer)
                    if not strip_cmd or line_count > 1 or line_buffer.strip() != self.command:
                        if not unbuffered:
                            output_io.write(line_buffer)
                        self.buffer += line_buffer
                    line_buffer = []
            else:
                if timeout >= 0 and (last_received_at + timeout) <= time.time():
                    raise TimeoutError("Timed out while waiting for prompt")
                time.sleep(0.005)

        if return_str:
            return output_io.getvalue()


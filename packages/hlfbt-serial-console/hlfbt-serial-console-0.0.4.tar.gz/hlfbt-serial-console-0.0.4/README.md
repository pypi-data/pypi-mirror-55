# serial_console

![PyPI](https://img.shields.io/pypi/v/hlfbt-serial-console)

Serial console is a small utility / library that makes it easier to interface with consoles that use a prompt-like interface.  
Instead of simply waiting until the connection times out, `serial_console` tries to continuously match for a prompt.  

```shell script
# With a simple sh shell present on /dev/ttyS0, 9600 baudrate:
$ serial_console -p '$ ' 'echo hello world!'

hello world!
```

### Prompt matching

`serial_console` reads byte for byte from the output buffer and tries to match for every new character it receives.  
It separates lines based on the OS's default line separator, and only matches on the current line, since prompts normally don't span multiple lines.  
Matching can be done on equality, substring, or regular expression matching.  
Prompts matched for equality must match the whole line. Substring matching simply looks for the existence of the prompt in the line.  
Regular expressions are also available, but may need some extra care to be made efficient.  

##### Regular Expressions

Take the following regular expression, matching most Cisco iOS console prompts:
```pythonregexp
^([a-z][a-z0-9.-]{0,61}[a-z0-9]|[a-z])(\([a-z0-9 ._-][a-z0-9 ._-]*\))?([>#])$
```
Executed on every single new character this is a very costly expression.  
To try and speed this up, `serial_console` will look for an "end anchor group" in the regexp.  
Most prompts will end in non-alphanumeric characters that may not be commonly found in regular output, like `$`, `#`, or `?`.  
If the regexp contains a group at its end, this group will be matched first before trying to match the whole expression. This will drop most non-matching lines quickly without having to try all iterations from the start of the regexp.  
So with the above example expression, `serial_console` would detect `([>#])$` as the "end anchor" and try to match for `[>#]$` first.  
The regexp may also contain any amount of spacing characters between the group and the end of the expression, and the group may also be a non-matching group or named group:  
```pythonregexp
(?P<endanchor>[#$>?)]) ?\s*$
# results in the following end anchor regexp:
[#$>?)] ?\s*$
```

### Serial communication

Serial communication is done with the help of the [pyserial][pypi-pyserial] package and is thus mostly OS independent.  
It is also possible to specify console encoding, character mappings (f.i. to map '\r\n' to '\n') and the line seperator (although not with `serial_console` cli tool).  

##### Note on character mapping

The `-m` cli argument makes it possible to easily specify one or multiple mappings.  
All mappings are applied in the order they have been supplied, but they are applied on the whole last read line on every new character.  
So with the following example:
```shell script
serial_console -m '\r\n' '\n' -m '\r' '\n' ...
```
Even if the `'\r\n' '\n'` rule is defined first, the `'\r' '\n'` rule would match first for a line like `foo output\r\n`, and result in a mapped string `foo output\n\n`.

### Compatibility with other consoles

While `serial_console` was mainly intended for use with "dumb" serial connections, it may just as well also be used with any console or interface that has the typical Pythonic IO API.  

An "interface" base class is available in `serial_console.io.ConsoleIO`.  
To use a custom `ConsoleIO` class, simply specify it as the `console_io_class` named parameter when instantiating a `Console` object.  
Calling `Console::open` will pass all `*args` and `**kwargs` straight through to the constructor of the `console_io_class`.  
```python
import serial_console

class MyCustomConsoleIO(serial_console.io.ConsoleIO):
    def __init__(self, foo_argument, bar_parameter=None):
        ...

console = serial_console.console.Console('(?:[#$]) $', console_io_class=MyCustomConsoleIO)
console.open('foo_argument', bar_parameter=123)
```


### Dependencies

 - **Python 3.5**: Required for `typing` type hinting. Python v3+ may also be used together with the [typing][pypi-typing] package.
 - **[pyserial][pypi-pyserial]**: Required for serial communication.


[pypi-pyserial]: https://pypi.org/project/pyserial/
[pypi-typing]: https://pypi.org/project/typing/

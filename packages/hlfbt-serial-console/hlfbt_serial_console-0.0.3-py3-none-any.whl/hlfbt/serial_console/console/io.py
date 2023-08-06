import serial

__all__ = []


class ConsoleIO(object):

    def open(self, *args, **kwargs):
        """
        Prepare and open the connection.
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % self.__class__.__name__)

    def close(self):
        """
        Terminate and close the connection.
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % self.__class__.__name__)

    def read(self, num: int = 1) -> bytes:
        """
        Read `num` number of bytes from the read buffer.

        :param num: the number of bytes to read
        :return: the retrieved bytes
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % self.__class__.__name__)

    def write(self, buffer: bytes) -> None:
        """
        Write `buffer` to the write buffer.

        :param buffer: the bytes to write
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % self.__class__.__name__)

    def flush(self) -> None:
        """
        Flush all remaining bytes from the write buffer.
        Wait until all data is written.
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % self.__class__.__name__)

    def available(self):
        """
        Get the number of bytes available in the read buffer.

        :return: the number of available bytes
        """
        NotImplementedError("Class %s doesn't implement aMethod()" % self.__class__.__name__)


class SerialConsoleIO(serial.Serial, ConsoleIO):

    def available(self):
        return self.in_waiting

    def open(self):
        if self.is_open:
            return
        return super().open()


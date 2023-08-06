from typing import (
    List,
    Optional,
    Tuple,
)
from typing_extensions import (
    Final,
)

from .constants import (
    Command,
    Constant,
    Register,
)
from .utility import (
    toByteArrayWithLength,
    toInt,
)


class SpiStub:
    def xfer2(self, data: List[int]) -> List[int]:
        pass


class StSpinDevice:
    """Class providing access to a single SPIN device"""

    def __init__(
            self, position: int, busy_pin: int,
            total_devices: int, spi: SpiStub,
            chip_select_pin: Optional[int] = None):
        """
        :position: Position in chain, where 0 is the last device in chain
        :chip_select_pin: Chip select pin,
        if different from hardware SPI CS pin
        :busy_pin: Pin to read busy status from
        :total_devices: Total number of devices in chain
        :spi: SPI object used for serial communication
        """
        self._position: Final           = position
        self._chip_select_pin: Final    = chip_select_pin
        self._busy_pin: Final           = busy_pin
        self._total_devices: Final      = total_devices
        self._spi: Final                = spi

    def _write(self, data: int) -> int:
        """Write a single byte to the device.

        :data: A single byte representing a command or value
        :return: Returns response byte
        """
        assert(data >= 0)
        assert(data <= 0xFF)

        buffer = [0] * self._total_devices
        buffer[self._position] = data

        # TODO: CS LOW
        response = self._spi.xfer2(buffer)
        # TODO: CS HIGH

        return response[self._position]

    def _writeMultiple(self, data: List[int]) -> List[int]:
        """Write each byte in list to device
        Used to combine calls to _write

        :data: List of single byte values to send
        :return: List of response bytes
        """
        response = []

        for data_byte in data:
            response.append(self._write(data_byte))

        return response

    def _writeCommand(
            self, command: int,
            payload: Optional[int] = None,
            payload_size: Optional[int] = None) -> None:
        """Write command to device with payload (if any)

        :command: Command to write
        :payload: Payload (if any)
        :payload_size: Payload size in bytes

        """
        self._write(command)

        if payload is None:
            return

        self._writeMultiple(toByteArrayWithLength(payload, payload_size))

    def setRegister(self, register: int, value: int) -> None:
        """Set the specified register to the given value
        :register: The register location
        :value: Value register should be set to
        """
        RegisterSize = Register.getSize(register)
        set_command = Command.ParamSet | register

        self._writeCommand(set_command, value, RegisterSize)

    def getRegister(self, register: int) -> int:
        """Fetches a register's contents and returns the current value

        :register: Register location to be accessed
        :returns: Value of specified register

        """
        RegisterSize = Register.getSize(register)
        self._writeCommand(Command.ParamGet | register)

        response = self._writeMultiple([Command.Nop] * RegisterSize)
        return toInt(response)

    def move(self, direction: int, steps: int) -> None:
        """Move motor in specified direction for n steps

        :direction: Motor direction
        :steps: Number of (micro)steps to take

        """
        assert(direction >= 0)
        assert(direction < Constant.DirMax)
        assert(steps >= 0)
        assert(steps <= Constant.MaxSteps)

        PayloadSize = Command.getPayloadSize(Command.Move)

        self._writeCommand(Command.Move | direction, steps, PayloadSize)

    def run(self, steps_per_second: float, direction: int) -> None:
        """Run the motor at the given steps per second, in the
        given direction

        :steps_per_second: Steps per second up to 15625.
        0.015 step/s resolution
        :direction: Direction as declared in constant

        """
        assert(direction >= 0)
        assert(direction < Constant.DirMax)
        assert(steps_per_second >= 0)
        assert(steps_per_second <= Constant.MaxStepsPerSecond)

        speed = int(steps_per_second * Constant.SpsToSpeed)
        PayloadSize = Command.getPayloadSize(Command.Run)

        self._writeCommand(Command.Run | direction, speed, PayloadSize)

    def hiZHard(self) -> None:
        """Stop motors abruptly, release holding current

        """
        self._writeCommand(Command.HiZHard)

    def hiZSoft(self) -> None:
        """Stop motors, release holding current

        """
        self._writeCommand(Command.HiZSoft)

    def stopHard(self) -> None:
        """Stop motors abruptly, maintain holding current

        """
        self._writeCommand(Command.StopHard)

    def stopSoft(self) -> None:
        """Stop motors, maintain holding current

        """
        self._writeCommand(Command.StopSoft)

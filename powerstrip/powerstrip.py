import serial

from enum import Enum
from typing import List



class Polarity(Enum):
    POSITIVE = 'VPOS'
    NEGATIVE = 'VNEG'
    OFF = 'OFF'



class Powerstrip:

    def __init__(self, port='/dev/ttyUSB0') -> None:
        self.serial = serial.Serial(port, baudrate=115200, timeout=1)

    def _send_command(self, cmd: str) -> None:
        """Sends a command to the power strip and returns the response.
        
        Returns:
            str: The response from the power strip.
        """
        self.serial.write((cmd + "\n").encode('utf-8'))
        return self.serial.readline().decode('utf-8').strip()


    def ping(self) -> bool:
        """Ping the equipment.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command('AT') == 'OK'

    def set_echo(self, state: bool) -> bool:
        """Enable (state=True) or disable (state=False) the echo of the sent command.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"ATE={int(state)}") == 'OK'

    def get_echo(self) -> bool:
        """Get the state of the echo.
        
        Returns:
            bool: True if echo is enabled, False otherwise.
        """
        return self._send_command("ATE?") == '1'

    def reset(self) -> bool:
        """Reset all outputs.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command("ATR") == 'OK'

    def get_firmware_version(self) -> str:
        """Get the firmware version.
        
        Returns:
            str: The firmware version in the format "MAJOR_VER.MINOR_VER".
        """
        return self._send_command("ATVER?")


    def set_all_ac(self, state: bool) -> str:
        """Activate (state=True) or deactivate (state=False) all AC outputs.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"ATAC={int(state)}") == 'OK'

    def get_all_ac(self) -> List[bool]:
        """Get the state of the AC outputs.
        
        Returns:
            List[bool]: A list of booleans representing the state of each AC output.
        """
        response = self._send_command("ATAC?")
        return [bool(int(bit)) for bit in bin(int(response, 16))[2:]]

    def set_ac(self, x: int, state: bool) -> str:
        """Activate (state=True) or deactivate (state=False) the AC output (x).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"ATAC{x}={int(state)}") == 'OK'


    def set_all_3v(self, state: bool) -> bool:
        """Activate (state=True) or deactivate (state=False) all 3V outputs.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"AT3V={int(state)}") == 'OK'

    def get_all_3v(self) -> List[bool]:
        """Get the state of the 3V outputs.
        
        Returns:
            List[bool]: A list of booleans representing the state of each 3V output.
        """
        response = self._send_command("AT3V?")
        return [bool(int(bit)) for bit in bin(int(response, 16))[2:]]

    def set_3v(self, x: int, state: bool) -> bool:
        """Activate (state=True) or deactivate (state=False) the 3V output (x).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"AT3V{x}={int(state)}") == 'OK'


    def set_all_5v(self, state: bool) -> bool:
        """Activate (state=True) or deactivate (state=False) all 5V outputs.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"AT5V={int(state)}") == 'OK'

    def get_all_5v(self) -> List[bool]:
        """Get the state of the 5V outputs.
        
        Returns:
            List[bool]: A list of booleans representing the state of each 5V output.
        """
        response = self._send_command("AT5V?")
        return [bool(int(bit)) for bit in bin(int(response, 16))[2:]]   


    def set_5v_polarity(self, polarity: Polarity) -> bool:
        """Set the polarity of the 5V output.
        
        Args:
            polarity (Polarity): The desired polarity. Use Polarity.POSITIVE for positive, 
                                 Polarity.NEGATIVE for negative, and Polarity.OFF to deactivate.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._send_command(f"ATVPOL={polarity.value}") == 'OK'

    def get_5v_polarity(self) -> Polarity:
        """Get the polarity of the 5V output.
        
        Returns:
            Polarity: The current polarity. Polarity.POSITIVE for positive, 
                      Polarity.NEGATIVE for negative, and Polarity.OFF if deactivated.
        """
        response = self._send_command("ATVPOL?")
        return Polarity(response)
    

    def set_variable(self, n: float) -> str:
        """Activate (2.0 ≤ n ≤ 5.0) or deactivate (n=0.0) the variable output.
        
        Returns:
            str: "OK" if successful, "ERROR" otherwise.
        """
        return self._send_command(f"ATVAR={n}")

    def get_variable(self) -> str:
        """Get the state of the variable output.
        
        Returns:
            str: "V" corresponding to the value, in floating, of the output.
        """
        return self._send_command("ATVAR?")


    def set_variable(self, n: float) -> bool:
        """Activate (2.0 ≤ n ≤ 5.0) or deactivate (n=0.0) the variable output.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if n != 0.0 and (n < 2.0 or n > 5.0):
            raise ValueError("n must be 0.0 or between 2.0 and 5.0")
        return self._send_command(f"ATVAR={n}") == 'OK'

    def get_variable(self) -> float:
        """Get the state of the variable output.
        
        Returns:
            float: The value of the output.
        """
        response = self._send_command("ATVAR?")
        return float(response[1:]) if response.startswith('V') else 0.0

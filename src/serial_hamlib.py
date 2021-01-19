import serial

class SerialHamlib:
    def __init__(self, port: str) -> None:
        self._ser = serial.Serial(port, timeout=0.5)

    def write_cmd(self, cmd) -> None:
       # TODO add error handling an try catch
        self._ser.write(cmd)

    def read_answer7(self) -> str:
        xx = self._ser.read(7)
        return xx

    def read_answer(self) -> str:
        xx = self._ser.read(16)
        print(xx)

    def get_audio_gain(self) -> int:
        self._ser.write(b'ZZAG;')
        xx = self._ser.read(8)
        gain = int(xx[4:7], base=10)
        return gain

    def set_audio_gain(self, ag: int ) -> None:
        self._ser.write(('ZZAG%03d;' % ag).encode('utf-8'))

    def get_band(self) -> int:
        self._ser.write(b'ZZBS;')
        xx = self._ser.read(8)
        band = int(xx[4:7], base=10)
        return band

    def set_band(self, band: int) -> None:
        self._ser.write(('ZZBS%03d;' % band).encode('utf-8'))

    def get_mox_status(self) -> int:
        self._ser.write(b'ZZTX;')
        xx = self._ser.read(6)
        mox = int(xx[4:5], base=10)
        return mox

    def set_mox_status(self, mox: int) -> None:
        if mox == 0:
            self._ser.write(b'ZZTX0;')
        else:
            self._ser.write(b'ZZTX1;')

    def get_stepsize(self) -> int:
        self._ser.write(b'ZZAC;')
        xx = self._ser.read(7)
        step = int(xx[4:6], base=10)
        return step

    def set_stepsize(self, step: int) -> None:
        self._ser.write(('ZZAC%02d;' % step).encode('utf-8'))

    def step_up(self) -> None:
        self._ser.write(b'ZZAU;')

    def step_down(self) -> None:
        self._ser.write(b'ZZAD;')

    def get_frequency(self) -> int:
        self._ser.write(b'ZZFA;')
        xx = self._ser.read(16)
        freq = int(xx[4:15], base=10)
        return freq

    def set_frequency(self, freq: int) -> None:
        self._ser.write(('ZZFA%011d;' % freq).encode('utf-8'))


import base64
import hmac
from datetime import datetime
from typing import Union
import unittest


class SignatureException(Exception):
    pass


class StaleResponseException(Exception):
    pass


class DoubleClickCrypto:
    @staticmethod
    def decrypt(enc: Union[str, bytes], e_key: Union[str, bytes], i_key: Union[str, bytes],
                max_timedelta_seconds: int = None) -> int:

        #  Decode keys if they are passed as strings
        if type(e_key) is str:
            e_key = base64.urlsafe_b64decode(e_key)
        if type(i_key) is str:
            i_key = base64.urlsafe_b64decode(i_key)

        #  Decode message if passed as string
        if type(enc) is str:
            #  Fix base64 padding
            if len(enc) % 4:
                enc += "=" * (4 - len(enc) % 4)

            enc = base64.urlsafe_b64decode(enc)

        #  Split message parts
        iv = enc[0:16]
        p = enc[16:24]
        sig = enc[24:28]

        #  Decrypt price
        price_pad = hmac.new(e_key, iv, "sha1").digest()
        price_bytes = bytes(a ^ b for a, b in zip(p, price_pad))
        price = int.from_bytes(price_bytes, "big")

        #  Decrypt confirmation signature and check
        conf_sig = hmac.new(i_key, price_bytes + iv, "sha1").digest()[0:4]
        if conf_sig != sig:
            raise SignatureException("Decryption failed signature check")

        #  Check timestamp if max_timedelta_seconds is provided
        if max_timedelta_seconds is not None:
            sec = int.from_bytes(iv[0:4], "big", signed=False)
            usec = int.from_bytes(iv[4:8], "big", signed=False)
            timestamp = datetime.fromtimestamp(sec + usec / 1000)
            timedelta = datetime.now() - timestamp
            if abs(timedelta.total_seconds()) > max_timedelta_seconds:
                raise StaleResponseException("Time delta is too large")

        return price


class DecryptionTest(unittest.TestCase):
    e_key = base64.urlsafe_b64decode('skU7Ax_NL5pPAFyKdkfZjZz2-VhIN8bjj1rVFOaJ_5o=')
    i_key = base64.urlsafe_b64decode('arO23ykdNqUQ5LEoQ0FVmPkBd7xB5CO89PDZlSjpFxo=')
    enc = ["YWJjMTIzZGVmNDU2Z2hpN7fhCuPemCce_6msaw", "YWJjMTIzZGVmNDU2Z2hpN7fhCuPemCAWJRxOgA",
           "YWJjMTIzZGVmNDU2Z2hpN7fhCuPemC32prpWWw"]

    def test_decryption(self):
        self.assertEqual(DoubleClickCrypto.decrypt(self.enc[0], self.e_key, self.i_key), 100)
        self.assertEqual(DoubleClickCrypto.decrypt(self.enc[1], self.e_key, self.i_key), 1900)
        self.assertEqual(DoubleClickCrypto.decrypt(self.enc[2], self.e_key, self.i_key), 2700)

    def test_timedelta(self):
        with self.assertRaises(StaleResponseException):
            DoubleClickCrypto.decrypt(self.enc[0], self.e_key, self.i_key, 0)

    def test_invalid(self):
        with self.assertRaises(SignatureException):
            DoubleClickCrypto.decrypt("", self.e_key, self.i_key, 0)


if __name__ == '__main__':
    unittest.main()

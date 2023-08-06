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
    def _decode_base64(s: Union[str, bytes]):
        """
        Decodes a base64 encoded string with or without padding. Bytes will pass through unchanged.
        :param s: The string or bytes
        :return: The decoded bytes
        """
        if type(s) is str:
            if len(s) % 4:
                s += "=" * (4 - len(s) % 4)

            return base64.urlsafe_b64decode(s)
        elif type(s) is bytes:
            return s
        else:
            raise TypeError

    @staticmethod
    def _decrypt(cipher: bytes, iv_len: int, payload_len: int, e_key: bytes, i_key: bytes) -> (bytes, bytes):
        """
        Decrypts a doubleclick encrypted cipher with the given parameters.
        :return: The plain bytes and initialization vector
        """
        iv = cipher[0:iv_len]
        p = cipher[iv_len:iv_len + payload_len]
        sig = cipher[iv_len + payload_len:iv_len + payload_len + 4]

        #  Decrypt cipher
        pad = hmac.new(e_key, iv, "sha1").digest()
        plain_bytes = bytes(a ^ b for a, b in zip(p, pad))

        #  Decrypt confirmation signature and check
        conf_sig = hmac.new(i_key, plain_bytes + iv, "sha1").digest()[0:4]
        if conf_sig != sig:
            raise SignatureException("Decryption failed signature check")

        return plain_bytes, iv

    @staticmethod
    def decrypt_price(cipher: Union[str, bytes], e_key: Union[str, bytes], i_key: Union[str, bytes],
                      max_timedelta_seconds: int = None) -> int:
        """
        Decrypts the price from a doubleclick cipher.
        https://developers.google.com/authorized-buyers/rtb/response-guide/decrypt-price
        :param cipher: The cipher as a base64 encoded string or bytes
        :param e_key: Encryption key as base64 encoded string or bytes
        :param i_key: Integrity key as base64 encoded string or bytes
        :param max_timedelta_seconds: The maximum allowable difference between the timestamp and the current time in
        seconds before a StaleResponseException is raised. Defaults to None, i.e. disabled.
        :return: The price
        """
        #  Decode inputs
        cipher = DoubleClickCrypto._decode_base64(cipher)
        e_key = DoubleClickCrypto._decode_base64(e_key)
        i_key = DoubleClickCrypto._decode_base64(i_key)

        price, iv = DoubleClickCrypto._decrypt(cipher, 16, 8, e_key, i_key)
        price = int.from_bytes(price, "big")

        #  Check timestamp if max_timedelta_seconds is provided
        if max_timedelta_seconds is not None:
            sec = int.from_bytes(iv[0:4], "big", signed=False)
            usec = int.from_bytes(iv[4:8], "big", signed=False)
            timestamp = datetime.fromtimestamp(sec + usec / 1_000_000)
            timedelta = datetime.now() - timestamp
            if abs(timedelta.total_seconds()) > max_timedelta_seconds:
                raise StaleResponseException("Time delta is too large")

        return price

    @staticmethod
    def decrypt_ad_id(cipher: Union[str, bytes], e_key: Union[str, bytes], i_key: Union[str, bytes]) -> bytes:
        """
        Decrypts the advertising id bytes from a doubleclick cipher.
        https://developers.google.com/authorized-buyers/rtb/response-guide/decrypt-advertising-id
        :param cipher: The cipher as a base64 encoded string or bytes
        :param e_key: Encryption key as base64 encoded string or bytes
        :param i_key: Integrity key as base64 encoded string or bytes
        :return: The advertising id bytes
        """
        #  Decode inputs
        cipher = DoubleClickCrypto._decode_base64(cipher)
        e_key = DoubleClickCrypto._decode_base64(e_key)
        i_key = DoubleClickCrypto._decode_base64(i_key)

        ad_id, _ = DoubleClickCrypto._decrypt(cipher, 16, 16, e_key, i_key)

        return ad_id


class DecryptionTest(unittest.TestCase):
    price_e_key = [base64.urlsafe_b64decode("skU7Ax_NL5pPAFyKdkfZjZz2-VhIN8bjj1rVFOaJ_5o="),
                   "skU7Ax_NL5pPAFyKdkfZjZz2-VhIN8bjj1rVFOaJ_5o="]
    price_i_key = [base64.urlsafe_b64decode("arO23ykdNqUQ5LEoQ0FVmPkBd7xB5CO89PDZlSjpFxo="),
                   "arO23ykdNqUQ5LEoQ0FVmPkBd7xB5CO89PDZlSjpFxo="]
    price_cipher = ["YWJjMTIzZGVmNDU2Z2hpN7fhCuPemCce_6msaw", "YWJjMTIzZGVmNDU2Z2hpN7fhCuPemCAWJRxOgA",
                    "YWJjMTIzZGVmNDU2Z2hpN7fhCuPemC32prpWWw"]

    ad_id_e_key = "sIxwz7yw62yrfoLGt12lIHKuYrK_S5kLuApI2BQe7Ac="
    ad_id_i_key = "v3fsVcMBMMHYzRhi7SpM0sdqwzvAxM6KPTu9OtVod5I="
    ad_id_cipher_base64 = "5nmwvgAM0UABI0VniavN72_tyXf-QJOmQdL0tmh_fduB2go_"
    ad_id_cipher = bytes([
        0xE6, 0x79, 0xB0, 0xBE,
        0x00, 0x0C, 0xD1, 0x40,
        0x01, 0x23, 0x45, 0x67,
        0x89, 0xAB, 0xCD, 0xEF,
        0x6F, 0xED, 0xC9, 0x77,
        0xFE, 0x40, 0x93, 0xA6,
        0x41, 0xD2, 0xF4, 0xB6,
        0x68, 0x7F, 0x7D, 0xDB,
        0x81, 0xDA, 0x0A, 0x3F,
    ])
    ad_id_plain = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

    def test_price_decryption(self):
        self.assertEqual(
            DoubleClickCrypto.decrypt_price(self.price_cipher[0], self.price_e_key[0], self.price_i_key[0]), 100)
        self.assertEqual(
            DoubleClickCrypto.decrypt_price(self.price_cipher[1], self.price_e_key[1], self.price_i_key[0]), 1900)
        self.assertEqual(
            DoubleClickCrypto.decrypt_price(self.price_cipher[2], self.price_e_key[0], self.price_i_key[1]), 2700)
        self.assertEqual(
            DoubleClickCrypto.decrypt_price(self.price_cipher[0], self.price_e_key[1], self.price_i_key[1]), 100)

    def test_ad_decryption(self):
        self.assertEqual(DoubleClickCrypto.decrypt_ad_id(self.ad_id_cipher, self.ad_id_e_key, self.ad_id_i_key),
                         self.ad_id_plain)
        self.assertEqual(DoubleClickCrypto.decrypt_ad_id(self.ad_id_cipher_base64, self.ad_id_e_key, self.ad_id_i_key),
                         self.ad_id_plain)

    def test_timedelta(self):
        with self.assertRaises(StaleResponseException):
            DoubleClickCrypto.decrypt_price(self.price_cipher[0], self.price_e_key[0], self.price_i_key[0], 0)

    def test_invalid(self):
        with self.assertRaises(SignatureException):
            DoubleClickCrypto.decrypt_price("", self.price_e_key[0], self.price_i_key[0], 0)
        with self.assertRaises(SignatureException):
            DoubleClickCrypto.decrypt_ad_id(self.ad_id_cipher, "", self.ad_id_i_key)


if __name__ == '__main__':
    unittest.main()

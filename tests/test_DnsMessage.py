from unittest import TestCase

from main import DnsMessage

import struct


class TestPackFlags(TestCase):
    def test(self):
        qr = 0x0
        opcode = DnsMessage.OPCODE_QUERY
        aa = 0
        tc = 1
        rd = 0
        ra = 1
        rcode = DnsMessage.RCODE_NO_ERROR

        expected = (0b0 << 15) | (DnsMessage.OPCODE_QUERY << 11) | (0b0101000 << 4) | DnsMessage.RCODE_NO_ERROR

        flags = DnsMessage.pack_flags(qr, opcode, aa, tc, rd, ra, rcode)
        self.assertEquals(expected, flags, "Expected %s but found %s" % (bin(expected), bin(flags)))


class TestUnpackFlags(TestCase):
    def test(self):
        expected = (0b1, 0b0101, 0b0, 0b1, 0b0, 0b1, 0b1111)
        flags = DnsMessage.unpack_flags(0b1010101010001111)
        self.assertEquals(expected, flags)


class TestCreateAndUnpackFlags(TestCase):
    def test(self):
        qr = 0x0
        opcode = DnsMessage.OPCODE_QUERY
        aa = 0
        tc = 1
        rd = 0
        ra = 1
        rcode = DnsMessage.RCODE_FORMAT_ERROR

        expected = (qr, opcode, aa, tc, rd, ra, rcode)

        self.assertEquals(expected, DnsMessage.unpack_flags(DnsMessage.pack_flags(qr, opcode, aa, tc, rd, ra, rcode)))


class TestPackDnsMessage(TestCase):
    def test(self):
        message = DnsMessage(1234, 1, DnsMessage.OPCODE_NOTIFY, 0, 0, 0, 0, DnsMessage.RCODE_FORMAT_ERROR, 3, 4, 5, 6)
        packed = message.pack()
        identifier = 0b0000010011010010
        flags = 0b1010000000000001
        question_count = 0b0000000000000011
        answer_count = 0b0000000000000100
        nameserver_count = 0b0000000000000101
        authority_count = 0b0000000000000110
        expected = struct.pack("!LLLLLL", identifier, flags, question_count, answer_count, nameserver_count,
                               authority_count)

        self.assertEquals(expected, packed);

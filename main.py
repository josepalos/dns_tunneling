import struct


class DnsMessage:
    OPCODE_QUERY = 0
    OPCODE_IQUERY = 1
    OPCODE_STATUS = 2
    OPCODE_RESERVED = 3
    OPCODE_NOTIFY = 4
    OPCODE_UPDATE = 5

    RCODE_NO_ERROR = 0
    RCODE_FORMAT_ERROR = 1
    RCODE_SERVER_FAILURE = 2
    RCODE_NAME_ERROR = 3
    RCODE_NOT_IMPLEMENTED = 4
    RCODE_REFUSED = 5
    RCODE_YX_DOMAIN = 6
    RCODE_YX_RR_SET = 7
    RCODE_NX_RR_SET = 8
    RCODE_NOT_AUTH = 9
    RCODE_NOT_ZONE = 10

    def __init__(self, dns_id, qr, opcode, aa, tc, rd, ra, rcode, qdcount, ancount, nscount, arcount):
        self.dns_id = dns_id  # Identifier. Generated by the device that does the query, copied by the server.
        self.qr = qr  # 1 bit [ 0 -> query, 1 -> response ]
        self.opcode = opcode
        # opcode = [0 -> query, 1 -> iquery (obsolete), 2 -> status, 3 -> reserved, 4 -> Notify, 5 -> Update ]
        self.aa = aa  # 1 if server is authoritative for the zone in the question.
        self.tc = tc  # 1 -> message truncated
        self.rd = rd  # 1 -> Ask the server (if supported) to answer the query recursively. Not changed in the response
        self.ra = ra  # 1 -> The server support recursive queries.
        # zero field (3 bits set to 0) ignored. Should be added when creating binary data.
        self.rcode = rcode
        # rcode = [ 0 -> No error, 1 -> Format error, 2 -> Server failure, 3 -> Name error, 4 -> Not implemented,
        #           5 -> Refused, 6 -> XY domain, 7 -> XY RR Set, 8 -> NX RR Set, 9 -> Not Auth, 10 -> NotZone ]
        self.qdcount = qdcount  # Number of questions in the Question section.
        self.ancount = ancount  # Number of resource records in the Answer section.
        self.nscount = nscount  # Number of resource records in the Authority section. (NS is name server)
        self.arcount = arcount  # Number of resource records in the Additional section.

    def pack(self):
        flags = DnsMessage.create_flags(self.qr, self.opcode, self.aa, self.tc, self.rd, self.ra, self.rcode)
        return struct.pack("!HHHHHH", self.dns_id, flags, self.qdcount, self.ancount, self.nscount, self.arcount)

    @staticmethod
    def unpack(data):
        (dns_id, flags, qdcount, ancount, nscount, arcount) = struct.unpack("!HHHHHH", data)
        (qr, opcode, aa, tc, rd, ra, rcode) = DnsMessage.unpack_flags(flags)
        return DnsMessage(dns_id, qr, opcode, aa, tc, rd, ra, rcode, qdcount, ancount, nscount, arcount)

    @staticmethod
    def unpack_flags(flags):
        qr = (flags >> 15) & 0b1
        opcode = (flags >> 11) & 0b1111
        aa = (flags >> 10) & 0b1
        tc = (flags >> 9) & 0b1
        rd = (flags >> 8) & 0b1
        ra = (flags >> 7) & 0b1
        rcode = flags & 0b1111

        return (qr, opcode, aa, tc, rd, ra, rcode)

    @staticmethod
    def create_flags(qr, opcode, aa, tc, rd, ra, rcode):
        return (qr << 15) | (opcode << 11) | (aa << 10) | (tc << 9) | (rd << 8) | (ra << 7) | (0b000 << 4) | rcode


class DnsService:
    def __init__(self):
        pass

    def run(self):
        pass


def start_service():
    return DnsService()


def main():
    dns_service = start_service()
    dns_service.run()

if __name__ == "__main__":
    main()

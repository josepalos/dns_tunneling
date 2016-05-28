import struct

class DnsMessage:
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
        flags = (self.qr << 15) | (self.opcode << 11) | (self.aa << 10) | (self.tc << 9) | (self.rd << 8) |\
                (self.ra << 7) | (0b000 << 4) | self.rcode

        return struct.pack("!HHHHHH", self.dns_id, flags, self.qdcount, self.ancount, self.nscount, self.arcount)


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

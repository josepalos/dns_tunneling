import struct
import socket


def print_hex(string):
    print ':'.join(x.encode('hex') for x in string)


def parse_qname(data):
    data.strip('\0')
    labels = []
    while data is not "":
        size = ord(data[0])
        labels.append(data[1:size + 1])
        data = data[size + 1:]


    return labels


qtype_names = {
    1: "A",
    2: "NS",
    5: "CNAME",
    6: "SOA",
    11: "WKS",
    12: "PTR",
    15: "MX",
    33: "SRV",
    28: "AAAA",
    255: "--ANY--",
}

qclass_names = {
    1: "IN",
}



class DnsMessageHeader:
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
        flags = DnsMessageHeader.pack_flags(self.qr, self.opcode, self.aa, self.tc, self.rd, self.ra, self.rcode)
        return struct.pack("!LLLLLL", self.dns_id, flags, self.qdcount, self.ancount, self.nscount, self.arcount)

    @staticmethod
    def unpack(data):
        (dns_id, flags, qdcount, ancount, nscount, arcount) = struct.unpack("!HHHHHH", data)
        (qr, opcode, aa, tc, rd, ra, rcode) = DnsMessageHeader.unpack_flags(flags)
        return DnsMessageHeader(dns_id, qr, opcode, aa, tc, rd, ra, rcode, qdcount, ancount, nscount, arcount)

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
    def pack_flags(qr, opcode, aa, tc, rd, ra, rcode):
        return (qr << 15) | (opcode << 11) | (aa << 10) | (tc << 9) | (rd << 8) | (ra << 7) | (0b000 << 4) | rcode


class DnsMessage:
    def __init__(self, headers, questions, answers, authority, additional):
        self.headers = headers
        self.questions = questions
        self.answers = answers
        self.authority = authority
        self.additional = additional

    def isQuery(self):
        return self.headers.qr == 0

    def pack(self):
        pass

    @staticmethod
    def unpack(data):
        raw_headers = data[:12]
        data = data[12:]
        headers = DnsMessageHeader.unpack(raw_headers)

        questions = []
        for i in range(0, headers.qdcount):
            # each question is from 0 to first ocurrence of NULL-character plus 32 bits.
            size = data.index('\x00') + 4 + 1  # Add one because index starts with 0.
            raw_question = data[:size]
            data = data[size:]
            questions.append(Question.unpack(raw_question))

        return DnsMessage(headers, questions, [], [], [])

class Question:
    def __init__(self, qname, qtype, qclass):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    @staticmethod
    def unpack(data):
        splited_data = data.split('\x00')
        raw_qname = splited_data[0]
        data = data[len(raw_qname) + 1:]
        qtype = sum([ord(i) for i in data[:2]])
        data = data[2:]
        qclass = sum([ord(i) for i in data])

        return Question(parse_qname(raw_qname), qtype, qclass)

    def pack_qname(self):
        raw = ""
        for label in self.qname:
            raw += chr(len(label)) + label
        raw += '\x00'
        return raw


    def pack(self):
        return self.pack_qname() + unichr(self.qtype) + unichr(self.qclass)


class DnsService:
    def __init__(self):
        self.names = {}
        self.reverse_names = {}

    def run(self):
        pass
        while True:
            data = self.read_data()
            self.process_query(self.parse_query(data))

    def read_data(self):
        pass

    def parse_query(self, data):
        pass

    def process_query(self, query):
        questions = query.questions
        for q in questions:
            # TODO: ----from here----
            print "Asked for '%s' (type: '%s') named '%s'" % \
                (query.qtype, query.qclass, query.qname)

    def register_entry(self, name, ip):
        self.names[name] = ip
        self.reverse_names[ip] = name

    def get_ip(self, name):
        return self.names.get(name)

    def get_reverse(self, ip):
        return self.reverse_names.get(ip)


def start_service():
    # TODO load config and data from files...
    return DnsService()


def main():
    dns_service = start_service()
    dns_service.run()

if __name__ == "__main__":
    main()

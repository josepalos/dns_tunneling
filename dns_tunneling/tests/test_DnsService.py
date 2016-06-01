import unittest

from dns_tunneling.main import DnsService


class RegisterANameAddsTheNameAndTheReverse(unittest.TestCase):
    def test(self):
        service = DnsService()
        service.register_entry("www.test.com", "1.2.3.4")
        self.assertEquals("1.2.3.4", service.get_ip("www.test.com"))
        self.assertEquals("www.test.com", service.get_reverse("1.2.3.4"))


class WhenSearchForAnInexistingEntryReturnsNone(unittest.TestCase):
    def test(self):
        service = DnsService()
        self.assertEquals(None, service.get_ip("www.no_exists.com"))
        self.assertEquals(None, service.get_reverse("-1.-1.-1.-1"))
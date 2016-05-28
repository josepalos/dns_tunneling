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

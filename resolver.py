import dns.name
import dns.message
import dns.rdatatype
import dns.rdataclass
import dns.query
from dns.message import MessageSection


def resolve(domain, name_server):
    qname = dns.name.from_text(domain)
    q = dns.message.make_query(qname, dns.rdatatype.A)

    while True:
        r = dns.query.udp(q, name_server)
        if len(r.sections[MessageSection.ANSWER]):
            return str(r.sections[MessageSection.ANSWER][0][0])
        elif len(r.sections[MessageSection.ADDITIONAL]):
            for rr in r.sections[MessageSection.ADDITIONAL]:
                if rr.rdtype == dns.rdatatype.A:
                    name_server = str(rr[0])
                    print(f'Route to next nameserver, {rr.name} {rr[0]}')
                    break
        else:
            print(f'Resolve nameserver, {r.sections[MessageSection.AUTHORITY][0][0]}')
            name_server = resolve(str(r.sections[MessageSection.AUTHORITY][0][0]), name_server)

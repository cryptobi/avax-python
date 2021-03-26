import json

from OpenSSL import crypto
from datetime import datetime

def bytes_to_string(bytes):
    return str(bytes, 'utf-8')

def x509_name_to_json(x509_name):
    json = { }

    for key, value in x509_name.get_components():
        json.update({ bytes_to_string(key): bytes_to_string(value) })

    return json

def x509_extensions_to_json(x509_cert):
    json = { }
    for ext_index in range(0, x509_cert.get_extension_count(), 1):
        extension = x509_cert.get_extension(ext_index)
        json.update({ bytes_to_string(extension.get_short_name()): str(extension) })

    return json

class x509Parser:

    def x509_to_str(x509_cert):
        cert_str = x509Parser.parse_x509(x509_cert)

        return json.dumps(cert_str, indent=4)

    def parse_x509(cert,ignore_extensions=False):
        x509_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

        cert = {
                "subject": x509_name_to_json(x509_cert.get_subject()),
                "issuer": x509_name_to_json(x509_cert.get_issuer()),
                "has-expired": x509_cert.has_expired(),
                "not-after": str(datetime.strptime(bytes_to_string(x509_cert.get_notAfter()), '%Y%m%d%H%M%SZ')),
                "not-before": str(datetime.strptime(bytes_to_string(x509_cert.get_notBefore()), '%Y%m%d%H%M%SZ')),
                "serial-number": x509_cert.get_serial_number(),
                "serial-number(hex)": hex(x509_cert.get_serial_number()),
                "signature-algorithm": bytes_to_string(x509_cert.get_signature_algorithm()),
                "version": x509_cert.get_version(),
                "pulic-key-length": x509_cert.get_pubkey().bits()
            }

        if (not ignore_extensions):
            cert.update({"extensions": x509_extensions_to_json(x509_cert)})

        return cert
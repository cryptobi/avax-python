#!/usr/bin/python

import sys, getopt
import ssl
import socket
import json

from x509Parser import x509Parser

BEGIN_X509_CERT = "-----BEGIN CERTIFICATE-----"
END_X509_CERT = "-----END CERTIFICATE-----"

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:p:f:deo:v", ["help", "host=", "port=", "file=", "dump", "ignore-extensions", "ignore-cert-validation", "ouput"])
    except getopt.GetoptError as err:
        print(err)
        print_help()
        sys.exit(2)

    cert_list = None
    host = None
    port = None
    ignore_extensions = False
    ignore_cert_validation = False
    file_output = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-e", "ignore-extensions"):
            ignore_extensions = True
        elif opt in ("-i", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-f", "--file"):
            cert_list = parse_multi_certs(open(arg, 'r').read())
        elif opt in ("-d", "--dump"):
            cert_input = ""
            line = input("Enter X509 cert: ")
            
            while line:
                cert_input += line
                cert_input += "\n"
                line = input()

            cert_list = parse_multi_certs(cert_input)
        elif opt in ("-v", "--ignore-cert-validation"):
            ignore_cert_validation = True
        elif opt in ("-o", "--output"):
            file_output = arg
        else:
            print_help
            sys.exit(2)

    if (host and port):
        cert_list = [get_certificate(host, port, ignore_cert_validation=ignore_cert_validation)]
    elif (host):
        cert_list = [get_certificate(host, ignore_cert_validation=ignore_cert_validation)]

    x509_array = []
    for cert in cert_list:
        x509_array.append(x509Parser.parse_x509(cert, ignore_extensions))

    certs = { "certs": x509_array }

    if (file_output):
        print("Writing to file %s..." % file_output)
        
        output_file = open(file_output, 'w')
        output_file.write(json.dumps(certs, indent=4))
        output_file.close
        
        print("Completed!")
    else:
        print(json.dumps(certs, indent=4))

def print_help():
    print("x509_parser.py -i <host> -p <port> -f <input-file> -d -e")
    print("-h (--help) = print this help summary.")
    print("-i (--host) = host name of the web server to obtain certificate from.")
    print("-p (--port) = to be used in conjunction with the host option to specify the port number to connect to the server on, if none is supplied it defaults to 443.")
    print("-f (--file) = the filename of the file containing the X509 certificates.")
    print("-d (--dump) = past in a collection of X509 certificates.")
    print("-e (--ignore-extensions = do not include extensions in the parse output.")
    print("-v (--ignore-cert-validation = ignore certificate validation.")
    print("-o (--output) = filename to put the output into instead of the standard output.")

def get_certificate(host, port=443, timeout=10, ignore_cert_validation=False):
    context = ssl.create_default_context()

    if (ignore_cert_validation):
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    connection = socket.create_connection((host, port))
    sock = context.wrap_socket(connection, server_hostname=host)
    sock.settimeout(timeout)

    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()

    return ssl.DER_cert_to_PEM_cert(der_cert)

def parse_multi_certs(certs):
    cert_list = []
    begin_index = certs.find(BEGIN_X509_CERT)

    while (begin_index != -1):
        end_index = certs.find(END_X509_CERT, begin_index) + len(END_X509_CERT)
        cert_list.append(certs[begin_index:end_index])
        begin_index = certs.find(BEGIN_X509_CERT, end_index)

    return cert_list

if __name__ == "__main__":
    main(sys.argv[1:])
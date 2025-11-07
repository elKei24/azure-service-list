import argparse
import sys

from az_service_list.csv_exporter import write_csv
from az_service_list.services_provider import get_services


def main():
    parser = argparse.ArgumentParser(description="Writes a CSV file of Azure services with their categories")
    parser.add_argument("-o", "--outfile", required=True, help="Filename of the output CSV file",
                        type=argparse.FileType("w"), default=sys.stdout)
    args = parser.parse_args()

    services = get_services()
    write_csv(services, args.outfile)


if __name__ == "__main__":
    main()

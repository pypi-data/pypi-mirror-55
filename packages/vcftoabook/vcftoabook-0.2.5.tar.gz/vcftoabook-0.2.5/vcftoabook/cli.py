import argparse
import vcftoabook


def main():
    parser = argparse.ArgumentParser(
        prog="vcftoabook",
        description="Convert .vcf files into addressbook files to be used in "
                    "abook/Mutt"
    )

    parser.add_argument(
        '-i', '--input',
        metavar='input',
        type=str,
        help="the input path of a .vcf file",
        required=True
    )

    parser.add_argument(
        '-o', '--output',
        metavar="output",
        type=str,
        default='addressbook',
        help="the output path/filename (default: ./addressbook)"
    )

    args = parser.parse_args()

    vcftoabook.main(args)


main()

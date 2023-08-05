import argparse
import os
import subprocess
import sys
import time

from pathmodel.pathmodel_wrapper import pathmodel_analysis

def main():
    '''
    Arguments when used with entrypoint as: pathmodel -d data.lp
    '''
    parser = argparse.ArgumentParser(
        "pathmodel",
        description="Prototype of the metabolic pathway drift. For specific help on each subcommand use: pathmodel {cmd} --help",
    )
    # parent parser
    parent_parser_i = argparse.ArgumentParser(add_help=False)
    parent_parser_i.add_argument(
        "-i",
        "--input",
        metavar="INPUT_FILE",
        help="input file containing atoms, bonds, reactions and goal",
        required=True)
    parent_parser_o = argparse.ArgumentParser(add_help=False)
    parent_parser_o.add_argument(
        "-o",
        "--out",
        dest="output_folder",
        required=True,
        help="output directory path",
        metavar="OUPUT_DIR")

    # subparsers
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands:',
        dest="cmd")
    infer_parser = subparsers.add_parser(
        "infer",
        help="metabolic network reconstruction",
        parents=[
            parent_parser_i, parent_parser_o
        ],
        description=
        "Run PathModel on input data lp file"
        )
    test_parser = subparsers.add_parser(
        "test",
        help="metabolic network reconstruction",
        parents=[
            parent_parser_i, parent_parser_o
        ],
        description=
        "Test PathModel on the data from the article (sterol and MAA)"
        )

    parser_args = parser.parse_args()

    # Print help and exit if no arguments.
    argument_number = len(sys.argv[1:])
    if argument_number == 0:
        parser.print_help()
        parser.exit()

    input_file = parser_args.input
    output_folder = parser_args.output_folder

    if parser_args.cmd == 'test':
        package_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])+ '/data/'
        sterol_input_path = package_path + 'new_sterol.lp'
        maa_input_path = package_path + 'MAA_pwy.lp'
        sterol_out = output_folder + '/sterol'
        maa_out = output_folder + '/MAA'
        if not os.path.isdir(sterol_out):
            try:
                os.makedirs(sterol_out)
            except OSError:
                raise OSError('Can not create output folder')
        if not os.path.isdir(maa_out):
            try:
                os.makedirs(maa_out)
            except OSError:
                raise OSError('Can not create output folder')
        pathmodel_analysis(sterol_input_path, sterol_out)
        pathmodel_analysis(maa_input_path, maa_out)

        return

    pathmodel_analysis(input_file, output_folder)

if __name__ == "__main__":
    main()

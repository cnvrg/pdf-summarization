from extractor import extract
from summarizer import summarize
import os
import argparse
import json
import traceback

cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")


# argument parsing
def argument_parser():
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "--dir",
        action="store",
        dest="dir",
        required=True,
        help="""directory containing all pdf files""",
    )
    parser.add_argument(
        "--page_wise",
        action="store",
        dest="page_wise",
        default=False,
        required=False,
        type=bool,
        help="""Whether you want page wise summary of the pdfs""",
    )
    return parser.parse_args()


def validation(args):
    """
    check if the pdf directory provided is a valid path if not raise an exception

    Arguments
    - argument parser

    Raises
    - An assertion error if the path provided is not a valid directory
    """
    assert os.path.exists(args.dir), " Path to the pdfs provided does not exist "


def main():
    # command line execution
    args = argument_parser()
    direc = args.dir
    page_wise = args.page_wise

    # check if the path provided is a valid directory
    validation(args)
    allpdfs = []
    # traverse the directory to get list of all files that end with .pdf
    for pdfname in os.listdir(direc):
        if pdfname.endswith(".pdf"):
            allpdfs.append(pdfname)

    assert len(allpdfs) != 0, "There are no pdf files located in the given directory"

    for pdfname in allpdfs:
        try:
            files = os.path.join(direc, pdfname)
            print("extracting text from :", pdfname)
            text = extract(files)
        except Exception:
            print(
                "While extracting text from pdf: ",
                pdfname,
                " following error occurred",
            )
            print(traceback.format_exc())
            continue
        try:
            print("summarizing text from :", pdfname)
            summaries = summarize(text, page_wise)
        except Exception:
            print(
                "While summarizing text from pdf: ",
                pdfname,
                " following error occurred",
            )
            print(traceback.format_exc())
            continue
        try:
            print(cnvrg_workdir + "/" + pdfname[:-4] + ".json")
            with open(cnvrg_workdir + "/" + pdfname[:-4] + ".json", "w") as outfile:
                json.dump(summaries, outfile)
        except Exception:
            print(
                "While writing summary as output from pdf: ",
                pdfname,
                " following error occurred",
            )
            print(traceback.format_exc())
            continue


if __name__ == "__main__":
    main()

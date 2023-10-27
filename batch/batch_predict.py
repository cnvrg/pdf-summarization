from extractor import master_extractor
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
    if(page_wise=="true" or page_wise=="True"):
        page_wise = True
    else:
        page_wise = False
    
    # check if the path provided is a valid directory
    validation(args)
    allfiles = []
    # traverse the directory to get list of all files that end with .pdf
    for filename in os.listdir(direc):
        if filename.endswith(".pdf") or filename.endswith(".docx") or filename.endswith(".doc") or filename.endswith(".txt"):
            allfiles.append(filename)

    assert len(allfiles) != 0, "There are no valid files located in the given directory"
    finaljson = {}
    for filename in allfiles:
        try:
            files = os.path.join(direc, filename)
            print("extracting text from :", filename)
            text = master_extractor(files)
            if(text is None):
                continue
        except Exception:
            print(
                "While extracting text from pdf: ",
                filename,
                " following error occurred",
            )
            print(traceback.format_exc())
            continue
        try:
            print("summarizing text from :", filename)
            summaries = summarize(text, page_wise)
            finaljson[filename] = summaries
        except Exception:
            print(
                "While summarizing text from pdf: ",
                filename,
                " following error occurred",
            )
            print(traceback.format_exc())
            continue
    try:
        with open(cnvrg_workdir + "/" + "results.json", "w") as outfile:
            json.dump(finaljson, outfile)
    except Exception:
        print(
                "While writing summary as output following error occurred",
            )
        print(traceback.format_exc())


if __name__ == "__main__":
    main()

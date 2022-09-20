# PDF Text Summarization Batch

This blueprint can be used to extract text from pdfs in a given directory and summarize the text. The summaries can be created pagewise or for the entire pdf. Results are saved in json files, each json file will have the same name as that of the pdf file. For example: `test.pdf` will have a corresponding `test.json` in the output artifacts. We use a combination of ocr and pdf processing techniques to extract the text from pdfs in the most accurate way possible before summarizing it. The summaries are generated using `BigBird` model architecture capable of working with much longer text and much lesser computing.

## Features

- Provide the directory path to the batch library containing all pdf files you want to run the summarizer model on.
- You can choose to have your data in s3 bucket or create a cnvrg dataset. 

## Arguments

- `--dir` : Directory path containing all the pdf files that you want to process.
- `--page_wise` : A flag taking `True` or `False` as input. Set True if you want summaries created per page for each pdf. Set False if you want summaries created for the entire pdfs.

## How to run
```
cnvrg run  --datasets='[{id:"{dataset_id}",commit:"{dataset_commit_id}"}]' --machine="{compute_template}" --image={compute_image} --sync_before=false python3 batch_predict.py --page_wise {Flag} --dir {path_to_pdfs}
```

### Example command

```
cnvrg run  --datasets='[{id:"pdfs",commit:"af3e133428b9e25c55bc59fe534248e6a0c0f17b"}]' --machine="AWS-ON-DEMAND.xlarge-memory" --image=cnvrg/cnvrg:v5.0 --sync_before=false python3 batch_predict.py --page_wise False --dir /data/pdfs
```
  
## Example output:

### Summary for the entire pdf

```
{

0 :
    {
        "Summary for the entire pdf"
    }
}
```

### For pagewise summaries

```
{

0 :     {
    
            "Summary of page 1"
        }

1 :     {
            "Summary of page 2"
        }
}

```
# Reference
OCR model

```
@misc{doctr2021,
    title={docTR: Document Text Recognition},
    author={Mindee},
    year={2021},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/mindee/doctr}}
}
```

BigBird
```
@misc{zaheer2021big,
      title={Big Bird: Transformers for Longer Sequences}, 
      author={Manzil Zaheer and Guru Guruganesh and Avinava Dubey and Joshua Ainslie and Chris Alberti and Santiago Ontanon and Philip Pham and Anirudh Ravula and Qifan Wang and Li Yang and Amr Ahmed},
      year={2021},
      eprint={2007.14062},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```
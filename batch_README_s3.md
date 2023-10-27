Use this blueprint to extract and summarize the text from documents in a directory. The summaries can be created page-wise or for the entire document. The results are saved in a JSON file. The blueprint uses a combination of OCR and PDF processing techniques to extract document text as accurately as possible before summarizing it. The summaries are generated using BigBird model architecture capable of handling more text with less computing. The supported document types are .pdf, .doc, .docx, and .txt.

Complete the following steps to run the document-summarizer model in batch mode:
1. Click **Use Blueprint** button. The cnvrg Blueprint Flow page displays.
2. Click the **S3 Connector** task to display its dialog.
   - Within the **Parameters** tab, provide the following Key-Value information:
     - Key: `bucketname` − Value: provide the data bucket name
     - Key: `prefix` − Value: provide the main path to the documents folders
   - Click the **Advanced** tab to change resources to run the blueprint, as required.
3. Click the **Batch** task to display its dialog.
   - Within the **Parameters** tab, provide the following Key-Value pair information:
     - Key: `--dir` − Value: provide the S3 path to the folder storing the target document files in the following format: `/input/s3_connector/text_summarization_data/`
     - Key: `--page_wise` − Value: set as True or False for by-page or full-file PDF summaries, respectively

     NOTE: The `page_wise` flag functions only for PDF files.
     NOTE: You can use the prebuilt data example paths provided.

  - Click the **Advanced** tab to change resources to run the blueprint, as required.
4. Click the **Run** button. The cnvrg software deploys a document-summarizer model that summarizes text in a batch of files and outputs a JSON file with the document summaries.
5. Select **Batch > Experiments > Artifacts** and locate the output file.
6. Click the **results.json** File Name, click the Menu icon, and select **Open File** to view the output file.

A custom model that summarizes text in different document files has been deployed in batch mode. To learn how this blueprint was created, click [here](https://github.com/cnvrg/pdf-summarization).

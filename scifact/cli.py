import luigi
from scifact.tasks.download import ContentData, SavedModel, DownloadData, DownloadModel
from scifact.tasks.tasks import Preprocess_arxiv_data
from scifact.model.download_pdf import find_download_pdf, extract_ref_pdf
from scifact.model.apply_model import cosine_pipeline
import pandas as pd
import os


def main(args=None):
    # luigi.build([DownloadData(data='arxivData.json')], local_scheduler=True)
    luigi.build([DownloadModel(model='rationale_roberta_large_fever.zip')], local_scheduler=True)
    # luigi.build([DataToCSV()], local_scheduler=True)

    luigi.build([Preprocess_arxiv_data()], local_scheduler=True)


def find_cs(args=None):
    # download the cleaned arxiv dataset
    arxiv_data = pd.read_csv(
        "/Users/meenu/Desktop/Harvard/AdvancedPython/Assignments/Pset3/2021sp-scifact-lalitanjali-ai/scifact/data/dataset/preprocessed_arXivData.csv")
    print(arxiv_data.head)

    # Downloading pdf with the title"Hadamard"
    pdf_name = "Dual Recurrent Attention Units "

    pdf_data = find_download_pdf(pdf_name, arxiv_data)
    # print(data[:200])

    references = extract_ref_pdf(pdf_data)
    print(references[:50])
    #
    # # Query from original pdf
    # doc_query = 'Bilinear representations Fukui et al. [7] use compact bi-linear pooling to attend over the image features and com-bine it with the language representation.'
    #
    # top_matches = 2
    # # find_extracts_labels(doc_query,all_ref_text,top_matches)
    # cosine_pipeline(doc_query, references, top_matches, pdf_data)


def unzip():
    import zipfile

    path_to_zip_file = "/Users/meenu/Desktop/Harvard/AdvancedPython/Assignments/Pset3/2021sp-scifact-lalitanjali-ai/scifact/data/saved_models/rationale_roberta_large_fever.zip"
    os.chdir("data/saved_models")

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Done!')

    # model_roberta = torch.load("/content/datasets/rationale_roberta_large_fever/pytorch_model.bin")
    #
    # # load tokenizer
    # tokenizer = AutoTokenizer.from_pretrained("/content/datasets/rationale_roberta_large_fever/")
    # model = AutoModelForSequenceClassification.from_pretrained("/content/datasets/rationale_roberta_large_fever/").to(
    #     device).eval()

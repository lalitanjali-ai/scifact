import luigi
from scifact.tasks.download import ContentData, SavedModel, DownloadData, DownloadModel
from scifact.tasks.tasks import Preprocess_arxiv_data
from scifact.model.download_pdf import find_download_pdf, extract_ref_pdf
from scifact.model.pretrained_model import pretrained_model
from scifact.tasks.tasks import find_display_abstracts
import pandas as pd
import os


def main(args=None):
    #luigi.build([DownloadData(data='arxivData.json')], local_scheduler=True)
    #luigi.build([DownloadModel(model='rationale_roberta_large_fever.zip')], local_scheduler=True)
    #luigi.build([DownloadModel(model='label_roberta_large_fever_scifact.zip')], local_scheduler=True)
    #uigi.build([Preprocess_arxiv_data()], local_scheduler=True)
    luigi.build([find_display_abstracts()], local_scheduler=True)



# def find_cs(args=None):
#     # download the cleaned arxiv dataset
#     arxiv_data = pd.read_csv("/Users/meenu/Desktop/Harvard/AdvancedPython/Assignments/Pset3/2021sp-scifact-lalitanjali-ai/scifact/data/dataset/preprocessed_arXivData.csv")
#     #print(arxiv_data.head)
#
#     # Downloading pdf with the title"Hadamard"
#     pdf_name = "Dual Recurrent Attention Units "
#
#     pdf_data = find_download_pdf(pdf_name, arxiv_data)
#     # print(data[:200])
#
#     references = extract_ref_pdf(pdf_data)
#     #print(references[:50])
#
#     # Query from original pdf
#     doc_query = 'Bilinear representations Fukui et al. [7] use compact bi-linear pooling to attend over the image features and com-bine it with the language representation.'
#
#     top_matches = 2
#
#     pm=pretrained_model()
#     pm.printwd()
#     pm.cosine_pipeline(doc_query, references, top_matches, arxiv_data)
#     #cosine_pipeline(doc_query, references, top_matches, arxiv_data)

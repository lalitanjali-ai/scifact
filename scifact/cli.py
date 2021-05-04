import luigi
from scifact.tasks.download import ContentData,SavedModel,DownloadData,DownloadModel
from scifact.tasks.tasks import Preprocess_arxiv_data
from scifact.model.download_pdf import find_download
import pandas as pd

def main(args=None):
    #luigi.build([DownloadData(data='arxivData.json')], local_scheduler=True)
    #luigi.build([DownloadModel(model='rationale_roberta_large_fever.zip')], local_scheduler=True)
    #luigi.build([DataToCSV()], local_scheduler=True)

    luigi.build([Preprocess_arxiv_data()], local_scheduler=True)

def extract_ref_pdf(text):
    # Extract only the references section from the entire pdf
    # get only text after word 'References'
    pos = text.find('References')
    reference_text = text[pos + len('References '):]
    return reference_text

def find_cs(args=None):
    #download the cleaned arxiv dataset
    arxiv_data=pd.read_csv("/Users/meenu/Desktop/Harvard/AdvancedPython/Assignments/Pset3/2021sp-scifact-lalitanjali-ai/scifact/data/dataset/preprocessed_arXivData.csv")
    print(arxiv_data.head)

    # Query from original pdf
    doc_query = 'Since global features can hardly answer questions about certain local parts of the input, attention mechanisms have been extensively used in VQA recently [5, 6, 7, 8, 9, 10,11, 12].'

    #Downloading pdf with the title"Hadamard"
    pdf_name = "Hadamard Product for "

    data=find_download(pdf_name,arxiv_data)
    print(data[:200])

    # references2=extract_ref_pdf(data)
    # print(references2)






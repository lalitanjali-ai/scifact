import luigi
from scifact.tasks.download import ContentData,SavedModel,DownloadData,DownloadModel
from scifact.tasks.tasks import Preprocess_arxiv_data


def main(args=None):
    #luigi.build([DownloadData(data='arxivData.json')], local_scheduler=True)
    #luigi.build([DownloadModel(model='rationale_roberta_large_fever.zip')], local_scheduler=True)
    #luigi.build([DataToCSV()], local_scheduler=True)

    luigi.build([Preprocess_arxiv_data()], local_scheduler=True)


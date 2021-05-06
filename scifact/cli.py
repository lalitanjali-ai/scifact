import luigi
from scifact.tasks.download import ContentData, SavedModel, DownloadData, DownloadModel
from scifact.tasks.tasks import Preprocess_arxiv_data
from scifact.tasks.tasks import find_display_abstracts



def main(args=None):
    #luigi.build([DownloadData(data='arxivData.json')], local_scheduler=True)
    #luigi.build([DownloadModel(model='rationale_roberta_large_fever.zip')], local_scheduler=True)
    #luigi.build([DownloadModel(model='label_roberta_large_fever_scifact.zip')], local_scheduler=True)
    #luigi.build([Preprocess_arxiv_data()], local_scheduler=True)
    luigi.build([find_display_abstracts()], local_scheduler=True)



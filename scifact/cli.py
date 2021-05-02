import luigi
from scifact.tasks.download import ContentData,SavedModel,DownloadData,DownloadModel


def main(args=None):
    luigi.build([DownloadData(data='arxivData.json')], local_scheduler=True)
    luigi.build([DownloadModel(model='rationale_roberta_large_fever.zip')], local_scheduler=True)


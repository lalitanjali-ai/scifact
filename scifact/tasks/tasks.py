from scifact.tasks.download import DownloadData, DownloadModel
from environs import Env
import json
import dask.dataframe as dd
import luigi
from csci_utils.luigi.dask_target import CSVTarget
from scifact.tasks.arxiv_preprocess import arxiv_clean
import os
from luigi import Parameter, Task
import pandas as pd
from csci_utils.luigi.luigi_task import TargetOutput, Requirement, Requires
from scifact.model.download_pdf import find_download_pdf, extract_ref_pdf
from scifact.model.pretrained_model import rationale_label_selection

env = Env()
env.read_env()


class Preprocess_arxiv_data(Task):
    requires = Requires()
    requirement = Requirement(DownloadData)

    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'dataset/'
    path = os.path.join(LOCAL_ROOT, SHARED_RELATIVE_PATH)
    if not os.path.isdir(path):
        os.makedirs(path)

    glob1 = 'preprocessed_arXivData.csv'
    glob_path = Parameter(default=glob1)
    ext = '.csv'

    def output(self):
        # return the CSVTarget of the data
        file_output = TargetOutput(target_class=CSVTarget,
                                   file_pattern="data/dataset/{task.__class__.__name__}/",
                                   ext=self.ext).__call__(self)

        return file_output

    def run(self):
        json_data = json.load(self.input()["requirement"].open())
        df = pd.DataFrame(json_data)

        df = arxiv_clean(df)
        # Convert df to dask df
        ddf = dd.from_pandas(df, npartitions=1)
        print(ddf.head())

        self.output().write_dask(ddf)
        output_path = self.path + self.glob_path

        df.to_csv(output_path, index=False)


class find_display_abstracts(Task):
    model_rationale = 'rationale_roberta_large_fever.zip'
    model_label = 'label_roberta_large_fever_scifact.zip'

    pdf_name = Parameter(
        default="Dual Recurrent Attention Units ")  # Downloading pdf with the title
    doc_query = Parameter(
        default='Bilinear representations Fukui et al. [7] use compact bi-linear pooling to attend over the image features and com-bine it with the language representation.')
    top_matches = luigi.IntParameter(
        default=5)

    def requires(self):
        return DownloadModel(self.model_rationale), DownloadModel(self.model_label), Preprocess_arxiv_data()

    def run(self):
        working_dir = os.path.dirname(os.getcwd())
        arxiv_data_path = working_dir + "/dataset/preprocessed_arXivData.csv"
        model_path = working_dir + "/saved_models/rationale_roberta_large_fever"

        if os.path.isdir(model_path) and os.path.isfile(arxiv_data_path):
            arxiv_data = pd.read_csv(arxiv_data_path)
            pdf_data = find_download_pdf(self.pdf_name, arxiv_data)
            references = extract_ref_pdf(pdf_data)

            pm = rationale_label_selection()
            pm.printwd()
            pm.abstract_selection(self.doc_query, references, self.top_matches, arxiv_data)

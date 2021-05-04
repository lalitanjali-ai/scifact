import os
from luigi import ExternalTask, Parameter, Task, LocalTarget
from tasks.download import DownloadData, DownloadModel
from environs import Env
import json
import dask.dataframe as dd
import pandas as pd
import io


from csci_utils.luigi.luigi_task import TargetOutput, Requirement, Requires
from csci_utils.luigi.dask_target import CSVTarget, ParquetTarget

from tasks.arxiv_preprocess import arxiv_clean

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

    glob1 = 'arXivData.csv'
    glob_path= Parameter(default=glob1)
    ext ='.csv'

    def output(self):
        # return the CSVTarget of the data
        #output = CSVTarget(self.s3_path, glob=self.glob_path,storage_options=dict(requester_pays=True))

        # output = TargetOutput(
        #     file_pattern=self.path + self.glob_path,
        #     ext="",
        #     target_class=CSVTarget,
        #     storage_options=dict(requester_pays=True),
        # ).__call__(self)

        file_output = TargetOutput(target_class=CSVTarget,
                                   file_pattern="data/dataset/{task.__class__.__name__}/",
                                   ext=self.ext).__call__(self)

        return file_output

    def run(self):
        json_data=json.load(self.input()["requirement"].open())
        df = pd.DataFrame(json_data)
        #print(df.head())

        out=arxiv_clean(df)
        #print(out.head())

        ddf = dd.from_pandas(out, npartitions=50)
        print(ddf.head())

        self.output().write_dask(ddf)

        output_path = self.path + self.glob_path
        ddf.to_csv(output_path)

        # with open(self.output(), "a") as f:
        #     out.to_csv(f, header=False, index=False)
        #
        #
        #
        #









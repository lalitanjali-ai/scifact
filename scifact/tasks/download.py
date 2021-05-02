import os
from luigi import ExternalTask, Parameter, Task, LocalTarget
from luigi.contrib.s3 import S3Target, S3Client
from environs import Env

env = Env()
env.read_env()

class ContentData(ExternalTask):
    DATA_ROOT = 's3://advancedpythonmeenu/scifact/' # Root S3 path, as a constant
    data_name = Parameter(default="arxivData.json") # Filename of the dataset under the root s3 path
    client = S3Client(env("AWS_ACCESS_KEY_ID"), env("AWS_SECRET_ACCESS_KEY"))

    def output(self):
        # return the S3Target of the dataset
        return S3Target(self.DATA_ROOT+self.data_name,client=self.client)

class DownloadData(Task):
    S3_ROOT = 's3://advancedpythonmeenu/scifact/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'dataset/'

    data = Parameter(default="arxivData.json") # luigi parameter
    path = os.path.join(LOCAL_ROOT, SHARED_RELATIVE_PATH)

    if not os.path.isdir(path):
        os.makedirs(path)

    def requires(self):
        # Depends on the ContentData ExternalTask being complete
        return ContentData()

    def output(self):
        return LocalTarget(self.path+self.data)

    def run(self):
        s3filename=str(self.S3_ROOT+self.data)

        print("S3 filename:",s3filename)
        print("Local path:",self.path)

        client = S3Client(env("AWS_ACCESS_KEY_ID"), env("AWS_SECRET_ACCESS_KEY"))
        #This function creates the file atomically
        client.get(s3filename,self.path+self.data)


class SavedModel(ExternalTask):
    MODEL_ROOT = 's3://advancedpythonmeenu/scifact/'

    model = Parameter(default="rationale_roberta_large_fever.zip") # Filename of the model
    client = S3Client(env("AWS_ACCESS_KEY_ID"), env("AWS_SECRET_ACCESS_KEY"))

    def output(self):
        # return the S3Target of the model
        return S3Target(self.MODEL_ROOT + self.model, client=self.client)

class DownloadModel(Task):
    S3_ROOT = 's3://advancedpythonmeenu/scifact/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'saved_models/'
    path = os.path.join(LOCAL_ROOT, SHARED_RELATIVE_PATH)

    if not os.path.isdir(path):
        os.makedirs(path)

    model = Parameter(default="rationale_roberta_large_fever.zip")# luigi parameter

    def requires(self):
        # Depends on the SavedModel ExternalTask being complete
        # i.e. the file must exist on S3 in order to copy it locally
        return SavedModel()

    def output(self):
        #print(self.path+self.model)
        return LocalTarget(self.path+self.model)

    def run(self):
        s3filename = str(self.S3_ROOT + self.model)

        print("S3 filename:", s3filename)
        print("Local path:", self.path)

        client = S3Client(env("AWS_ACCESS_KEY_ID"), env("AWS_SECRET_ACCESS_KEY"))
        # This function creates the file atomically
        client.get(s3filename, self.path + self.model)


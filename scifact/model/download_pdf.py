import textract
import arxiv
import ssl
import os
import zipfile


def find_download_pdf(pdf_name,data):
    """Given a name of a pdf, downloads the pdf

    :param pdf_name: name of the pdf to download which contains to claim
    :type pdf_name:  str
    :param data: arxiv dataset which contains the details of all pdfs and their authors, links etc
    :type data:  pandas dataframe

    :return: all the content/text found in the pdf
    :rtype: str
    """

    #SSL Certificate to download pdf from link
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    df1 = data[data['title'].str.contains(pdf_name)]

    reference_id = {"id": df1.iloc[0, 1]}

    reference_get = next(arxiv.Search(id_list=[reference_id['id']]).get())
    paper_reference = reference_get.download_pdf()

    ref_text = textract.process(paper_reference, method='pdfminer')

    #Convert text type from bytes to string
    ref_text=ref_text.decode("utf-8")

    ref_text = ref_text.replace('\x0c','')

    return ref_text

def extract_ref_pdf(text):
    """Extract portion of the pdf that appears in the References section

    :param text: contents of the pdf in str form
    :type text:  str

    :return: text of all the References found in the pdf
    :rtype: str
    """
    # Extract only the references section from the entire pdf
    # get only text after word 'References'
    pos = text.find('References')
    reference_text = text[pos + len('References '):]

    return reference_text

def unzip(path_to_zip_file,dir_path):
    """Unzip a folder

    :param path_to_zip_file: path to the zipped folder
    :type path_to_zip_file:  str
    :param dir_path: path to place unzipped files
    :type dir_path:  str

    """
    os.chdir(dir_path)

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Done!')


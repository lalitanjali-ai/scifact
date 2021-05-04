import textract
import arxiv
import ssl

def find_download_pdf(pdf_name,data):
    """ Given a name of a pdf, downloads the pdf
           Parameters
           ----------
           pdf_name: str
               name of the pdf to download which contains to claim
           data: pandas dataframe
               arxiv dataset which contains the details of all pdfs and their authors, links etc

           Returns
           -------
           str
               str of all the content found in the pdf
    """

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

    #text = text.replace('.','')
    ref_text = ref_text.replace('\x0c','')

    return ref_text

def extract_ref_pdf(text):
    """ Extract portion of the pdf that appears in the References section
               Parameters
               ----------
               text: str
                    contents of the pdf in str form

               Returns
               -------
               str
                   str of all the References found in the pdf
        """
    # Extract only the references section from the entire pdf
    # get only text after word 'References'
    pos = text.find('References')
    reference_text = text[pos + len('References '):]

    return reference_text

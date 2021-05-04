import textract
import arxiv
import ssl

def find_download(pdf_name,data):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context


    df1 = data[data['title'].str.contains(pdf_name)]
    print(df1)
    reference_link = {"pdf_url": df1.iloc[0, 12]}
    reference_id = {"id": df1.iloc[0, 1]}

    reference_get = next(arxiv.Search(id_list=[reference_id['id']]).get())
    paper_reference = reference_get.download_pdf()

    ref_text = textract.process(paper_reference, method='pdfminer')

    #Convert text type from bytes to string
    ref_text=ref_text.decode("utf-8")

    #text = text.replace('.','')
    ref_text = ref_text.replace('\x0c','')
    table_of_contents_raw = ref_text.split('\n')

    return ref_text

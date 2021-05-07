import luigi
from scifact.tasks.tasks import find_display_abstracts

def main(args=None):

    pdf_name = "Dual Recurrent Attention Units "
    doc_query = 'Bilinear representations Fukui et al. [7] use compact bi-linear pooling to' \
                ' attend over the image features and com-bine it with the language representation.'
    top_matches = 5


    luigi.build([find_display_abstracts(pdf_name=pdf_name,doc_query=doc_query,top_matches=top_matches)],local_scheduler=True)



import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

abs_path = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(abs_path, 'test_files/test_file_pdf.pdf')
plain_path = os.path.join(abs_path, 'test_files/test_file_plain.txt')
docx_path = os.path.join(abs_path, 'test_files/test_file_word.docx')

# pdf_file = SimpleUploadedFile("test_file_pdf.pdf", b"file_content", content_type="application/pdf")

url_options = reverse('get_options_simplification')
url_simplification = reverse('simplification_post')
url_simplification_file = reverse('simplification_file_post')

original_text = "Het Van Goghmuseum in Amsterdam heeft vier kostbare prenten verworven van Mary Cassatt, " \
                "de Amerikaanse impressionistische kunstenaar en tijdgenoot van Vincent van Gogh. Dat heeft het " \
                "museum woensdagmiddag op een persconferentie bekendgemaakt. Het gaat om drie grote kleurenetsen en " \
                "een zwart-wit litho met voorstellingen van vrouwen. Voor deze prenten, die afkomstig zijn van een " \
                "Amerikaanse verzamelaar, betaalde het museum ruim 1,4 miljoen euro. Drie grote fondsen en een aantal " \
                "particulieren hebben samen de aankoopsom beschikbaar gesteld. Mary Stevenson Cassatt (1844-1926) " \
                "woonde en werkte lange tijd in Frankrijk. Ze staat met haar impressionistische schilderijen en " \
                "tekeningen te boek als een van de vernieuwers van de Parijse kunstwereld in de late negentiende eeuw."
simplified_text = "Het Van Goghmuseum heeft vier kostbare prenten verworven. Het gaat om drie grote kleurenetsen en " \
                  "een zwart-wit litho. Het museum betaalde ruim 1,4 miljoen euro voor de aankoop. De verzamelaar is " \
                  "een Amerikaanse impressionistische kunstenaar. De vier kunstwerken zijn afkomstig van Mary " \
                  "Cassatt, een tijdgenoot van Vincent van Gogh. De Amerikaanse kunstenaar is te herkennen als een " \
                  "van de vernieuwers van de Parijs"
correct_options = {
    "model_name": "T5",
    "model_options":
        {
            "max_length_sum": 0.95,
            "min_length_sum": 0.05,
            "max_length_original": 512
        }
}

invalid_options_model_name = {
    "model_name": "invalid_model_name",
    "model_options":
        {
            "max_length_sum": 0.95,
            "min_length_sum": 0.05,
            "max_length_original": 512
        }
}

invalid_options_option_name = {
    "model_name": "T5",
    "model_options":
        {
            "invalid_option_name": 0.95,
            "min_length_sum": 0.05,
            "max_length_original": 512
        }
}


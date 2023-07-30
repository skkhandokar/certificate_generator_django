



from turtle import width
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponseServerError
from io import BytesIO
from matplotlib.font_manager import weight_dict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from .models import Certificate
from django.template.loader import render_to_string
from jinja2 import Environment, BaseLoader
from django.template import engines
from reportlab.lib.units import inch





from django.shortcuts import render, HttpResponse,get_object_or_404
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import landscape

def index(request):
    return render(request, "index.html")



def verify(request):
    if request.method == "POST":
        certificate_id = request.POST.get("certificate_id")
        # You can add more fields to the form if needed for validation, such as digital signature, etc.
        ok = True
        try:
            certificate = get_object_or_404(Certificate, pk=certificate_id)
            # Validate the certificate based on your criteria here
            # For example, you can check the digital signature, or any other custom validation.

            # Set a flag to indicate whether the certificate is valid or not
            is_valid_certificate = True

        except :
            # If the certificate with the given ID doesn't exist, it's invalid
            is_valid_certificate = False
        
        return render(request, "verification.html", {"is_valid_certificate": is_valid_certificate,"ok": ok})

    return render(request,"verification.html")

    
def download_certificate_pdf(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)

    # Load the certificate image to get its dimensions
    certificate_image = ImageReader(certificate.image.path)  # Assuming the image is stored locally
    image_width, image_height = certificate_image.getSize()

    # Set the PDF canvas size based on the image dimensions
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=landscape((image_width, image_height)))

    # Draw the image on the PDF canvas with accurate size
    c.drawImage(certificate_image, 0, 0, width=image_width, height=image_height)

    # Save the canvas as a PDF
    c.save()

    # Rewind the buffer for reading and return the response with the PDF content
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.pk}.pdf"'
    return response



def certificate_display(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    return render(request, "certificate_display.html", {"certificate": certificate})

def generate_certificate_pdf(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        signature = request.POST.get("signature")
        certificate = Certificate(name=name, signature=signature, date=date)
        certificate.save()

        image = Image.open("static/certificate.jpg")
        draw = ImageDraw.Draw(image)

        # Set the font and font size
        font = ImageFont.truetype("static/fonts/BRUSHSCI.TTF", 30)
        signature_font = ImageFont.truetype("static/fonts/Sunydate-PERSONAL USE ONLY.otf", 10)
        date_font = ImageFont.truetype("static/fonts/HelveticaNowText-Regular.otf", 10)

        # Set the text colors
        text_color = (19, 21, 22)  # Black
        signature_color = (19, 21, 22)  # Red
        date_color = (19, 25, 26)
        id_color = (2, 3, 18)  # Hex color: #020312

        # Calculate the position to center the text on the image
        text_width, text_height = draw.textsize(name, font=font)


        image_width, image_height = image.size

        x_position = (image_width - text_width) / 2
        y_position = (image_height - text_height) / 2

        # Draw the text on the image
        x_position=55
        y_position=170       
        draw.text((x_position, y_position), name, fill=text_color, font=font)

        x_position = 285
        y_position = 337
        draw.text((x_position, y_position), date, fill=date_color, font=date_font)

        x_position = 405
        y_position = 335
        draw.text((x_position, y_position), signature, fill=signature_color, font=signature_font)

        x_position = 25
        y_position = 7
        draw.text((x_position, y_position), "ID " + str(certificate.pk), fill=id_color, font=date_font)

        # Save the modified image under the certificate_image field of the certificate model
        buffer = BytesIO()
        image.save(buffer, format="JPEG")

        # Save the buffer as the certificate_image field of the certificate model
        certificate.image.save(f"certificate_{certificate.pk}.jpg", buffer)

        # return redirect('generate_certificate_pdf')
        return redirect('certificate_display', certificate_id=certificate.pk)
    return render(request, "certificate_form.html")
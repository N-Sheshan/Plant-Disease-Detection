from django.core.files.base import ContentFile
from PIL import Image
import numpy as np
from .ml_utils import predict
from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .form import UploadForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.platypus import Paragraph
from io import BytesIO
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet



def upload_form(request):
    return render(request, 'index.html', {'form': UploadForm()})



def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            
            # Read the image and encode it as base64
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Save the image file in Django's default storage
            saved_file_path = default_storage.save(image_file.name, ContentFile(image_data))
            image=request.FILES["image"]
            img = Image.open(image)
            img_array = np.array(img)
            # resized_img = zoom(img_array, (256 / img_array.shape[0], 256 / img_array.shape[1], 1))
            resized_img = np.expand_dims(img_array, 0)
            predicted,confident = predict(resized_img,request)
            return render(request, 'result.html', {'predicted': predicted ,'confident':confident,'base64_image': base64_image})
    else:

        return redirect('upload_form')



def generate_report(request):
    buffer = BytesIO()
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="report.pdf"' 
    #  # Create a response object with appropriate headers for PDF download
    # response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    

    p = canvas.Canvas(response, pagesize=letter)
    p.setLineWidth(1.5)
    p.line(15, 9.9*inch, 8.5*inch-15, 9.9*inch)
    p.line(15, 0.4*inch, 8.5*inch-15, 0.4*inch)


    #diplay the logo
    logo_path = 'static\images\logo4.png'

    # Draw the logo on the PDF
    p.drawImage(logo_path, 30, 10*inch, width=2*inch, height=0.9*inch)

    # Add text to the PDF
   # Set font size and color
    p.setFont("Helvetica", 12)  # You can adjust the font family and size
    p.setFillColor(colors.black)  # You can set the color using RGB or predefined colors
    v1 = request.session.get('predicted_class', '')
    v2 = request.session.get('confidence', '')
    # Add text to the PDF
    
    current_datetime = datetime.now()
    # Add more text with increased font size and different color
    p.setFont("Helvetica-Bold", 17)  # You can use a bold font
    p.setFillColor(colors.black)  # You can set a different color
    p.drawString(3.7*inch, 10.4*inch, " Report ")
    p.drawString(6*inch, 10.62*inch, f"Date    : {current_datetime.date()}")# Adjust the coordinates as needed
    p.drawString(6*inch, 10.25*inch, f"Timing : {current_datetime.time().strftime('%H:%M:%S')}")
    p.setFont("Helvetica-Bold", 22) 
    p.drawString(20, 9.1*inch, "Uploaded Image :")
    p.line(20, 9.01*inch, 3.01*inch-15, 9.01*inch)
     # Draw the base64-encoded image
    base64_image = request.session.get('base64_image', '')
    if base64_image:
        try:
            image_data = base64.b64decode(base64_image)
            img_path = 'image.jpg'  # Set the path to save the image
            with open(img_path, 'wb') as f:
                f.write(image_data)

            # Draw the image on the PDF
            # p.setFillColor(colors.green)
            p.drawImage(img_path, 140, 440, width=250, height=200)
        except Exception as e:
            print("Error decoding or drawing image:", e)

    p.drawString(20, 5.6*inch, "Result :")
    p.line(20, 5.52*inch, 1.6*inch-15, 5.52*inch)
    p.setFont("Helvetica-Bold", 15) 
    if str(v1) == "Healthy":
        p.drawString(100, 360, f'"{str(v1)} "Plant')
    else:
        p.drawString(100, 360, f'Disease of the Plant is " {str(v1)}"')
    p.drawString(100, 330, f'Confidence Level is "{str(v2)}%"')
    p.setFont("Helvetica-Bold", 22) 
    p.drawString(20, 3.78*inch, "About Plant:")
    p.line(20, 3.7*inch, 2.3*inch-15, 3.7*inch)
    p.setFont("Helvetica", 17)
    pageWidth = 8*inch
    styles = getSampleStyleSheet()
    custom_style = styles["Normal"]
    custom_style.fontSize = 13 
    custom_style.leading = 14
    custom_style.textColor = colors.Color(0.2, 0.2, 0.2) 
    if str(v1) == "Healthy":
        text = """A healthy plant refers to a plant that exhibits robust growth, vitality, and overall well-being.
         Such plants typically have vibrant green leaves, strong stems, and an active reproductive capacity. They 
         are free from diseases, pests, and nutritional deficiencies, showcasing a balance in their physiological 
         processes. Healthy plants are resilient to environmental stressors and can effectively carry out essential 
         functions like photosynthesis and nutrient absorption. Adequate sunlight, proper watering, and a 
         nutrient-rich soil contribute to the overall health of a plant. Regular monitoring for signs of distress
          and timely intervention can help maintain the optimal condition of a plant, ensuring its ability to thrive 
          and fulfill its ecological role."""
        paragraph = Paragraph(text, custom_style)
        paragraph.wrapOn(p, pageWidth - 90, 11*inch)
        paragraph.drawOn(p, 90,135) 
    elif str(v1) == "Powdery" :
        text="""Powdery plant diseases refer to fungal infections that manifest as a powdery, white or grayish
         substance on the surfaces of plant leaves, stems, and sometimes flowers. This powdery residue consists 
         of fungal spores and mycelium, hindering the plant's ability to photosynthesize and compromising its 
         overall health. Unlike some diseases that require water for spore germination, powdery mildews thrive 
         in dry conditions, making them prevalent in arid climates. Effective management strategies include pruning 
         affected plant parts, improving air circulation, and applying fungicides to prevent or control the spread 
         of the disease. Regular monitoring and early intervention are crucial for minimizing the impact of 
         powdery plant diseases and preserving the vitality of affected plants."""
        paragraph = Paragraph(text, custom_style)
        paragraph.wrapOn(p, pageWidth - 90, 11*inch)
        paragraph.drawOn(p, 90,120) 
    elif str(v1) == "Rust":
        text="""Rust is a plant disease caused by various fungi that typically manifest as reddish-brown or orange 
        powdery spots on the leaves, stems, or other plant parts. These fungal infections weaken the plant by 
        disrupting its ability to photosynthesize and absorb nutrients. Rust diseases are often specific to certain 
        plant species and can lead to reduced crop yields and overall plant health. Prevention involves practices
         such as crop rotation, selecting resistant plant varieties, and applying fungicides when necessary. Timely
          identification and management of rust diseases are crucial for maintaining the vitality of plants and 
          preventing the spread of infections within a crop or garden."""
        paragraph = Paragraph(text, custom_style)
        paragraph.wrapOn(p, pageWidth - 90, 11*inch)
        paragraph.drawOn(p, 90,130) 
    else:
        text = "Empty"
        paragraph = Paragraph(text, custom_style)
        paragraph.wrapOn(p, pageWidth - 90, 11*inch)
        paragraph.drawOn(p, 90,202) 

    # Load the image as a watermark
    watermark_path = 'static\images\watermark4.jpg'
    opacity = 0.19
    p.setFillColorRGB(1, 1, 1, alpha=opacity)
    p.rotate(-45)
    p.drawImage(watermark_path, -200, 230, width=5*inch, height=5*inch, preserveAspectRatio=True)
    p.setFillColorRGB(0, 0, 0)  # Black color

    p.showPage()
    p.save()
    buffer.seek(0)

   
    response.write(buffer.read())

    return response

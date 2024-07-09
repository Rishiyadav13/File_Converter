from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import User ,CaptchaData
from xhtml2pdf import pisa
from io import BytesIO
import os,sys
import random
import string
from django.core.files.storage import FileSystemStorage
import pypandoc
from captcha.image import ImageCaptcha

import logging
logger=logging.getLogger(__name__)
# logger=logging.getLogger('detail')




@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def html_to_pdf_view(request):
    output_filename = 'test.pdf'
    if request.method == 'POST' and request.FILES['html_file']:
        html_file = request.FILES['html_file']
        html_content = html_file.read().decode('utf-8')
        result = BytesIO()
        pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=result)
        if pisa_status.err:
            return HttpResponse('Error while converting HTML to PDF', status=400)
        result.seek(0)
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        action = request.POST.get('action', 'view')
        if action == 'download':
            response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
        else:
            response['Content-Disposition'] = f'inline; filename="{output_filename}"'
        return response
    return render(request, 'html_to_pdf.html')



def generate_captcha(request):
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    captcha_otp = CaptchaData(captcha_text=captcha_text)
    captcha_otp.save()
    image = ImageCaptcha(width=300, height=60)
    captcha_image_path = os.path.join(settings.MEDIA_ROOT, f'{captcha_text}.png')
    image.write(captcha_text, captcha_image_path)
    image_url = os.path.join(settings.MEDIA_URL, f'{captcha_text}.png')
    return JsonResponse({'image_url': image_url})



@login_required
def convert_docx_to_pdf(request):
    if request.method == 'POST':
        docx_file = request.FILES.get('docx_file')
        if not docx_file:
            return HttpResponse("No file uploaded. Please upload a DOCX file.", status=400)
        if not docx_file.name.endswith('.docx'):
            return HttpResponse("Invalid file type. Please upload a DOCX file.", status=400)
        fs = FileSystemStorage()
        filename = fs.save(docx_file.name, docx_file)
        uploaded_file_path = fs.path(filename)
        pdf_file_path = f"{uploaded_file_path}.pdf"
        try:
            output = pypandoc.convert_file(
                uploaded_file_path, 
                'pdf', 
                outputfile=pdf_file_path, 
                extra_args=['--pdf-engine=xelatex']
            )
            assert output == ""
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            action = request.POST.get('action', 'view')
            if action == 'download':
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file_path)}"'
            else:
                response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_file_path)}"'
        os.remove(uploaded_file_path)
        os.remove(pdf_file_path)
        return response
    return render(request, 'convert.html')




def register_view(request):
    if request.method == 'POST':
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username= request.POST.get("username")
        phone_no= request.POST.get("phone_no")
        email= request.POST.get("email")
        password= request.POST.get("password")
        image= request.FILES.get("profile_photo")
        confirm_password = request.POST.get("confirm_password")
        captcha= request.POST.get("captcha")
        en_captcha= CaptchaData.objects.latest('created_at').captcha_text
        if captcha == en_captcha:  
            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():  
                    messages.info(request, 'Username Taken')
                    return redirect('register') 
                else:
                    user_obj = User.objects.create(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        phone_no=phone_no,
                        email=email,
                        image=image,
                    )
                    user_obj.set_password(password)
                    user_obj.save()
                    # subject= 'Welcome to Our Website!'
                    # message= f'Hi {first_name},\n\nThank you for registering on our website.'
                    # from_email= settings.EMAIL_HOST_USER
                    # to_email= [email]
                    # send_mail(subject, message, from_email, to_email)
                    return redirect('login')
            else:
                messages.info(request, 'Password Not Matching')
        else:
            messages.info(request, 'Enter Valid Captcha')   
            return redirect('register')
    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email= request.POST.get("email")
        password = request.POST.get("password")
        user= authenticate(email=email,password=password)
        if user is not None:
            login(request, user)
            logger.info("Successfuly login")
            return redirect('home')
        else:
            logger.info("Enter Valid Credentials")
            # messages.info(request, 'Credentials Invalid')
            return redirect('login')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    current_user = request.user
    user_detail = User.objects.get(id=current_user.id)
    if request.method == 'POST':
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username= request.POST.get("username")
        phone_no= request.POST.get("phone_no")
        email= request.POST.get("email")
        user_detail.first_name= first_name
        user_detail.last_name= last_name
        user_detail.username= username
        user_detail.phone_no= phone_no
        user_detail.email= email
        if 'profile_photo' in request.FILES:
            user_detail.image= request.FILES['profile_photo']
        user_detail.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')
    else:
        context = {
            'first_name': user_detail.first_name,
            'last_name': user_detail.last_name,
            'username': user_detail.username,
            'phone_no': user_detail.phone_no,
            'email': user_detail.email,
            'image': user_detail.image,
        }
        return render(request, 'profile.html', context)
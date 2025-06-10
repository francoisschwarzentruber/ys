from django.http import HttpResponse
from django.template import loader
from .models import Member, Report, Review
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from django.shortcuts import render
from .forms import SubmitReportForm
from .forms import SubmitReviewForm
from django.shortcuts import redirect
import datetime

DEADLINE = datetime.datetime(2025, 8, 18, 0, 0)



def is_reviewer(user):
    return user.groups.filter(name="reviewers").exists()


def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))



def all_reports(request):
  user = request.user
  
  if(user.is_anonymous):
      return redirect("")
    
  if not is_reviewer(user):
       return redirect("")
    
  reports = Report.objects.all().values()
  template = loader.get_template('all_reports.html')
  context = {
    'reports': reports,
  }
  return HttpResponse(template.render(context, request))




def download_report(request, id):
    user = request.user
    
    if(user.is_anonymous):
        return redirect("")
    
    report = Report.objects.filter(id=id).get()
    response = FileResponse(open(report.pdf.path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="{report.pdf}"'
    return response
  
  



def handle_uploaded_report(filename, f):  
    with open(filename, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)
            




def submit_report(request):
    user = request.user
    if(user.is_anonymous):
        return redirect("")

    context = {}
  
    context['user'] = request.user
    
    
    
    report = Report.objects.filter(author=user).first()

    context['report'] = report
    context['DEADLINE'] = DEADLINE
    
    toolate = datetime.datetime.now() > DEADLINE
    
    if toolate:
        return render( request, "toolate.html", context)
    
    if request.POST:
        form = SubmitReportForm(request.POST, request.FILES)
        if form.is_valid():
            filename = 'reportspdf/'+str(user.id)+'.pdf'
            
            if report == None:
                report = Report(
                    author=user
                )
                
            report.title = form.cleaned_data['title']
            report.save()
            report.pdf = 'reportspdf/'+str(report.id)+'.pdf'
            report.save()
            
            # Handle the uploaded file
            handle_uploaded_report(filename, request.FILES["pdf"])
            
        return render( request, "submit_report_thankyou.html", context)
    else:
        form = SubmitReportForm(initial={"title": report.title} if report is not None else None)
        context['form'] = form
        return render( request, "submit_report.html", context)
  
  
  
def submit_review(request, id):
    
    user = request.user
    context = {}
    context['user'] = user
    
    
    if(user.is_anonymous):
        return redirect("")
    
    if not is_reviewer(user):
       return redirect("")
   
    if not Report.objects.filter(id=id).exists():
        return redirect("")
    
    report = Report.objects.get(id=id)
    
    context['report'] = report
    
    review = Review.objects.filter(reviewer=user, report=report).first()

    
    if request.POST:
        form = SubmitReviewForm(request.POST, request.FILES)
        if form.is_valid():
            
            if review == None:
                review = Review(
                    report = report,
                    reviewer = user,
                )
            review.review = form.cleaned_data['review']
                
            review.save()
            
            context['saved'] = True
        
    form = SubmitReviewForm(initial={"review": review.review} if review is not None else None)
    context['form'] = form
    return render( request, "submit_review.html", context)

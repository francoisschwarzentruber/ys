from django.http import HttpResponse
from django.template import loader
from .models import Member, Report
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from django.shortcuts import render
from .forms import SubmitReportForm
from .forms import SubmitReviewForm
from django.shortcuts import redirect



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
    response = FileResponse(open(report.report.path, 'rb'))
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
    
    if request.POST:
        form = SubmitReportForm(request.POST, request.FILES)
        if form.is_valid():
            filename = 'reportspdf/'+str(user.id)+'.pdf'
            
            report = Report.objects.filter(author=user).first()
            
            if report == None:
                report = Report(
                    author=user,
                    title=form.cleaned_data['title'],
                )
                
            report.save()
            report.pdf = 'reportspdf/'+str(report.id)+'.pdf'
            report.save()
            
            # Handle the uploaded file
            handle_uploaded_report(filename, request.FILES["pdf"])
            
        return render( request, "submit_report_thankyou.html", context)
    else:
        form = SubmitReportForm()
        context['form'] = form
        return render( request, "submit_report.html", context)
  
  
  
def submit_review(request, id_report):
  
    user = request.user
    context = {}
    context['user'] = user
    
    if(user.is_anonymous):
        return redirect("")
    
    
    if not is_reviewer(user):
       return redirect("")
    
    if request.POST:
        form = SubmitReviewForm(request.POST, request.FILES)
        if form.is_valid():
            pass
            
        return render( request, "submit_review_thankyou.html", context)
    else:
        form = SubmitReviewForm()
        context['form'] = form
        return render( request, "submit_review.html", context)

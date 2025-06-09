from django.http import HttpResponse
from django.template import loader
from .models import Member, Submission
from django.shortcuts import get_object_or_404
from django.http import FileResponse

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))



def submissions(request):
  submissions = Submission.objects.all().values()
  template = loader.get_template('all_submissions.html')
  context = {
    'submissions': submissions,
  }
  return HttpResponse(template.render(context, request))




def download_submission(request, id):
    submission = Submission.objects.filter(id=id).get()
    response = FileResponse(open(submission.report.path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="{submission.report}"'
    return response
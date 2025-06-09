from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    user = request.user
    
    if user.is_anonymous:
        return redirect('/accounts/login')
    
    if user.groups.filter(name='reviewers').exists():
       return redirect('/all_reports')
    else:
        return redirect('/submit_report') 
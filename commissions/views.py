from django.shortcuts import render
from .models import Commission, Comment

def comms_list(request):
    commissions = Commission.objects.all().order_by('title')
    ctx = {"commissions": commissions}
    return render(request, "commissions/comms_list.html", ctx)

def comm_detail(request, id):
    commission = Commission.objects.get(id__exact=id)
    comments = Comment.objects.filter(commission__pk=id)
    ctx = {"commission": commission, "comments": comments}
    return render(request, "commissions/comm_detail.html", ctx)

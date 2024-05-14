from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Profile, Commission, Job, JobApplication
from .forms import CommissionForm, JobForm, JobApplicationForm


def comms_list(request):
    all_comms = Commission.objects.all()
    if request.user.is_authenticated:
        curr_profile = Profile.objects.get(user=request.user)
        created_comms = Commission.objects.filter(author=curr_profile)
        applied_comms = Commission.objects.filter(jobs__applications__applicant=curr_profile)

        ctx = { "created_comms": created_comms, "applied_comms": applied_comms,
                "all_comms": all_comms }
    else:
        ctx = { "all_comms": all_comms }
    return render(request, "commissions/comms_list.html", ctx)


def comm_detail(request, id):
    curr_profile = Profile.objects.get(user=request.user)
    comm = Commission.objects.get(id=id)
    job_apply_form = JobApplicationForm()
    jobs_needed = Job.objects.filter(commission=id)
    signed_applicants = len(Commission.objects.filter(jobs__applications__status='2_ACPT'))
    manpower_needed = 0
    for job in jobs_needed:
        manpower_needed += job.manpower_required
    open_manpower = manpower_needed - signed_applicants
    if request.method == 'POST':
        job_apply_form = JobApplicationForm(request.POST)
        if job_apply_form.is_valid():
            temp_form = job_apply_form.save(commit=False)
            temp_form.applicant = Profile.objects.get(user=request.user)
            temp_form.save()
    ctx = { "curr_profile": curr_profile, "comm": comm, "job_apply_form": job_apply_form,
           "manpower_needed": manpower_needed, "open_manpower": open_manpower }
    return render(request, "commissions/comm_detail.html", ctx)


@login_required
def comm_create(request):
    curr_profile = Profile.objects.get(user=request.user)
    comm_form = CommissionForm(initial={'author': curr_profile})
    job_form = JobForm()
    if request.method == 'POST':
        if 'comm_submit' in request.POST:
            comm_form = CommissionForm(request.POST)
            if comm_form.is_valid():
                new_comm = comm_form.save()
                return redirect('commissions:comm_detail', id=new_comm.id)
        elif 'job_submit' in request.POST:
            job_form = JobForm(request.POST)
            if job_form.is_valid():
                job_form.save()
    ctx = { "comm_form": comm_form, "job_form": job_form }
    return render(request, "commissions/comm_create.html", ctx)


@login_required
def comm_update(request, id):
    curr_profile = Profile.objects.get(user=request.user)
    comm = Commission.objects.get(id=id)
    comm_update_form = CommissionForm(instance=comm)
    if request.method == 'POST':
        comm_update_form = CommissionForm(request.POST)
        if comm_update_form.is_valid():
            updated_comm = comm_update_form.save(commit=False)
            updated_comm.id = comm.id
            updated_comm.created_on = comm.created_on
            is_full = True
            for job in Job.objects.filter(commission=id):
                if job != 'Full':
                    is_full = False
            if is_full:
                updated_comm.status = 'FULL'
            updated_comm.save()
            return redirect('commissions:comm_detail', id=updated_comm.id)
    ctx = { "curr_profile": curr_profile, "comm": comm, "comm_update_form": comm_update_form }
    return render(request, "commissions/comm_update.html", ctx)

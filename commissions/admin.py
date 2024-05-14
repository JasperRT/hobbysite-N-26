from django.contrib import admin
from .models import Commission, Job, JobApplication


class CommissionAdmin(admin.ModelAdmin):
    model = Commission

    search_fields = ('title',)
    list_display = ('title', 'author', 'status', 'created_on', 'updated_on',)


class JobAdmin(admin.ModelAdmin):
    model = Job

    search_fields = ('role',)
    list_display = ('commission', 'role', 'manpower_required', 'status',)


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication

    list_display = ('job', 'applicant', 'status', 'applied_on',)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)

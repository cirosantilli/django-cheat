from django.contrib import admin

from polls.models import Poll
from polls.models import Choice

class ChoiceInline(admin.TabularInline): #makes a table with fields of Choice
    #class ChoiceInline(admin.StackedInline): #stacks the fields of Choice

    model = Choice #each one is based on a Choice object
    extra = 3    #show 3 Choice inlines per Poll add page

class PollAdmin(admin.ModelAdmin):
    #organizes forms in categories
    #data information is collapsable

    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    inlines = [ChoiceInline]
    #show Choice ojects, which refer to Poll objects in the same page as Poll add page
    #each one will use the id of this Poll object

    list_display = ('question',
        'pub_date',
        'was_published_recently',)
    #what data to display on the choose/add Poll page
    #default is str(), which tends not to be very useful
    #can also include functions instead of fields as was_published_recently.
    # by default you cannot sort by an arbitrary function such as this

    list_filter = ['pub_date'] #sidebar filter, knows type of field and makes nice filter for it

    search_fields = ['question'] #creates a search text that looks into row question and filters only matches

    date_hierarchy = 'pub_date' #navigation by date

admin.site.register(Poll, PollAdmin)



from .models_l_env454 import Run
from .forms import RunForm

def get_run(request):
    print "Running get_run from utils"
    run_data = {}
    if request.method == 'POST':
        form = RunForm(request.POST)
        print "request.POST = "
        print request.POST
        if form.is_valid():
            run_data['find_rundate'] = form.cleaned_data['find_rundate'].run
            run_data['find_machine'] = form.cleaned_data['find_machine']
            run_data['find_domain']  = form.cleaned_data['find_domain']
            run_data['find_lane']    = form.cleaned_data['find_lane']

            return (form, run_data)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RunForm()
    return form


# from myapp.utils import my_cool_func
#
# def view_coolness(request):
#     data = my_cool_func(request)
#     return render_to_response("xxx.html")
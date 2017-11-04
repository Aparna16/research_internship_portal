from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import Postform
from .forms import Loginform,EditForm,projectReqs
from .models import Register,project_desc
from django.contrib.auth.decorators import login_required
import random
from student.models import Notifications,Appliedproject,StudentDB
from django.core.mail import send_mail
# Create your views here.
def post_list(request):
    status = 200
    print('hello')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Postform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            instance=form.save(commit=False)
            #print(instance.c_password)
            #print(instance.c_confirm_password)
            instance.c_verification = random.randint(1,1000)
            instance.save()

            #form=Postform()
            #return render(request, 'Professor/tempform.html', {'form': form}, status=status)
            #form.save()
            '''send_mail(
                'Verification Mail',
                'Please verify the mail id by clicking on the below link http:localhost:8000/Professor/verify/'+str(instance.c_verification),
                
                
            )'''
            return render(request, 'Professor/verifymail.html')
        else:
            status = 422
    else:
        form=Postform()
    return render(request, 'Professor/tempform.html', {'form':form},status=status)
def view_home(request):
    if request.session.has_key('username') and request.session.has_key('type'):
        user = request.session['username']
        type = request.session['type']
        if (type == "student"):
            return render(request, 'student/loggedin.html', {'username': user})
        else:
            return render(request, 'Professor/loggedin.html', {'username': user})
    else:
        if request.method == 'POST':
            form=Loginform(data=request.POST)
            #print (form.errors)
            #print (form.non_field_errors)
            if form.is_valid():
                print("Validation Success")
                user=request.POST['username']
                passw=request.POST['password']
                try:
                    r=Register.objects.filter(c_name__exact=user)
                    if r.filter(c_password__exact=passw):
                        if r.values()[0]['c_verified'] :
                            request.session['username'] = user
                            request.session['type'] = "professor"
                            request.session.set_expiry(3000)
                            #form = EditForm()
                            return render(request,'Professor/loggedin.html',{'username':user})
                        else:
                            return render(request,'Professor/verifymail.html')
                    else:
                        return render(request, 'Professor/login_failure.html')
                except:
                    return render(request,'Professor/login_failure.html')
                #instance.save()
            else:
                print("Validation Failed")
                #form = Loginform()
                return render(request, 'Professor/login.html')
        else:
            form=Loginform()
            return render(request,'Professor/login.html',{'form':form})
#@login_required()
def view_edit(request):
    if request.session.has_key('username'):
        user = request.session["username"]
        if request.method == 'POST':
            print(user)
            tmp=Register.objects.get(c_name=user)
            print(tmp.c_professor_name,tmp.c_details)
            form=EditForm(request.POST,request.FILES,instance=tmp)
            print (form.errors)
            print (form.non_field_errors)
            if form.is_valid():
                instance = form.save(commit=False)
                # if instance.c_name!=instance.c_confirm_password:
                instance.save()
                #instance.save()
                return render(request,'Professor/Professorform.html',{'form':form, 'username':user})
            else:
                print("Validation Failed")
                #form = Loginform()
                return render(request, 'Professor/Professorform.html',{'form':form,'username':user})
        else:
            form = EditForm()
            return render(request,'Professor/Professorform.html',{'form':form,'username':user})
    else:
        return HttpResponse("Unauthorised Access")
def verify(request):
    if request.method == 'GET':
        val=int(request.GET['value'])
        name=request.GET['name']
        #print(val,name)
        #print(type(val))
        r=Register.objects.filter(c_name=name)[0]
        print(r)
        if r.c_verification == val:
            print("Success")
            r.c_verified=True
            r.save()
        else:
            pass
        form = EditForm()
        return render(request, 'Professor/verificationsuccess.html', {'form': form})
def projectreqs(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            user=request.session["username"]
            m=Register.objects.get(c_name=user)
            tmp=project_desc.objects.create(register=m)
            form=projectReqs(request.POST,instance=tmp)
            print (form.errors)
            print (form.non_field_errors)
            if form.is_valid():
                instance = form.save(commit=False)
                # if instance.c_name!=instance.c_confirm_password:
                instance.save()
                #i=project_desc.objects.filter(c_position=instance.c_position).update(register=tmp.id)

                #instance.save()
                form=projectReqs()
                return render(request,'Professor/projectreqs.html',{'form':form})
            else:
                print("Validation Failed")
                #form = Loginform()
                return render(request, 'Professor/projectreqs.html',{'form':form})
        else:
            form = projectReqs()
            return render(request,'Professor/projectreqs.html',{'form':form})
    else:
        return HttpResponse("Unauthorised Access")


def profile(request,username):
    if request.session.has_key('username'):
        user=request.session['username']
        tmp=Register.objects.filter(c_name=user)
        form=tmp.values()[0]
        return render(request,'Professor/Professor_profile.html',{'username':user,'form': form})
    else:
        return HttpResponse('Unauthorised Access')

def change_password(request):
    if request.session.has_key('username'):
        user=request.session['username']
        return render(request,'Professor/change_password.html',{'username':user})
    else:
        return HttpResponse('Unauthorised Access')

def successfull_change(request):
    if request.session.has_key('username'):
        user=request.session['username']
        tmp=Register.objects.get(c_name=user)
        try:
            old=request.POST["piCurrPass"]
            print(old)
            print(tmp.c_password)
            if tmp.c_password==old:
                tmp.c_password=request.POST["piNewPass"]
                tmp.c_confirm_password=request.POST["piNewPass"]
                tmp.save(update_fields=['c_password','c_confirm_password'])
        except:
            return HttpResponse('Unauthorised Access')
        return render(request,'Professor/loggedin.html',{'username':user})
    else:
        return HttpResponse('Unauthorised Access')
def listproject(request):
    if request.session.has_key('username'):
        user = request.session['username']
        m=Register.objects.get(c_name=user)
        tmp= project_desc.objects.filter(register=m)
        form=list(tmp.values())
        print(form)
        return render(request, 'Professor/list_project.html', {'form':form,'username':user})
    else:
        return HttpResponse('Unauthorised Access')

def projectdesc(request,projectid):
    #retrieve project description from database having id project id and give option to apply
    disable=""
    if request.session.has_key('username'):
        user = request.session['username']
        request.session['projectid'] = projectid
    else:
        user="Guest"
        disable="disabled"

    tmp=project_desc.objects.filter(pk=projectid)
    t=project_desc.objects.get(pk=projectid)
    form=list(tmp.values())#retrieved row
    name = Register.objects.get(pk=t.register_id).c_name
    return render(request, 'Professor/apply_project.html', {'form':form,'professor':name,'projectid':projectid,'username':user,'disabled':disable})

def projectapplied(request):
    #store student Id to applied, display a student profile page
    if request.session.has_key('projectid') and request.session.has_key('username'):
        projectid=request.session['projectid']
        user=request.session['username']
    else:
        projectid=1
        user="Guest"
    j=project_desc.objects.get(pk=projectid)
    if user in j.list_of_student.split(","):
        return HttpResponse("Already applied !!!")
    else:
        s=StudentDB.objects.get(s_username=user)
        a=Appliedproject(stdid=s,projectid=j)
        a.applied=True
        a.save()
        if(len(j.list_of_student)==0):
            j.list_of_student=user
        else:
            j.list_of_student=j.list_of_student+","+user
        j.save()
        return render(request, 'student/applied_msg.html')

def view_student_list(request,projectid):
    n=project_desc.objects.get(pk=projectid)
    stdnames=n.list_of_student.split(",")
    form=stdnames
    request.session['offerid']=projectid
    return render(request, 'Professor/student_list.html',{'form':form})

def already_taken(request):
    print ("here");
    if request.method == "GET":
        p=request.GET.copy()
        if 'username' in p:
            name=p['username']
            if Register.objects.filter(c_name__iexact=name):
                return HttpResponse("False")
            else:
                return HttpResponse("True")

def offered(request,userid):
    if request.session.has_key('offerid'):
        projectid=request.session['offerid']
        sid=StudentDB.objects.get(s_username=userid)
        j=project_desc.objects.get(pk=projectid)
        a=Appliedproject.objects.get(stdid=sid,projectid=j)
        a.got_offer="Yes"
        a.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)

from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View
from work.forms import Register,loginform,Taskform
from work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,**kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        else:
            return fn(request,**kwargs)
        
    return wrapper

def mylogin(fn):
    def wrapper(request,**kwargs):
        id=kwargs.get("pk")
        obj=Taskmodel.objects.get(id=id)
        if obj.user!=request.user:
            return redirect('signin')
        else:
            return fn(request,**kwargs)
    return wrapper


#  C R U D

# ...........C..........

class Registration(View):
    def get(self,request,**kwargs):
        form=Register()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):
        form=Register(request.POST)
        if form.is_valid():
            # form.save()
            # form=Register()
            # return render(request,"register.html",{"form":form})


            User.objects.create_user(**form.cleaned_data)
            form=Register()
            return render (request,"register.html",{"form":form})
    

# class Update_user(View):
#     def get(self,request,**kwargs):
#         id=kwargs.get("pk")
#         data=User.objects.get(id=id)
#         form=Register(instance=data)
#         return render(request,"register.html",{'form':form})
#     def post(self,request,**kwargs):
#         id=kwargs.get("pk")



class Login(View):
    def get(self,request):
        form=loginform()
        return render (request,"login.html",{"form":form})
    def post (self,request,**kwargs):
        form=loginform(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")

            user_obj=authenticate(username=u_name,password=pwd)
            if user_obj:
                print("valid credentials")
                login(request,user_obj)
                return redirect("index")
            else:
                print("inncoreect")
                return render (request,"login.html")



@method_decorator(signin_required,name="dispatch")    #> dispatch > decorator thazek vere vilikendi vannal villikan...
class Add_task(View):
    def get(self,request):
        form=Taskform()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed') #.all() edku vaum
        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,**kwargs):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user

            # request.user=get the authenticated user(login)
            form.save()
            messages.success(request,"task added successfully")
            form=Taskform()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')          # >>>>>>.......read....
        return render(request,"index.html",{"form":form,"data":data})
        




#  ............delete........


@method_decorator(mylogin,name='dispatch')
@method_decorator(signin_required,name='dispatch')
class Delete_task(View):
    def get(self,request,**kwargs):                     #key word arguments   >kwargs
        id= kwargs.get("pk")

        Taskmodel.objects.get(id=id).delete()
        return redirect("index")



class Task_edit(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")

        obj=Taskmodel.objects.get(id=id)
       

        if obj.completed == False:
            obj.completed = True
            print(obj.completed)
            obj.save()
        return redirect("index")
    


#log out.....


class Signout(View):
    def get(self,request):
        logout(request)
        return redirect('signin')


class User_del(View):
    def get(self,request,**kwargs):
        id=kwargs.get("pk")
        User.objects.get(id=id).delete()
        return redirect ("home")

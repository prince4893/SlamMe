from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from .models import user,abs_user,slam_request,slam_post

def index(request):
    return HttpResponse('Kudos ! this is setup now .. and now you are on the Landing page')

def fetch_signup(request):
    return render(request,'signup.html')

def fetch_login(request):
    context={}
    return get_login_template(request,context)

def get_login_template(request,context):
    return render(request,'login.html',context)

def signup(request):
    if request.method == 'POST':
        name=request.POST['name']
        username=request.POST['username']
        key=request.POST['key']
        try:
            old_user=user.objects.get(username=username)
            #Redirect to signup page after unsuccessful signup
            return fetch_signup(request)
        except:
            new_user1=user(name=name,username=username)
            new_user2=user(uid=new_user1,logged=False,key=key)
            new_user1.save()
            new_user2.save()
            #Redirect to login page after successful signup
            context={
                'status':'Signup Successful !'
            }
            return get_login_template(request,context)
    else:
        return fetch_signup(request)


def login(request):
    if request.method == 'POST':  
        username=request.POST['username']
        key=str(request.POST['key'])
        print(f'login creds = {username} | {key}')
        try:
            correct_username=user.objects.get(username=username)
            correct_creds=abs_user.objects.get(uid=correct_username)
            if correct_creds.key == key:
                correct_creds.logged=True
                correct_creds.save()
                #Successful login
                context={'status':'You are now logged in !',}
                return fetch_home(request)
            else:
                #Incorrect password
                context={'status':'Sorry wrong Credentials !'}
        except:
            #Incorrect Username/ Username not found
            context={'status':'Incorrect username !'}
        return get_login_template(request,context) 
    else:
        return fetch_login(request)

# def fetch_home(request):
#     context={
#         'logged':is_logged(request),
#         'log_user':request.GET.get('user'),
#     }
#     if context['log_user']=='' or context['log_user']==None:
#             context['log_user']=request.POST.get('username')
#     return render(request,'home.html',context)

def fetch_home(request):
    try:
        home_slams=slam_post.objects.raw('select * from slamer_slam_post where public=True')
    except:
        home_slams=None
    context={
        'logged':is_logged(request),
        'log_user':request.GET.get('user'),
        'home_slams':home_slams,
    }
    if context['log_user']=='' or context['log_user']==None:
            context['log_user']=request.POST.get('username')
    return render(request,'home.html',context)

def usearch(request):
    search_user=request.POST['user_search']
    cursor=connection.cursor()
    users=[]
    users_by_username=cursor.execute(f"select * from slamer_user where username like '{search_user}%'")
    users_by_name=cursor.execute(f"select * from slamer_user where name like '{search_user}%'")
    for i in users_by_username:
        if(i[1]!=request.GET.get('user')):
            users.append(list(i))
    for j in users_by_name:
        if(i[1]!=request.GET.get('user')):
            users.append(list(j))

    old_request=None    
    if(is_logged(request)):
        old_request=slam_request.objects.raw(f'select * from slamer_slam_request where req_from ="{request.GET.get("user")}"')
    
    if not old_request == None:
        for arequest in old_request:
            for user in users:
                if(user[1] == arequest.req_to):
                    if(len(user) <= 3):
                        user.append('hidden')
                    else:
                        user[3]='hidden'
                else:
                    if(len(user) <= 3):
                        user.append('visible')
                    else:
                        user[3]='visible'

    context={
        'users':users,
        'logged':is_logged(request),
        'log_user':request.GET.get('user'),
        'old_request':old_request,
        'user_search':search_user,
    }
    
    return render(request,'user_search_res.html',context)

def pub_profile(request):
    if request.method == 'GET':
        username=str(request.GET.get('user'))
        try:
            profile=user.objects.get(username=username)
            context={
                'profile':profile,
            }
        except:
            context={
                'profile':''
            }
        return render(request,'pub_profile.html',context)
    else:
        return HttpResponse('Get not allowd here , please try again legitimately at /flogin !')

def is_logged(request):
    try:
        username=request.GET.get('user')
        if username == '' or username == None:
            try:
                username=request.POST['up_username']
            except:
                username=request.POST['username']
            else:
                pass
        username=user.objects.get(username=username)
        logged=abs_user.objects.get(uid=username)
    except:
        return False
    return logged.logged

def logout(request):
    out_user=request.POST['out_username']
    out_user=abs_user.objects.get(uid=out_user)
    out_user.logged=False
    out_user.save()
    return fetch_home(request)

def priv_profile(request):
    username=request.GET.get('user')
    if(is_logged(request)):
        my_info=user.objects.get(username=username)
        my_slams=slam_post.objects.raw(f'select * from slamer_slam_post where post_for="{username}"')
        request_forme=slam_request.objects.raw(f'select * from slamer_slam_request where req_to ="{username}"')
        context={
            'logged':is_logged(request),
            'log_user':username,
            'my_info':my_info,
            'request_forme':request_forme,
            'my_slams':my_slams,
        }
        return render(request,'priv_profile.html',context)
    else:
        return fetch_login(request)

def fetch_update_profile(request):
    if(is_logged(request)):
        username=request.POST['up_username']
        my_info_pub=user.objects.get(username=username)
        my_info_priv=abs_user.objects.get(uid=username)
        context={
            'logged':is_logged(request),
            'log_user':username,
            'my_info_pub':my_info_pub,
            'my_info_priv':my_info_priv,
        }
        return render(request,'update_profile.html',context)
    else:
        return fetch_login(request)

def update_profile(request):
    username=request.GET.get('user')
    if(is_logged(request)):
        name=request.POST['up_name']
        bio=request.POST['up_bio']
        key=request.POST['up_key']
        new_cred=user.objects.get(username=username)
        if name != '':
            new_cred.name=name
            new_cred.save()
        if bio != '':
            new_cred.bio=bio
            new_cred.save()
        if key !='':
            new_cred=abs_user.objects.get(uid=username)
            new_cred.key=key
            new_cred.save()
        context={
            'log_user':username,
            'logged':is_logged(request),
            }
        return priv_profile(request)
    else:
        return fetch_login(request)

def request_slam(request):
    if(is_logged(request)):
        try:
            check=slam_request.objects.get(req_from=request.GET.get('user'))
            if check.req_to == request.POST['req_for']:
                create_request=False
        except:
            create_request=True
        if (create_request):
            new_request=slam_request(req_from=request.GET.get('user'),req_to=request.POST['req_for'])
            new_request.save()
        return usearch(request)
    else:
        return fetch_login(request)

def fetch_slam_form(request):
    if(is_logged(request)):
        if request.method == 'POST':
            context={
                'logged':is_logged(request),
                'log_user':request.GET.get('user'),
                'post_for':request.POST['post_from'],
                'post_from':request.POST['post_for'],
            }
            return render(request,'slam_post.html',context)
    else:
        print('inside of else in slam page fetch !')
        return fetch_login(request)

def slam_poster(request):
    if(is_logged(request)):
        f1=request.POST['f1']
        f2=request.POST['f2']
        f3=request.POST['f3']
        f4=request.POST['f4']
        f5=request.POST['f5']
        f6=request.POST['f6']
        f7=request.POST['f7']
        f8=request.POST['f8']
        f9=request.POST['f9']
        f10=request.POST['f10']
        f11=request.POST['f11']
        f12=request.POST['f12']
        f13=request.POST['f13']
        f14=request.POST['f14']
        f15=request.POST['f15']
        f16=request.POST['f16']
        post_from=request.POST['post_from']
        post_for=request.POST['post_for']
        username=request.GET.get('user')
        delete_request=slam_request.objects.get(req_from=post_for,req_to=post_from)
        delete_request.delete()
        new_post=slam_post(post_from=post_from,post_for=post_for,public=False,f1=f1,f2=f2,f3=f3,f4=f4,f5=f5,f6=f6,f7=f7,f8=f8,f9=f9,f10=f10,f11=f11,f12=f12,f13=f13,f14=f14,f15=f15,f16=f16)
        new_post.save()
        return priv_profile(request)
    else:
        return fetch_login(request)

def fetch_slam(request):
    post_from=request.POST['post_from']
    post_for=request.POST['post_for']
    # if (is_logged(request) and request.method=='POST'):
    try:
        slam=slam_post.objects.get(post_from=post_from,post_for=post_for)
        if not slam.public and not is_logged(request):
            return fetch_login(request)
    except:
        slam=None
    context={
        'slam':slam,
        'log_user':post_for,
        'logged':is_logged(request),
    }
    return render(request,'slam.html',context)
    # else:
        # return fetch_login(request)

def pub_priv_toggle(request):
    if(is_logged(request) and request.method == 'POST'):
        post_from=request.POST['post_from']
        post_for=request.POST['post_for']
        slam=slam_post.objects.get(post_from=post_from,post_for=post_for)
        if slam.public :
            slam.public=False
        else:
            slam.public=True
        slam.save()
    return priv_profile(request)

def slam_delete(request):
    if(is_logged(request) and request.method=='POST'):
        post_id=request.POST['post_id']
        try:
            delete_slam=slam_post.objects.get(id=post_id)
            delete_slam.delete()
        except:
            pass
        return priv_profile(request)
    else:
        return fetch_login(request)
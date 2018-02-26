
from django.shortcuts import render, redirect
from .models import User, Project, Donation
from django.db.models import Sum, Avg
from datetime import date, time
# Create your views here.
def index(request):
    return render(request, 'FundHausII/index.html')

def register(request):
    #print request.POST
    if request.method == 'POST':
        messages = User.objects.register(request.POST)
        #Above line might be postData
    if not messages:
        print "No messages! Success!"
        # fetch user id and name via email
        user_list = User.objects.all().filter(email=request.POST['email'])
        request.session['id'] = user_list[0].id
        request.session['first_name'] = str(user_list[0].firstName)
        request.session['last_name'] = str(user_list[0].lastName)
        request.session['name'] = str(user_list[0].firstName) +  " " + str(user_list[0].lastName)
        return redirect('/allusers')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/signup')

def login(request):
    users = User.objects.all()
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password'],
    }
    if request.method == 'POST':
        messages = User.objects.login(request.POST)
    if not messages:
        print "No messages! Success!"
        user_list = User.objects.all().filter(email=request.POST['email'])
        request.session['id'] = user_list[0].id
        request.session['first_name'] = str(user_list[0].firstName)
        request.session['last_name'] = str(user_list[0].lastName)
        request.session['name'] = str(user_list[0].firstName) +  " " + str(user_list[0].lastName)
        return redirect('/projects')
    else:
        request.session['messages'] = messages
        return redirect('/')

def signin(request):
    return render(request, 'FundHausII/signIn.html')

def signup(request):
    return render(request, 'FundHausII/signUp.html')

def allusers(request):
    users = User.objects.all()
    context={
        'users': users
    }
    return render(request, 'fundHausII/allusers.html', context)

def newproject(request):
    #print request.POST
    first_name = request.session['first_name']
    print "First Name: {}",format(first_name)
    name = request.session['name']
    currentuser = request.session['name']
    print currentuser
    if request.method == 'POST':
        print request.POST
        messages = Project.objects.createproject(request.POST, first_name)
        #Above Line Might Be Post postData
    if not messages:
        print "No messages! Success!"
        #fetch project id and name using title
        projectList = Project.objects.all().filter(title=request.POST['title'])
        request.session['project_id'] = projectList[0].id
        return redirect('/projects')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/projects')

def project(request, id):
    user_id = request.session['id']
    print "User ID: {}".format(user_id) 
    project_id = id
    print "Project ID: {}".format(id)
    name = request.session['name']
    print "{} is the name I Want to print!".format(name)
    users = User.objects.all()
    print "Users: {}".format(users)
    # user_pic_id = Project.objects.get(project_donated__id=id)
    # print "User Pic ID: {}".format(user_pic_id)
    currentuser = User.objects.all().filter(id=request.session['id'])
    print "Current User: {}".format(currentuser)
    # userdonations = User.objects.donations.all().filter(gte=1)
    # donations = Project.objects.donations.all().filter(id=id)
    project = Project.objects.get(id=id)
    print "Project: {}".format(project)
    donations = Donation.objects.filter(campaign_id=id)
    print "Donations: {}".format(donations)
    donations_count = donations.count()
    print "Donations Count: {}".format(donations_count)
    donations_sum = Donation.objects.all().filter(campaign__id=id).aggregate(Sum('amount'))['amount__sum']
    print "Donation Sum: {}".format(donations_sum)
    if not donations_sum:
        donations_sum = 0
    percentage = (float(donations_sum) / project.goal) * 100
    print "Percentage: {}".format(percentage)
    funded_message = []
    if percentage >= 100:
        funded_message.append("Conratulations! Your Project Is Officially Funded" )
        print "Funded Message: {}".format(funded_message)    
    # project_id = project.id
    # print "Projects: {}".format(projects)
    # project_id = project.id
    # print "Project ID: {}".format(project_id)
    context={
        'donations': donations,
        'donations_count': donations_count,
        'donations_sum': donations_sum,
        'funded_message': funded_message,
        'project': project,
        'project_id': project_id,
        'percentage': percentage,
        # 'userdonations': userdonations,
        # 'user': user,
        'users': users,
        'id': id
    }
    return render(request, 'fundHausII/project.html', context)

def projects(request):
    name = request.session['name']
    print "Name: {}".format(name)
    # first_name = request.session['first_name']
    # print "First Name: {}".format(first_name)
    # last_name = request.session['last_name']
    # print "Last Name: {}".format(last_name)
    projects = Project.objects.all()
    # project_id = id
    # print "Project ID: ".format(project_id)
    users = User.objects.all()
    context={
        'projects': projects,
        'users': users, 
        'name': name,
        # 'first_name': first_name,
        # 'last_name': last_name
    }
    return render(request, 'fundHausII/projects.html', context)

def donate(request, id):
    if request.method == 'POST':
       return newdonation(request, id)
    user_id = request.session['id']
    print "User ID: {}".format(user_id) 
    project_id = id
    print "Project ID: {}".format(id)
    project = Project.objects.all().filter(id=id)
    print "Project: {}".format(project)
    context={
        'project': project,
        'project_id': project_id,
        'user_id': user_id
    }
    return render(request, 'fundHausII/donate.html', context)

def newdonation(request, id):
    user_id = int(request.session['id'])
    print "User ID: {}".format(user_id)
    project_id = id
    print "Project ID: {}".format(project_id)
    # current_project = Project.objects.get(id=project_id)
    # print "Current Project: {}".format(current_project)
    name = request.session['name']
    print "Name: {}".format(name)
    # first_name = request.session['first_name']
    # print "First Name: {}".format(first_name)
    # last_name = request.session['last_name']
    # print "Last Name: {}".format(last_name)
    users = User.objects.all()
    print "Users: {}".format(users)
    all_donations = Donation.objects.all()
    if request.method == 'POST':
        messages = Donation.objects.donate(request.POST, user_id, project_id)
    if not messages:
        print "No Errors! Success!"
        donor = name
        current_donation = request.POST['donation']
        print "Current Donation is: {}".format(current_donation)
        context = {
            # 'donations_list': donations_list,
            'name': name,
            'project_id': project_id,
            'users': users,
            'all_donations': all_donations,
            'donor': donor,
            'all_donations:': all_donations,
            'user_id': user_id
        }
        return redirect('/projects', context)
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/projects')

def trending(request):
    projects = Project.objects.all()
    trending_projects = Project.objects.all().order_by('-created_at')
    context={
        'trending_projects': trending_projects,
        'projects': projects,
    }
    return render(request, 'fundHausII/trending.html', context)

def createproject(request):
    name = request.session['name']
    print "Name: {}".format(name)
    first_name = request.session['first_name']
    print "First Name: {}".format(first_name)
    last_name = request.session['last_name']
    print "Last Name: {}".format(last_name)
    print "{} is the Logged In user".format(name)
    context={
        'name': name,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'fundHausII/createProject.html', context)

def user(request, user_id):
    projects_donated_to = Project.objects.all().filter(project_donated__id=user_id)
    print "Projects Donated To: {}".format(projects_donated_to)
    user = User.objects.get(id=user_id)
    print "User: {}".format(user)
    user_donations = Donation.objects.all().filter(donor_id=user_id)
    print "User Donations: {}".format(user_donations)
    users = User.objects.all()
    # print "Users: {}".format(users)
    context = {
        'user': user,
        'users': users,
        'user_donations': user_donations,
        'projects_donated_to': projects_donated_to
    }
    return render(request, 'fundHausII/user.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')


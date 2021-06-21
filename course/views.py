import course
from django.shortcuts import render,redirect
from .models import Contact,Profile,Class, Student_class, Questions,Answers, VoteForAnswer, Short_question,Short_answered_by
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from .forms import SignUpForm,ProfileForm,ImageForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
#from django.db.models import Q
from django.db.models import Sum
from datetime import datetime
from django.utils.crypto import get_random_string

@login_required
def edit_profile(request):
    current_user = request.user 
    user_profile = Profile.objects.get(user_id=current_user)
    
    
    if request.method=='POST' and 'btnform1' in request.POST:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid(): 
            profile = Profile.objects.get(user_id=request.user)
            profile.profile_image = form.cleaned_data['profile_image']
            profile.save()
            return redirect('/edit_profile') 

    
    if request.method=='POST' and 'btnform2' in request.POST:
        pass
    else: 
        image_form = ImageForm()
    
    return render(request, 'course/edit_profile.html', {'user_profile': user_profile, 'image_form': image_form})


def index(request):   
    return render(request, 'course/home.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('fname','') + " " + request.POST.get('lname','')
        email = request.POST.get('email', '')
        desc = request.POST.get('description', '')
        phone = request.POST.get('mobile', '')
        cont = Contact(name=name,description=desc,email=email,phone=phone)
        cont.save()
    return render(request, 'course/contact.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            u = User.objects.get(username=username)
            u1 = Profile.objects.get(user=u)
            if request.user.is_superuser or u1.user_type == 'Admin':
                return redirect('/admin')
            if u1.user_type == 'Customer':
                return redirect('/')
            else:
                return redirect('/')

    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'course/signup.html', {'form': form , 'profile_form': profile_form})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        u = User.objects.get(username=username)
        u1 = Profile.objects.get(user=u)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.user.is_superuser or u1.user_type == 'Admin':
                   return redirect('/admin')
                if u1.user_type == 'Customer':
                    return redirect('/')
                if u1.user_type == 'Permitted_Employee':
                    return redirect('/emp_home')
                else:
                    return redirect('/')

            else:
                messages.error(request, 'Your account has been disabled..!')
                return render(request, 'course/login.html')
        else:
            messages.error(request, 'Invalid login..!')
            return render(request, 'course/login.html')
    else:
        return render(request, 'course/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        u = User.objects.get(email=email)
        u.set_password(password)
        u.save()
        return redirect('/login')
    else:
        return render(request,'course/change_password.html')

def thank(request):
    return render(request,'course/thank.html')

@login_required
def create_class(request):
    current_user = request.user
    
    if request.method == "POST":
        course_code = request.POST.get('course_code', '')
        course_title = request.POST.get('course_title', '')
        course_credit = request.POST.get('course_credit','0.0')
        section = request.POST.get('section', '')
        
        code = get_random_string(length=8)
        while Class.objects.filter(code=code).exists():
            code = get_random_string(length=8)
        
        class1 = Class(course_code=course_code, course_title=course_title, course_credit=course_credit,
                       section=section, teacher=current_user, code = code)
        class1.save()
        return render(request, 'course/my_class.html')
    return render(request, 'course/create_class.html')

@login_required
def join_class(request):
    current_user = request.user
    if request.method == "POST":
        code = request.POST.get('code', '')
        if Class.objects.filter(code=code).exists():
            course_id = Class.objects.get(code=code)
            if Student_class.objects.filter(student = current_user,course_id = course_id).exists():
                return render(request, 'course/join_class.html')
                 
            else:
                student1 = Student_class(student = current_user, course_id = course_id)
                student1.save()
                return render(request, 'course/home.html')
    return render(request, 'course/join_class.html')



@login_required
def my_class(request):
    current_user = request.user
    joined_class = Student_class.objects.filter(student=current_user).order_by('-id')
    all_class = Class.objects.all()
    user = User.objects.all()
    created_class = Class.objects.filter(teacher=current_user).order_by('-id')
    image = Profile.objects.get(user_id=current_user)
    profiles = Profile.objects.all()
    if created_class.exists():
        c=1
    else:
        c=0

    if joined_class.exists():
        j=1
    else:
        j=0

    params = {'created_class': created_class, 'teacher_name': current_user, 'image': image, 'all_class': all_class,
    'user': user, 'joined_class': joined_class, 'profiles': profiles, "c":c, 'join': j }    
    return render(request, 'course/my_class.html', params)
@login_required
def enter_class(request, course):
    current_user = request.user 
    cour = Class.objects.get(id = course)
    request.session['selected_course_id'] = course
    request.session['selected_course_title'] = cour.course_code + " " + cour.course_title
    #time = datetime.now() 
    c = Class.objects.filter(id = course)
    for i in c:
        teacher = i.teacher
    if teacher==current_user:
        s = 0
    else:
        s = 1

    question = Questions.objects.filter(status = "Pending", course_id = course).order_by('-id')
    return render(request, 'course/class_home.html', {'question': question, 's': s })
@login_required
def ask_question(request):
    current_user = request.user
    course_id = request.session.get('selected_course_id')
    if request.method == "POST":
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        mark = request.POST.get('mark', '')
        course = Class.objects.get(id = course_id)
        ques = Questions(question = question, asked_by = current_user, status = "Pending", course = course, marks=mark)
        ques.save()
        if answer != '':
            ans = Answers(answer = answer, answered_by = current_user, question_id = ques )
            ans.save()
        stu_cls = Student_class.objects.filter(student = current_user, course_id = course )
        for j in stu_cls:
            # j.marks += float(mark)
            j.asked_ques += 1 
            j.save()
        return redirect('/my_question')
    return render(request, 'course/ask_question.html')
@login_required
def answers(request, question_id):
    current_user = request.user
    course_id = request.session.get('selected_course_id')
    question = Questions.objects.filter(id = question_id)
    course = Class.objects.get(id = course_id)
    answers = Answers.objects.filter(question_id = question_id).order_by('-time')
    my_ans = Answers.objects.filter(question_id = question_id, answered_by = current_user)
    if my_ans.exists():
        my_ans1 = True
    n = answers.count()
    if request.method == "POST" and 'btnAns' in request.POST:
        answer = request.POST.get('answer', '')
        ans = Answers(answer = answer, answered_by = current_user, question_id_id = question_id, status = 'Not marked' )
        ans.save()
        j = Student_class.objects.get(student = current_user, course_id = course )
        j.answered_ques += 1
        j.save
    voteForAnswer = VoteForAnswer.objects.filter(voter = current_user)
    if not voteForAnswer.exists():
        voteForAnswer = 1
    context = {'voteForAnswer': voteForAnswer,'my_ans': my_ans, 'm': my_ans1, 'question': question, 'answers': answers, 'question_id': question_id, 'n': n}
    return render(request, 'course/reply.html',context)
@login_required
def reply(request):
    return render(request, 'course/reply.html')
@login_required
def test(request):
    return render(request, 'course/ab.html')

@login_required
def unmarked_answers(request, question_id):
    
    question = Questions.objects.filter(id = question_id)
    answers = Answers.objects.filter(question_id = question_id, status = 'Not marked').order_by('-time')
   # n = answers.count()
    if request.method == "POST":
        ans = request.POST.get('ans', '')
        #ans = int(ans)
        mark = request.POST.get('mark', '')
        a = Answers.objects.filter(id=ans)
        for i in a:
            i.marks = mark
            i.status = 'Marked'
            i.save()
            answered_by = i.answered_by
            course_id = ''
            for q in question:
               course_id = q.course_id
            stu_cls = Student_class.objects.filter(student = answered_by, course_id = course_id )
            for j in stu_cls:
               j.marks += float(mark)
               #j.answered_ques += 1 
               j.save()
    context = {'question': question, 'answers': answers}
    return render(request, 'course/unmarked_answers.html',context)

@login_required
def dashboard(request):
   course_id = request.session.get('selected_course_id')
   stu_cls = Student_class.objects.filter(course_id = course_id ).order_by('-marks')
   context = {'students' : stu_cls}
   return render(request, 'course/dashboard.html', context) 

@login_required
def my_question(request):
    course_id = request.session.get('selected_course_id')
    question = Questions.objects.filter(asked_by = request.user, course_id = course_id).order_by('-id')
    n = question.count()
    if request.method == "POST":
        question_id = request.POST.get('question_id', '')
        text = request.POST.get('question', '')
        q = Questions.objects.get(id = question_id )
        q.question = text
        q.save()
    context = {'question': question, 'n': n}
    return render(request, 'course/my_question.html', context)

@login_required
def my_answer(request):
    answer = Answers.objects.filter(answered_by_id = 13).order_by('-id')
    n = answer.count()
    if request.method == "POST":
        answer_id = request.POST.get('answer_id', '')
        text = request.POST.get('answer', '')
        q = Answers.objects.get(id = answer_id )
        q.answer = text
        q.save()
    context = {'answers': answer, 'n': n }
    return render(request, 'course/my_answer.html', context)

@login_required
def delete(request, question_id):
    query = Questions.objects.get(id=question_id)
    query.delete()
    return redirect('/my_question')

@login_required
def delete_answer(request, answer_id):
    query = Answers.objects.get(id=answer_id)
    query.delete()
    return redirect('/my_answer')

@login_required
def vote(request, answers_id):
    query = Answers.objects.get(id=answers_id)
    std = Student_class.objects.get(student = query.answered_by)
    a = VoteForAnswer.objects.filter(voter = request.user, answer = query )
    if a.exists():
        a.delete()
        query.vote -= 1
        query.save()
        std.point -= 2
        std.save()
    else:
        query.vote += 1
        query.save()
        b = VoteForAnswer(voter = request.user, answer = query)
        b.save()
        std.point += 2
        std.save()
    return redirect('/answers/%d'%query.question_id.id)

@login_required
def ask_short_question(request):
    current_user = request.user
    course_id = request.session.get('selected_course_id')
    if request.method == "POST":
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        answer = answer.lower()
        course = Class.objects.get(id = course_id)
        ques = Short_question(question = question, asked_by = current_user, status = "Approved", course = course, answer=answer)
        ques.save()
       
        stu_cls = Student_class.objects.filter(student = current_user, course_id = course )
        for j in stu_cls:
            # j.marks += float(mark)
            j.asked_ques += 1 
            j.save()
        return redirect('/my_question')
    return render(request, 'course/ask_short_question.html')

@login_required
def short_questions(request):
    course_id = request.session.get('selected_course_id')
    course = Class.objects.get(id = course_id)
    j = Student_class.objects.get(student = request.user, course_id = course )
    short_answer_by = Short_answered_by.objects.filter(answered_by = request.user)  
    if request.method == "POST":
        question = request.POST.get('question', '')
        ques = Short_question.objects.get(id = question)
        ans = request.POST.get('ans', '')
        answer = request.POST.get('answer', '')
        answer = answer.lower()
        a = Short_answered_by.objects.filter(answered_by = request.user, question = ques)
        if(a.exists()):
            messages.info(request, "You have already answered.")
        else: 
            sab = Short_answered_by(answered_by = request.user, question = ques, answer = answer)
            sab.save()
            if(ans == answer):
                j.answered_ques += 1
                j.marks += 1 
                j.save
                messages.info(request, "Correct!")
            else:
                messages.info(request, "Incorrect answer.")

            
        
        return redirect('/short_questions')
        
    course = request.session.get('selected_course_id')
    question = Short_question.objects.filter(status = "Approved", course_id = course).order_by('-id')
    context = {'question': question, 'answered_by': short_answer_by}
    return render(request, 'course/short_questions.html', context)

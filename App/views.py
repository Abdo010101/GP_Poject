from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate ,login ,logout


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
# Create your views here

tfvect = TfidfVectorizer(stop_words='english', max_df=0.7)
loaded_model = pickle.load(open('model.pkl', 'rb'))
dataframe = pd.read_csv('news.csv')
x = dataframe['text']
y = dataframe['label']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)




def fake_news_det(news):
    tfid_x_train = tfvect.fit_transform(x_train)
    tfid_x_test = tfvect.transform(x_test)
    input_data = [news]
    vectorized_input_data = tfvect.transform(input_data)
    prediction = loaded_model.predict(vectorized_input_data)
    return prediction


def predict(request):
    if request.method == 'POST':
        message = request.POST['message']
        pred = fake_news_det(message)
        print(pred)
        context={'pred':pred}
        return render(request,'index.html', context)
    else:
        return render(request,'index.html', context)


def registerPage(request):
    form = CreateUserForm()
    # check the data valdiation 
    if request.method == "POST":
        #if the is Post mehtod throw this data inot htis form 
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request ,'Account was created for ' + user )
            return redirect('loginPage')

    context = {'form': form}
    return render(request , 'register.html' ,context)

def loginPage(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username , password = password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request ,'Username OR Passwrod is incorrect')

        
    return render(request , 'login.html')    

def logoutPage(request):
    logout(request)
    return redirect('login') 



def index(request):
    return render(request ,'index.html')

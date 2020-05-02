from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=715884204ca593faf87c4668a84634dc'
    cities=City.objects.all()
    err_msg=''
    message=''
    message_class=''
    weather_data=[]
    print(request.META)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip=''
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    if request.method == 'POST':
        form=CityForm(request.POST)
        if form .is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if(existing_city_count == 0):
                res=requests.get(url.format(new_city)).json()
                if(res['cod'] == 200):
                    form.save()
                else:
                    err_msg="Invalid city"
            else:
                pass
        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='Search Result'
            message_class='is-success'
        if err_msg:
            for city in cities:
                res=requests.get(url.format(city)).json()
                city_weather={
                    'city':city.name,
                    'temperature':res['main']['temp'],
                    'description':res['weather'][0]['description'],
                    'icon':res['weather'][0]['icon']
                }
                weather_data.append(city_weather)
        

        else:
            city_weather={
                'city':new_city,
                'temperature':res['main']['temp'],
                'description':res['weather'][0]['description'],
                'icon':res['weather'][0]['icon']
            }
            weather_data.append(city_weather)
        context={'weather_data' : weather_data,'form':form,'message':message,'message_class':message_class} 


        return render(request,'weather/weather.html',context)

    form =CityForm()
   
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather={
            'city':city.name,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'icon':res['weather'][0]['icon']
        }
        weather_data.append(city_weather)
    context={'weather_data' : weather_data,'form':form,'message':message,'message_class':message_class} 


    return render(request,'weather/weather.html',context)

def Covid(request):
    url='https://api.covid19api.com/summary'
    res=requests.get(url).json()
    results=res['Countries']
    covid_res=[]
    TotalConfirmed=0
    TotalDeath=0
    TotalActiveCase=0
    for result in results:
        if result['Country']:
            TotalActiveCase+=int(result['TotalConfirmed']) - int(result['TotalRecovered'])
            TotalConfirmed+=result['TotalConfirmed']
            TotalDeath+=result['TotalDeaths']
            covid_dict={
                'Country':result['Country'],
                'Confirmed':result['TotalConfirmed'],
                'NewConfirmed':result['NewConfirmed'],
                'Deaths':result['TotalDeaths'],
                'NewDeaths':result['NewDeaths'],
                'Recovered':result['TotalRecovered'],
                'ActiveCase':int(result['TotalConfirmed']) - int(result['TotalRecovered'])
            }
            covid_res.append(covid_dict)
    covid_res.sort(key=lambda x:x['Confirmed'],reverse=True)
    context={'covid_data':covid_res,'TotalConfirmed':TotalConfirmed,'TotalDeath':TotalDeath,'TotalActiveCase':TotalActiveCase}
    return render(request,'weather/Covid.html',context)

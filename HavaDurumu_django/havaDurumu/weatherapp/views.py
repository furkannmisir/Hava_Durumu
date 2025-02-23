from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import os

def home(request):
    # Kullanıcının girdiği şehir bilgisi (Varsayılan: Indore)
    city = request.POST.get('Sehir', 'Antalya')

    # API Anahtarları (Senin sağladığın Google API key kullanıldı)
    WEATHER_API_KEY = 'kendi apin'  # OpenWeatherMap test API anahtarı
    GOOGLE_API_KEY = 'kendi apin'  # Google API anahtarı (Daha sonra güvenli hale getir)
    SEARCH_ENGINE_ID = 'kendi apin'  # Google Custom Search Engine ID

    # OpenWeatherMap API URL
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'

    # Google Custom Search API URL (Şehir görseli için)
    query = f"{city} 1920x1080"
    search_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&imgSize=xlarge"

    # Başlangıç değerleri
    weather_data = None
    image_url = None
    exception_occurred = False

    # Hava durumu verisini çekme
    try:
        response = requests.get(weather_url)
        weather_data = response.json()

        if weather_data.get('cod') != 200:
            raise KeyError("API'den geçerli veri alınamadı.")

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()
    except (requests.exceptions.RequestException, KeyError):
        exception_occurred = True
        messages.error(request, "Hava durumu bilgisi alınamadı, lütfen tekrar deneyin.")
        description = "Hava Temiz "
        icon = "01d"
        temp = 25
        day = datetime.date.today()

    try:
        response = requests.get(search_url)
        image_data = response.json()
        search_items = image_data.get("items", [])

        if search_items:
            image_url = search_items[0]['link']
        else:
            messages.warning(request, "Şehir için görsel bulunamadı.")

    except requests.exceptions.RequestException:
        messages.warning(request, "Görsel arama başarısız oldu.")

    # Template'e verileri gönderme
    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'exception_occurred': exception_occurred,
        'image_url': image_url
    })

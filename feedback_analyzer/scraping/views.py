from django.shortcuts import render
from .forms import ScrapingParamsForm
from .models import ScrapingParams

def scraping_params(request):
    if request.method == 'POST':
        form = ScrapingParamsForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ScrapingParamsForm()

    return render(request, 'scraping/scraping_params.html', {'form': form})

def process_scraping_params(request):
    if request.method == 'GET':
        all_params = ScrapingParams.objects.all()
        return render(request, 'scraping/scraping_results.html', {'results': results})

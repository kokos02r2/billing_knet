from django.http import HttpResponse

# # Главная страница
# def index(request):    
#     return HttpResponse('Главная страница')


# Страница со списком мороженого
def abonents(request):
    return HttpResponse('Список абонентов')


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def abonent_detail(request, pk):
    return HttpResponse(f'Абонент договор № {pk}')

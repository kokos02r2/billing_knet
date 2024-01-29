from django.http import HttpResponse

# # Главная страница
# def index(request):    
#     return HttpResponse('Главная страница')


# Страница со списком мороженого
def groups(request):
    return HttpResponse('Список групп')


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def group_detail(request, pk):
    return HttpResponse(f'Группа {pk}')

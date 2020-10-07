from datetime import datetime


def base_main(request):
    now = datetime.now()
    copyright_year = now.year

    context = {
        'copyright_year': copyright_year,
    }
    return context

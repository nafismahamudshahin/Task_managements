from django.shortcuts import render , HttpResponse
from django.views import View
# Create your views here.

class Gretting(View):
    gretting = "hello everyone"

    def get(self,request):
        return HttpResponse(self.gretting)
    
# overwriting:
class HiGreeting(Gretting):
    gretting = "Hi greeting how are you"
from django.shortcuts import render
import pprint
from Internal.oneAmazon import main
import pandas as pd
# import TextMiddleware
# from django.shortcuts import process_response

# Create your views here.

from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'asins/index.html')

def search_form(request):
    return render(request, 'asins/search_form.html')

def search(request):

    # return render()
    # df = main('B00607B6VO')
    # return .to_html(classes="table striped")
    # df = pd.DataFrame() 
    # df['special_col_1'] = pd.Series([0,0,0,1,1,1])
    # df['special_col_2'] = pd.Series([0,1,2,0,1,2])
    # context ={
    # 'df': df.to_html(),
    #'df': '<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>special_col_1</th> <th>special_col_2</th> </tr> </thead> <tbody> <tr> <th>0</th> <td>0</td> <td>0</td> </tr> <tr> <th>1</th> <td>0</td> <td>1</td> </tr> <tr> <th>2</th> <td>0</td> <td>2</td> </tr> <tr> <th>3</th> <td>1</td> <td>0</td> </tr> <tr> <th>4</th> <td>1</td> <td>1</td> </tr> <tr> <th>5</th> <td>1</td> <td>2</td> </tr> </tbody> </table>'
    # }
    # return TextMiddleware.process_template_response(request,'asins/res2html.html',context)
    #return render(request,'asins/res2html.html',context)
    if 'q' in request.GET and request.GET['q'] is not None:
        return HttpResponse(main(request.GET['q']))
    else:
        return HttpResponse('wrong input')
    # return HttpResponse(df.to_html())

    # return 
    # return HttpResponse(df.to_html(classes="table striped"))
    # if 'q' in request.GET:
    #     message = 'You searched for: %r' % request.GET['q']
    # else:
    #     message = 'You submitted an empty form.'
    # return HttpResponse(message)
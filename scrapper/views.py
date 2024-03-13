from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.template import loader 


def scrapping_data(request):
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        url_data = f'https://online.autobrand.ro/csp/berta/portal/Artikel.csp?CSPToken={product_code}'
        get_data = requests.get(url_data)
        if get_data.status_code ==200:
            soup = BeautifulSoup(get_data.text, 'html.parser')
            # print(soup)
            product_name = soup.find("td", class_="properties-value").text.strip
            price = soup.find("td", class_="numeric preis15").text.strip
            provider = soup.find("td", class_="properties-value").text.strip
       

            data = {
                'Name': product_name,
                'Price': price,
                'Provider': provider
            }
            df = pd.DataFrame(data)
            excel_doc = f'{product_name}.xlsx'
            df.to_excel(excel_doc, index=False)

            with open(excel_doc, 'rb') as f:
                response = HttpResponse(f.read())
            
            return response
        else:
            return HttpResponse("Produsul nu a fost gasit")
    else:
        return render(request, template_name='download_data.html')
        



    
from django.shortcuts import render
import requests
import pandas as pd

def home(request):
    return render(request, 'dashboard/home.html')

def dashboard(request):
    # calling it's own api to avoid repeating of code
    response = requests.get('http://localhost:8000/compounds/')
    # converting data to normalised json so that assay results can be added to dataframe
    json_data = response.json()
    df = pd.json_normalize(json_data, record_path='assay_results', meta=['compound_id', 'smiles', 'molecular_weight' , 'a_log_p', 'molecular_formula', 'num_rings', 'image'], errors='ignore')

    df.to_csv('compounds.csv', index=False)
    from . import dashboard

    context = {'data': json_data}
    return render(request, 'dashboard/dashboard.html', context)

def getImgData(img):
    with open(img, "rb") as f:
        data = f.read()
    return data

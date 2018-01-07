FlaskAPI-for-PowerBI

A simple Python based Flask API for embedding PowerBI in web application. 
The API currently uses SQL SERVER. You may use it for any other database. 
Please follow the steps below to use the api. 

	1.Client application sends a request to the Flask API.
	2.API sends back the reportid and embeddedtoken which will be used by powerbi.js file for report embedding.
	3.Client sends the data based on which the current dataset will change and report will be generated. 

	
Simple Django Based View as a Client :

	def bidemo(request):
	r=requests.post('http://127.0.0.1:5000/token', data = {'key1':'sendToken'})
	a=json.loads(str(r.text))
	selectedReport=a['selectedReport']
	embedToken=a['embedToken']
	if request.method == 'POST':
		form=UserForm(request.POST)        
		if form.is_valid():
			dist=request.POST.get('distributor','')
			r=requests.post('http://127.0.0.1:5000/api', data = {'key2':dist})
			print r.text
	else:
		form=UserForm()
	return render(request, 'registration/bidemo.html', {'form':form,'selectedReport': selectedReport,
						
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode
from django.template.loader import get_template
from django.template import Context, Template
import json
from collections import Counter

def clean_node(node,addr,html):

	flag = 0
	#flag used to differentiate between parent node and leaf node in template
	title_list= []
	slug_list= []
	# lists store value of title and slug respectively in the for loop below
	title= node['title']
	if node['slug']==addr:
		if node['kind'] == 'Topic':
			flag =1
			# if value of kind is topic , flag is set to 1
			k= len(node['children'])		
				
			for i in range(0,k): 
				
				title_val=node['children'][i]['title']
				#title value of child node
				x= smart_str(title_val)
				#title value was in unicode type, which is converted to string
				title_list.append(x)
				# the string value is added to the list
	   			slug_val = node['children'][i]['slug']
				#slug value of child node
				y = str(slug_val)
				#slug value was in unicode type, which is converted to string
				slug_list.append(y)
				# the string value is added to the list

			t = get_template('project.html')
			#returns the compiled template project.html
			zipde= zip(title_list,slug_list)
			#zip function used to combine two lists, so that they can be traversed parallely in temeplate using for loop
			html = t.render(Context({'title': title,'title_list':title_list,'slug_list':slug_list, 'k':k , 'flag':flag, 'zipde':zipde}))
			return html	
			
		else:
			flag = 0
			content_val = node['content']
			#template loading
	   		t = get_template('project.html')
			html = t.render(Context({'title': title,'content_val':content_val,'slug':node['slug']}))
			return html
			
	else:   
        
		if node['kind'] == 'Topic':		
			for child in node['children']:
				html = clean_node(child,addr,html)
					     
		
	return html
	
#function to create dynamic urls in urls.py
def dynamic(node,a):


	
	c= "'}  ),"
	d= "/$', load ,{'addr' : '"

	a += node['slug']
	prev=a
	a +=d
	a += node['slug']
	a +=c

	if node['kind'] == 'Topic':	
		for i in node['children'] :                                                                     
			dynamic(i,prev+"/") 	
			
	#after adding urls to "a", the value of a is written in urls.py file
	with open("../tree/tree/urls.py", "a") as myfile:
    		myfile.write(a+"\n")	



#function to be called first for generating the dynamic urls
#after calling this function a message will be shown on screen "URL Generated"
def gen_url(request):
	json1_file = open('json1.json')    
     	json1_str = json1_file.read()
     	json1_data = json.loads(json1_str) 		
	#json1_data is the final format of data in python dictionary form
	fo = open("../tree/tree/urls.py", "r")
	fo.seek(-5,2)
	if fo.read(5)=="#Done":
		return HttpResponse("URL Already Generated")
	#the if condition is to check whether urls are already generated in urls.py file

	with open("../tree/tree/urls.py", "a") as myfile:
   		myfile.write("urlpatterns += patterns('',\n")

	dynamic(json1_data,"url(r'^")	

	with open("../tree/tree/urls.py", "a") as myfile:
   		myfile.write(")\n#Done")	

	return HttpResponse("URL Generated")

# load function opens the json file
def load(request,addr):
	html=" "
	json1_file = open('json1.json')    
     	json1_str = json1_file.read()
     	json1_data = json.loads(json1_str)
	#json data is converted to dictionary format
	html= clean_node(json1_data,addr,html)
	#clean node is called and dictionary format of data is passed for further processing
	return HttpResponse(html)	

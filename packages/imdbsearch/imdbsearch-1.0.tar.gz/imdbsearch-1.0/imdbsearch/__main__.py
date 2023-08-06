# IMPORTS
from bs4 import BeautifulSoup
import requests
import urllib.parse
from datetime import date
import json


def main():

	actordict = {}

	# make sure actor name exists
	descending = 'n'
	actorinfo = 0
	while actorinfo == 0:
		inputname = input("Please enter actor\'s name: ")
		actorinfo = getactorinfo(inputname)
	
	descending = input("List sorted in descending order? (y/n): ")

	print("\nDisplaying movies from{}".format(actorinfo.get_text()))

	# store all actor information into dictionary
	actordict['ActorName'] = actorinfo.get_text().split('(')[0][1:-1]
	actordict['KnownFor'] = actorinfo.get_text().split(',')[1][1:-1]

	actordict['Movies'] = getactormovies(actorinfo, descending)

	if input("\nExport to JSON file? (y/n): ") == 'y':
		exporttoJSON(actordict)
	


def exporttoJSON(actordict): 
	filename = '{}.json'.format(actordict['ActorName'].replace(' ','_'))
	with open(filename, 'w') as outfile:
		json.dump(actordict, outfile)
	
	print("Exported as {}!".format(filename))
	#TODO CLOSE FILE

def getactormovies(actor, order): 
	
	actorcode = actor.find('a')['href']
	#href for actor's profile page comes in format /name/actorcode/ want to extract actorcode
	actorcode = actorcode.split('/')[2]

	# default sort is ascending order, sorts in descending if user requests
	if(order == 'y'):
		order = ''
	else:
		order = ',asc'

	# querying page listing all movies from a particular actor
	# will only display movies that have already been released
	moviepage = requests.get(
		"https://www.imdb.com/search/title/?title_type=movie&role={}&mode=simple&sort=year{}&job_type=actor&release_date=%2C{}&count=250"
		.format(actorcode, order, date.today().year))

	# use beautiful soup to parse document
	soup = BeautifulSoup(moviepage.content, 'html.parser')

	movies = []
	# find each movie and print out their year and name 
	movielist = soup.find_all(class_="lister-item-content")
	for movie in movielist:
		try:
			moviename = movie.find('a').text
			movieyear = movie.find(class_="lister-item-year").text
			print("{} {}".format(movieyear, moviename))

			# put info into dictionary to later output in JSON
			
			movies.append({
				'name': moviename,
				'year': movieyear
			})

		except AttributeError:
			print("No movies exist")
	
	return movies


def getactorinfo(inputname): 
	
	# get html contents of page when actors of exact name `actorname` is searched on imdb
	inputname = urllib.parse.quote(inputname)
	imdbpage = requests.get("https://www.imdb.com/find?q=" + inputname + "&s=nm&exact=true")

	# use beautiful soup to parse document
	soup = BeautifulSoup(imdbpage.content, 'html.parser')

	# find each actor and their unique description
	actorinfo = soup.find_all(class_='result_text')
	
	if len(actorinfo) == 0: 
		print("No actors named " + inputname)
		return 0
	if len(actorinfo) == 1:
		# there is only 1 actor in search result
		return actorinfo[0]
	else: 
		# multiple actors in search result
		# allow user to select an actor based on avalailable information
		print("\nWhich actor did you mean? Please insert number\n")
		currdisplayed = 0
		num = ''
		numtodisplay = 5
		
		# display only 5 actors at a time, allow user to scroll
		while currdisplayed < len(actorinfo) and not num: 
			
			for i in range(numtodisplay):
				print("{}. {}".format(currdisplayed+i+1, actorinfo[currdisplayed+i].get_text()))

			currdisplayed+=numtodisplay
			
			#check if user has scrolled through entire list
			if currdisplayed > len(actorinfo)-numtodisplay:
				numtodisplay= len(actorinfo)%numtodisplay
			
			if currdisplayed < len(actorinfo):
				# TODO: REMOVE THIS LINE WHEN LOOPED AGAIN
				print("press `enter` to see more...")

			num = input()
		
		#make sure input is an integer
		while not num:
			print("Please insert integer")
			num = input()
			

		return  actorinfo[int(num)-1]



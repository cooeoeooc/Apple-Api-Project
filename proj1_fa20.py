#########################################
##### Name:                         Zekun Zhao
##### Uniqname:                     zzekun
#########################################
import json
import webbrowser
import requests


#from requests.models import Response



class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year",url="No Url",json=None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year=release_year
            self.url=url
        
        else:
            #for member in json:
            #print(type(json),'this is the type of json!!!')##need to comment out later!!!
            #print(json,'this is json')
            if 'trackName' in json.keys():
                self.title=json['trackName']
            elif 'collectionName' in json.keys():
                self.title=json['collectionName']
            elif 'trackCensoredName' in json.keys():
                self.title=json['trackCensoredName']
            elif 'collectionCensoredName' in json.keys():
                self.title=json['collectionCensoredName']
            
                
            self.author=json['artistName']
                
            self.release_year=json['releaseDate'].split("-")[0]
            
            try:
                self.url=json['trackViewUrl']
            except:
                self.url=json['collectionViewUrl']
        
    def info(self):
        return self.title +" by "+self.author+" ("+str(self.release_year)+")"
    def length(self):
        return 0
    
class Song(Media):
    def __init__(self,title="No Title",author="No Author",release_year="No Release Year",
                 url="No Url",album="No Album",genre="No Genre",track_length=0,
                 json=None):
        if json is None:
            super().__init__(title,author,release_year,url)
            self.track_length=track_length
            self.album=album
            self.genre=genre
            
        else:
            #for member in json:
            super().__init__(json=json)
            self.album=json["collectionName"]
            self.genre=json['primaryGenreName']
            self.track_length=json["trackTimeMillis"]
            self.release_year=json['releaseDate'].split("-")[0]
            self.author=json['artistName']
        
    def info(self):
        return super().info()+" ["+str(self.genre)+"]"
    def length(self):
        return self.track_length/1000
    #this return need to convert ms to s, 2
    
class Movie(Media):
    def __init__(self,title="No Title",author="No Author",
                 release_year="No Release Year",url="No Url",
                 rating="No Rating",movie_length=0,
                 json=None):
        if json is None:
            super().__init__(title,author,release_year,url)
            self.rating=rating
            self.movie_length=movie_length
        else:
            #for member in json:
            super().__init__(json=json)
            self.rating=json["contentAdvisoryRating"]
            self.movie_length=json["trackTimeMillis"]
            self.author=json['artistName']
            self.release_year=json['releaseDate'].split("-")[0]
    def info(self):
        return super().info()+ " [" +str(self.rating) +"]"
    def length(self):
        return self.movie_length/1000/60
    





# Other classes, functions, etc. should go here

base_itunes_url= "https://itunes.apple.com/search?"
def get_data(input):
    params={}
    params['term']=input
    response=requests.get(base_itunes_url,params)
    res_dict=response.json()

    return res_dict['results']
    
    #print(get_data(input))
   

    if response.status_code==200:
        res_dict=response.json()
        return res_dict['results']###need fix for convenient
    else:
        print('can not find the results')
        return None
    
def creat_Media(list_dict1):
    other_media_list=[]
    song_list=[]
    movie_list=[]
    #print(dict1)
    for dict1 in list_dict1:
        #print(dict1,'this is dict1!!!!!')
        try:
            if 'kind'not in dict1.keys():
                if Media(json=dict1) not in other_media_list:
                    other_media_list.append(Media(json=dict1))
            if dict1['kind']=='song':
                if Song(json=dict1) not in song_list:
                    song_list.append(Song(json=dict1))
            if dict1['kind']=="feature-movie":
                if Movie(json=dict1) not in movie_list:
                    movie_list.append(Movie(json=dict1))
        except:
            if Media(json=dict1) not in other_media_list:
                other_media_list.append(Media(json=dict1))
            
    return song_list,movie_list,other_media_list



if __name__ == "__main__":
   #Media_list=[]
    # your control code for Part 4 (interactive search) should go here
    search_input = input("Enter a search query or enter 'exit' to quit: ")
    while True:
        if search_input.lower()=='exit':
            print('bye')
            break
        if search_input.isnumeric() is False:
            
            Song_list,Movie_list,Other_list=creat_Media(get_data(search_input))
      
            
            if len(Song_list)!=0:
                print('\nSong\n')
                for i in range(len(Song_list)):
                    print(str(i+1),' ',Song_list[i].info())
                    i+=1
            if len(Movie_list)!=0:
                print('\nMovie\n')
                for i in range(len(Movie_list)):
                    print(str(len(Song_list)+i+1),' ',Movie_list[i].info())
            if len(Other_list)!=0:
                print('\nOther_media\n')
                for i in range(len(Other_list)):
                    print(str(len(Song_list)+len(Movie_list)+i+1), ' ', Other_list[i].info())
        if search_input.isnumeric():
            whole_media_list=Song_list+Movie_list+Other_list

            search_index=int(search_input)
            if int(search_index)>len(whole_media_list):
                print('invalid number please print a number between 1 and ',str(len(whole_media_list)))
            elif int(search_index)<= len(whole_media_list):
                #itunes="https://www.apple.com/itunes/"
                open_url=whole_media_list[int(search_index)-1].url
                print('Lauching')
                webbrowser.open(open_url)
                
        search_input=input("Enter a number for to lauch preview or enter a search query to search or enter 'exit' to quit: ")
            
        
            
            
            
        
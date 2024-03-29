'''
Names: Ayush Misra, Stephen, Santiago
Pledge: We pledge our honor that we have abided by the Stevens Honor System
CS 115 Group Project Part 2
'''
#START CODE HERE


db = {}


def open_database():
    try:
        database = open('musicrecplus.txt', 'r')
    except FileNotFoundError:
        database = open('musicrecplus.txt', 'w+')
    return database

def loadDatabase(filename = "musicrecplus.txt"):
    """Reads the file and assigns its contents to a dictionary"""
    global db
    try:
        with open(filename, 'r') as file:
            for line in file:
                lineSplit = line.strip().split(':')
                name = lineSplit[0]
                artists = set(lineSplit[1].strip().split(','))
                db[name] = artists
    except FileNotFoundError:
        db = {}

def doesUserExist(name):
    '''checks to see if the name exists (Ayush Misra)'''
    db = open_database()
    if db == []:
        return []
    for User in db:
        just_name = User.split(':')
        if just_name[0].lower().strip() == name.lower().strip():
            return [just_name[1]]
    return []


def startMenu(name, preferences):
    """Prints menu and gives options (Ayush Misra)"""
    global db
    if preferences == []:
        preferences = enterPreferences()
        preferences.sort()
        preferences.sort()
        db[name] = preferences
    while True:
        print("""Enter a letter to choose an option :
        e - Enter preferences
        r - Get recommendations
        p - Show most popular artists
        h - How popular is the most popular
        m - Which user has the most likes
        q - Save and quit""")
        choice = input("").lower()
        if choice == "e": #DONE
            preferences = preferences + enterPreferences()
            preferences.sort()
            db[name] = preferences
        if choice == "r": #ALMOST DONE
            getRecommendations(name) 
        if choice == "p":
            showMostPopularArtists(3,sortArtistsByPopularity(countArtistInstances(db))) #Santiagos Task
        if choice == "h":
            howPopularIsMostPopular(sortArtistsByPopularity(countArtistInstances(db))) #Santiagos Tast
        if choice == "m": #DONE
            whichUserHasMostLikes(name) 
        if choice == "q":
            saveAndQuit(name, preferences)
            break
        if choice == "" or choice not in ["e", "p", "r", "h", "m", "q"]:
            print("Invalid Value")

#ENTER PREFERENCES FUNCTION
def enterPreferences():
    preferences = []
    while True:
        artist = input("Enter an artist that you like ( Enter to finish ): ")
        if artist == "":
            break
        preferences += [artist.title()]
    return preferences

#Helper function for most popular artists and how popular is most popular
artistInst = {}
def countArtistInstances(db):
    """By Santiago Yeomans, This function takes the dictionary form of the database as an input, it then
    sorts through every artist within the database and generates a dictionary containing each artist and
    the number of times it appears in the database"""
    for user in db:
        if user[-1] =="$":
            continue
        for artist in db[user]:
            if artist in artistInst:
                artistInst[artist] += 1
            else:
                artistInst[artist] = 1
    return artistInst

#Second helper function for popular artists
topArtists = []
def sortArtistsByPopularity(artistInst):
    """By Santiago Yeomans, This helper function takes a dictionary cointaining artists and how many times
    they appear in a database, it transforms the key value pairs into tupples that start with how many times
    the artist appears and sorts them by most appearences to least appearences
    """
    for artist in artistInst:
        topArtists.append((artistInst[artist],artist))
    topArtists.sort(reverse=True)
    return topArtists

#show most popular artists function
def showMostPopularArtists(n,topArtists):
    """By Santiago Yeomans, This function takes a number n and an ordered list of tupples topArtists, and
    then returns the n number of top artists and integrates it to the general functioning of the music
    recomender. 
    """
    if topArtists  == []:
        print("Sorry , no artists found.")
    else:
        i = 0 
        for i in range(0,n):
            try:
                print(str(i+1)+ "." + topArtists[i][1])
                i += 1
            except IndexError:
                break
            
#How popular is most popular function
def howPopularIsMostPopular(topArtists):
    """By Santiago Yeomans, This function takes the list topArtists generated by the sortArtistsByPopularity
    function and prints how many times the most popular artist appears in it. 
    """
    if topArtists  == []:
        print("Sorry , no artists found.")
    else:
        print(topArtists[0][0])
    

#MOST LIKED FUNCTION
def whichUserHasMostLikes(name):
    db = open_database()
    mostLiked = name, 0
    for line in db:
        just_name = line.strip().split(":")
        just_artists = just_name[1].strip().split(",")
        if "$" in just_name[0]:
            continue
        curr_likes = len(just_name[1].strip().split(","))
        if curr_likes > mostLiked[1]:
            mostLiked = (just_name[0], curr_likes)
    print(mostLiked[0])


#HELPER FUNCTIONS FO GET RECOMMENDATIONS:
def matchNumber(L, l):
    """Find the number of matches for a specific item in 2 separate lists (Stephen)"""
    matches = 0
    for item in L:
        if item in l:
            matches += 1
    return matches



def removeMatch(L, l):
    """Removes the items in a list that were already in a separate list, then
returns the new list (Stephen)"""
    return [item for item in l if item not in L]

 
#ACTUAL GET RECOMMENDATIONS FUNCTION
def getRecommendations(name):
    """Finds the most similar lists of artists as the current user's list in the
memory, then recommends the artists in that list that aren't in the current
users list (Stephen)"""
    maxMatches = 0
    mName = ''
    L = db[name]
    for i in db:
        if i[-1] != '$':
            if i != name:
                l = db[i]
                newMatch = matchNumber(L, l)
                if newMatch > maxMatches:
                    maxMatches = newMatch
                    mName = i
                    final_L = db[mName]
    if maxMatches == 0:
        print("No recommendations available at this time")
    else:
        recommendations = removeMatch(L, final_L)
        print(recommendations)

        
#SAVE AND QUIT FUNCTION
def saveAndQuit(name, preferences):
    '''Uploads the name and preferences to musicrecplus.txt (Ayush Misra)'''
    newPreferences = f"{name}:{','.join(preferences)}\n" 
    with open('musicrecplus.txt', 'r') as f:
        lines = f.readlines()
    newLines = [line for line in lines if line.split(':')[0] != name]
    newLines.append(newPreferences)
    newLines.sort()
    with open('musicrecplus.txt', 'w') as f:
        f.writelines(newLines)



'''Starts the program (Ayush Misra)'''
loadDatabase()
name = input("Enter your name ( put a $ symbol after your name if you wish your preferences to remain private): ")
preferences = doesUserExist(name)
startMenu(name, preferences)

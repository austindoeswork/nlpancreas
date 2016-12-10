import json,MySQLdb
from fuzzywuzzy import fuzz
dbConfig = json.loads(open("nutrition_facts/config.json").read())

class Nutrition():
    def __init__(self, name, protein, fat, carbs, sugar):
        self.name = name
        self.protein = protein
        self.fat = fat
        self.carbs = carbs
        self.sugar = sugar
    def pprint(self):
        print "Nutrition Info:"
        print self.name
        print "----Protein:", self.protein
        print "----Fats   :", self.fat
        print "----Carbs  :", self.carbs
        print "----Sugar  :", self.sugar

#Function takes an string of words like "dried apple"
#returns JSON containing food name, protein,fat,carbohydrate,total_sugar
def getNutritionValue(input):
	inputArray = input.split(" ")
	#  db = MySQLdb.connect(host=dbConfig["host"],user=dbConfig["user"],passwd=dbConfig["passwd"],db=dbConfig["db"], unix_socket=dbConfig["unix_socket"])
	db = MySQLdb.connect(host=dbConfig["host"],user=dbConfig["user"],passwd=dbConfig["passwd"],db=dbConfig["db"])
	cur = db.cursor()
	query = "SELECT Food_Name, Protein, Fat, Carbohydrate, Total_Sugar from nutrition_fact WHERE "

	for i in range(0,len(inputArray)):
		if( i != len(inputArray)-1):
			query += "Food_Name LIKE '%"+inputArray[i]+"%' AND "
		else:
			query += "Food_Name LIKE '%"+inputArray[i]+"%'"

	cur.execute(query)

        try:
            allMatches = cur.fetchall()
            bestMatch = None
            bestRatio = 0
            
            for match in allMatches:
                ratio = fuzz.partial_token_sort_ratio(match[0], input)
                if ratio > bestRatio:
                    ratio = bestRatio
                    bestMatch = match

            n = Nutrition(bestMatch[0],bestMatch[1],bestMatch[2],bestMatch[3],bestMatch[4])
            return n

        except:
            return None
        



#EXAMPLE CALL:
#  a="dried apple"
#  getNutritionValue(a)

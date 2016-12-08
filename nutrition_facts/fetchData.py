import json,MySQLdb
dbConfig = json.loads(open("./config.json").read())

#Function takes an string of words like "dried apple"
#returns JSON containing food name, protein,fat,carbohydrate,total_sugar
def getNutritionValue(input):
	inputArray = input.split(" ")
	db = MySQLdb.connect(host=dbConfig["host"],user=dbConfig["user"],passwd=dbConfig["passwd"],db=dbConfig["db"], unix_socket=dbConfig["unix_socket"])
	cur = db.cursor()
	query = "SELECT Food_Name, Protein, Fat, Carbohydrate, Total_Sugar from nutrition_fact WHERE "

	for i in range(0,len(inputArray)):
		if( i != len(inputArray)-1):
			query += "Food_Name LIKE '%"+inputArray[i]+"%' AND "
		else:
			query += "Food_Name LIKE '%"+inputArray[i]+"%'"

	cur.execute(query)
	first = cur.fetchall()[0]

	jsonOut = "{"
	jsonOut +="'Food_Name':" + "'" + first[0] + "',"
	jsonOut +="'Protein':" + "'" + first[1] + "',"
	jsonOut +="'Fat':" + "'" + first[2] + "',"
	jsonOut +="'Carbohydrate':" + "'" + first[3] + "',"
	jsonOut +="'Total_Sugar':" + "'" + first[4] + "'"
	jsonOut += "}"

	return jsonOut



#EXAMPLE CALL:
# a="dried apple"
# getNutritionValue(a)

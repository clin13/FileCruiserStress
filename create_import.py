name = "test"
password = "123456"
email = "kevin.chang@tw.promise.com"
status = "TRUE"
quota = "1"
OU = ""

begin_user = 501
n = 1500

with open("501~2000.csv", "w") as textfile:
	for i in range(begin_user, begin_user + n):
		textfile.write(name + "{0}".format(i) + "," + password + "," 
			+ email + "," + status + "," + quota + "," + OU +"\n")
		print name + "{0}".format(i) + "," + password + "," + email + "," + status + "," + quota + "," + OU
import pyrebase
config = {
  "apiKey": " AIzaSyBi1QOGpckOdZnanlDl3o1Dlbz8gfqOxVU",
  "authDomain": "polireddit",
  "databaseURL": "https://polireddit.firebaseio.com",
  "storageBucket": "polireddit.appspot.com",
  "serviceAccount": "poliReddit-serviceAccount.json"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
#authenticate a user
user = auth.sign_in_with_email_and_password("jsuarez@go.olemiss.edu", "polipoli")
_userId = user['idToken']

db = firebase.database()

numbers = {1:1, 2:2, 3:3}

db.child('test').set(numbers, _userId)
db.child('test').update({4:4}, _userId)

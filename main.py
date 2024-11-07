from flask import Flask, render_template, request, redirect,  session, jsonify
import os
from models.User import db, User
from models.Question import Question

app = Flask(__name__)



# replace key value in future
app.secret_key = "amongus"

f = open('static/comc2006/Answers.txt', 'r')
imageNames = os.listdir('static/comc2006/Images/')
imageList = ['/static/comc2006/Images/' + name for name in imageNames]
answerList = f.read().split("\n")
print(answerList)


questionList=[Question(imageList[i], answerList[i]) for i in range(0, len(imageList))]
# dictionary with Question object as key value and fileName as key 
questionId = {imageNames[i]:questionList[i] for i in range (0, len(imageNames))}

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
questionList =[Question(imageList[i], answerList[i]) for i in range(0, len(imageList))]
questionId= {imageNames[i]:questionList[i] for i in range (0, len(imageNames))}


scores = [0.5, 0.89]
db.init_app(app)
with app.app_context():
    db.create_all() 

@app.route('/', methods=['GET', 'POST'])
def register():
      if request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')
          user = User(username = username, password=password) # type: ignore
          db.session.add(user)
          db.session.commit()
         
      return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')
          user = User.query.filter_by(username=request.form.get("username")).first()
          if user.password == password: # type: ignore
              session['userId']=user.id # type: ignore
              return redirect('/index')
          
          
     return render_template('login.html')

@app.route('/test')
def test():
    return render_template('test.html', profile = User.query.all())



@app.route('/index')
def index():
    print(questionList[0].isCompleted())
    return render_template('index.html')

@app.route('/page1')
def page1():
    duration = 1.25
    return render_template('page1.html', duration = duration)

@app.route('/submit_time', methods=['POST'])
def submit_time():
    timeLeft = request.json.get('timeLeft')
    print(timeLeft)


    return jsonify({"status": "success", "timeLeft": timeLeft})

@app.route('/practice')
def practice():
    return render_template('practice.html', questionId=questionId)

@app.route('/handle_question', methods=['POST'])
def handle_question():
    question_id = request.form.get('question_id')
    q = questionId[question_id]
    q.setStarred()
    print(q.isStarred())

    print(f"Processing question with ID: {question_id}")
    return render_template('practice.html', questionId=questionId)


@app.route('/q/<string:id>', methods=['GET', 'POST'])
def question(id):
    #user = User.query.get(session['userId'])
    q = questionId[id]
    if request.method=='POST':
        ans = request.form.get('answer')
        if not q.isCompleted() and ans == q.getAnswer():
            q.setCompleted()
            #user.score += 1
            #db.session.commit()
    

    return render_template('problem.html', question=q)



@app.route('/contest', methods=['GET', 'POST'])
def contest():
    contestQuestions = questionList
    score = 0
    if request.method == 'POST':
        for q in contestQuestions:
            ans = request.form.get(q.getFileName())
            print(str(ans) + " " + str(q.getAnswer()))
            if ans == q.getAnswer():
                q.setCompleted()
                score+=1
        scores.append(score/len(contestQuestions))
        return redirect('/index')

    return render_template('contest.html', contestQuestions = contestQuestions)

@app.route('/profile')
def profile ():
    return render_template('profile.html', scores = scores)

if __name__ == '__main__':
    app.run(debug=True)

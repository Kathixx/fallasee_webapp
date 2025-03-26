from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello from Flask!"


# source: https://heartbeat.comet.ml/deploying-a-text-classification-model-using-flask-and-vue-js-25b9aa7ff048
# The input_predict_text() function receives the text input from the web application, and using the text
# classifier (best-model.pt) loaded from the models folder, predicts and returns the result in Json format.
# The get_results function, on the other hand, prepares the output to be displayed on the Vue.js frontend.
#
#
# @app.route('/tasks', methods=['GET'])
# def get_result():
#     result = []
#     data_result = session['my_result']
#     result.append ({'title': data_result['title'], 'tag': data_result['tag'] })
#     session.clear()
#     return jsonify(result)

# @app.route('/task', methods=['POST'])
# def input_predict_text():
#     #path to the classification model
#     classifier = TextClassifier.load_from_file('models/best-model.pt')
#     #get input
#     title = request.get_json()['title']
#     sentence = Sentence(title)
#     # # run the classifier over sentence
#     classifier.predict(sentence)
#     text = sentence.to_plain_string()
#     label = sentence.labels[0]
#     result = {'title' : text, 'tag' : label.value}
#     session['my_result'] = result
#     return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)

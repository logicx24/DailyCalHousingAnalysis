from flask.ext.api import FlaskAPI
from flask import request, current_app
import listingPrediction 
app = FlaskAPI(__name__)


classifier = listingPrediction.Classifier()

@app.route("/classify", methods=['GET'])
def classify():
	toClassify = request.args.get('link')#request.data['link']
	callback = request.args.get('callback')
	return '{0}({1})'.format("resp", classifier.predictionFromLink(toClassify)[0])
if __name__ == "__main__":
	listingPrediction.jsonDump()
	classifier.csvDump()
	classifier.train()
	app.run(debug=True)

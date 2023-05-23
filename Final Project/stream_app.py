import pickle
import streamlit as st
import pandas as pd
from PIL import Image


dv = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

def main():

	image = Image.open('images/icone.png')
	image2 = Image.open('images/image.png')
	img =Image.open('images/Customer-Churn.png')
	st.image(image,width=700, use_column_width=120)
	add_selectbox = st.sidebar.selectbox(
	"How would you like to predict?",
	("Online", "Batch"))
	st.sidebar.info('This app is created to predict Customer Churn')
	st.sidebar.image(image2)
	st.sidebar.image(img)
	st.title("Predicting Customer Churn")
	if add_selectbox == 'Online':
		st.info("Input data below")
		gender = st.selectbox('Gender:', ['male', 'female'])
		seniorcitizen= st.selectbox(' Customer is a senior citizen:', [0, 1])
		partner= st.selectbox(' Customer has a partner:', ['yes', 'no'])
		dependents = st.selectbox(' Customer has  dependents:', ['yes', 'no'])
		phoneservice = st.selectbox(' Customer has phone service:', ['yes', 'no'])
		multiplelines = st.selectbox(' Customer has multiple lines:', ['yes', 'no', 'no_phone_service'])
		internetservice= st.selectbox(' Customer has internet service:', ['dsl', 'no', 'fiber_optic'])
		onlinesecurity= st.selectbox(' Customer has online security:', ['yes', 'no', 'no_internet_service'])
		onlinebackup = st.selectbox(' Customer has online backup:', ['yes', 'no', 'no_internet_service'])
		deviceprotection = st.selectbox(' Customer has device protection:', ['yes', 'no', 'no_internet_service'])
		techsupport = st.selectbox(' Customer has tech support:', ['yes', 'no', 'no_internet_service'])
		streamingtv = st.selectbox(' Customer has streaming tv:', ['yes', 'no', 'no_internet_service'])
		streamingmovies = st.selectbox(' Customer has streaming movies:', ['yes', 'no', 'no_internet_service'])
		contract= st.selectbox(' Customer has a contract:', ['month-to-month', 'one_year', 'two_year'])
		paperlessbilling = st.selectbox(' Customer has a paperless billing:', ['yes', 'no'])
		paymentmethod= st.selectbox('Payment Option:', ['bank_transfer_(automatic)', 'credit_card_(automatic)', 'electronic_check' ,'mailed_check'])
		tenure = st.number_input('Number of months the customer has been with the current telco provider :', min_value=0, max_value=240, value=0)
		monthlycharges= st.number_input('Monthly charges :', min_value=0, max_value=300, value=0)
		totalcharges = tenure*monthlycharges
		output= ""
		output_prob = ""
		input_dict={
				"gender":gender ,
				"seniorcitizen": seniorcitizen,
				"partner": partner,
				"dependents": dependents,
				"phoneservice": phoneservice,
				"multiplelines": multiplelines,
				"internetservice": internetservice,
				"onlinesecurity": onlinesecurity,
				"onlinebackup": onlinebackup,
				"deviceprotection": deviceprotection,
				"techsupport": techsupport,
				"streamingtv": streamingtv,
				"streamingmovies": streamingmovies,
				"contract": contract,
				"paperlessbilling": paperlessbilling,
				"paymentmethod": paymentmethod,
				"tenure": tenure,
				"monthlycharges": monthlycharges,
				"totalcharges": totalcharges
			}

		if st.button("Predict"):
			X = dv.transform([input_dict])
			y_pred = model.predict_proba(X)[0, 1]
			churn = y_pred >= 0.5
			output_prob = float(y_pred)
			output = bool(churn)
		st.success('Churn: {0}, Risk Score: {1}'.format(output, output_prob))
  
	if add_selectbox == 'Batch':
		file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
		try:
			if file_upload is not None:
				data = pd.read_csv(file_upload)
				cust_ids = data['customerID']
				data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
				data['TotalCharges'] = data['TotalCharges'].fillna(0)
				data.columns = data.columns.str.lower().str.replace(' ', '_')

				string_columns = list(data.dtypes[data.dtypes == 'object'].index)
				for col in string_columns:
					data[col] = data[col].str.lower().str.replace(' ', '_')
				data = data.iloc[:, 1:-1].to_dict(orient='records')

				X = dv.transform(data)
				y_pred = model.predict_proba(X)[:,1]
				churn = y_pred > 0.5
				st.write("Customer Id :: churn")

				for i in range(len(cust_ids)):
					st.write(f"{cust_ids[i]} :: {churn[i]}")

				#st.write(churn)

		except Exception as msg:
			st.write("Error Occured", msg)

if __name__ == '__main__':
	main() 
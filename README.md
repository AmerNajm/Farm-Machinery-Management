🚜 Tractor Performance & Fuel Consumption Estimator
This Streamlit app helps farm managers estimate tractor fuel consumption and field performance based on ASABE Agricultural Machinery Management guidelines.

✅ Features

Inputs for tractor and implement details:

Engine Power (kW)
Load Factor (0–1)
Hours of Operation
SVFC (L/kWh)
Fuel Price
Field Area (ha)
Speed (km/h)
Width (m)
Field Efficiency (%)


Outputs:

Energy Output (kWh)
Fuel Consumption (L)
Fuel Cost
Effective Field Capacity (ha/h)
Time Required (h)


Charts:

Fuel Consumption vs Load Factor
Field Capacity vs Speed


ASABE Typical Values Table
Download results as Excel


✅ How to Run Locally

Clone the repository:
Shellgit clone https://github.com/<your-username>/tractor-performance-app.gitcd tractor-performance-appShow more lines

Install dependencies:
Shellpip install -r requirements.txtShow more lines

Run the app:
Shellstreamlit run tractor_app.pyShow more lines

Open the URL shown in the terminal (usually http://localhost:8501).


✅ How to Deploy on Streamlit Cloud

Push tractor_app.py and requirements.txt to your GitHub repository.
Go to https://streamlit.io/cloud.
Sign in with your GitHub account.
Click New App → Select your repo → Enter tractor_app.py as the app file.
Click Deploy.
Share the public URL with your team.


✅ Troubleshooting

App fails to deploy (ModuleNotFoundError):

Ensure all libraries are listed in requirements.txt.


App stuck on “Installing dependencies”:

Check for typos in requirements.txt.


Charts not showing:

Confirm plotly is installed and imported correctly.


Excel download not working:

Ensure xlsxwriter is in requirements.txt.# Farm-Machinery-Management
Farm Machinery Management Solution

# AI-Powered Crop Disease Tracker


![gi-kace logo](https://github.com/user-attachments/assets/86326df3-bcf6-47d2-9b50-f346f6a9e7ec)

A data analytics project to track and predict crop disease spread in agriculture, built with Python, SQL Server, and Streamlit. This tool visualizes disease hotspots, trends, and lets farmers report outbreaks in real-time—blending data science with a touch of AI potential.

## Overview

Crop diseases threaten global food security, and farmers need proactive tools. This project delivers:
- An **interactive dashboard** with maps and severity trends.
- A **real-time reporting system** for farmers.
- A foundation for **AI predictions** (work in progress).

Built from scratch—database design, synthetic data generation, and a sleek UI—it’s a showcase of agriculture meeting modern tech.

## Features

- **Disease Map**: Visualize outbreaks with severity-based markers (red for severe, orange for mild).
- **Severity Trend**: Track average disease severity over time.
- **Reporting Form**: Submit new disease reports, updating the dashboard live.
- **Dark/Light Mode**: Toggle themes for a personalized experience.
- **Responsive Design**: Works on desktop and mobile.

## Tech Stack

- **Database**: SQL Server (schema in `create_database.sql`)
- **Data Population**: Python, Pandas, NumPy, SQLAlchemy (`populate_data.ipynb`)
- **Dashboard**: Streamlit, Folium (maps), Plotly (charts) (`app.py`)
- **Future**: Machine Learning (e.g., Random Forest) and Generative AI

## Setup

### Prerequisites
- Python 3.8+
- SQL Server (local or remote)
- Git

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/OforiPrescott/Crop-Disease-Tracker.git
   cd crop-disease-tracker
   
2. Set Up Virtual Environments:
- For Jupyter Notebook:
     python -m venv notebook_env
     notebook_env\Scripts\activate
     pip install jupyter pandas numpy sqlalchemy

- For Streamlit:
     python -m venv streamlit_env
     streamlit_env\Scripts\activate
     pip install -r requirements.txt
  
3. Create Database:
   - Open SQL Server Management Studio (SSMS).
   - Run AgriDiseaseDB.sql to set up AgriDiseaseDB.

4. Populate Data:
- Activate notebook_env:
  notebook_env\Scripts\activate
  
- Open populate_data.ipynb in Jupyter:
  jupyter notebook

- Update the server name in the connection string (e.g., PresHacks), then run all cells.
  
5. Run the Dashboard:
   Activate streamlit_env:
   streamlit_env\Scripts\activate

6. Launch the app:
   - streamlit run app.py

  Visit http://localhost:8501 


## Usage
1. Explore: Filter by disease or date range in the sidebar.
2. Report: Submit a new disease sighting via the form.
3. Toggle Theme: Switch between dark and light modes.


## Screenshots

## Disease Map

![Screenshot 2025-03-10 150209](https://github.com/user-attachments/assets/35247913-2cba-4da6-bff4-a413186100b1)

Interactive map showing disease spread

## Severity 

![Screenshot 2025-03-10 150230](https://github.com/user-attachments/assets/b2dc42c7-b59f-4124-a4ef-fadc924880f7)

Trend of Average Severity


## Demo Notes
The live demo on Streamlit Cloud uses mock data due to the SQL Server database not being accessible in the cloud environment. You’ll see a message:

   Database connection failed: ... Using mock data for demo.
- The map, trend chart, and filters work fully with mock data.
- The reporting form is disabled in this mode.To enable full functionality (including reporting), set up a local SQL Server instance or
  host the database on a cloud provider like Azure SQL (future enhancement).
  
## Future Enhancements
- Add ML models to predict disease spread.
- Integrate generative AI for mitigation suggestions.
- Support real farmer data via API.
- Host the database in the cloud for full functionality.

## Contributing
Feel free to fork, tweak, or suggest ideas! Open an issue or submit a pull request—I’d love to collaborate.


## License
MIT License—use it, share it, build on it.


## Acknowledgments
- GI-KACE for inspiration.
- The open-source community for tools like Streamlit and Folium.



## Try It Out
- Live Demo: https://crop-disease-tracker-hplhecjyjamm2qtsvmkras.streamlit.app/
- LinkedIn Article: Read the full story
  
Questions? Thoughts? Drop a comment or connect with me on LinkedIn!




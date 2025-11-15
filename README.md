# FDC 1.0.0 - Fermentation and Distillation Calculator

A comprehensive web application for precise calculations of alcohol fermentation and distillation processes.

## 📋 Features

### Fermentation Calculations
- **Sugar Fermentation Calculator**: Calculate sugar content, water volume, and required nutrients
- **Grain Fermentation**: Fermentation calculations for various grains
- **Fruit Fermentation**: Fermentation calculations for fruits
- **General Fermentation Calculations**: Overall fermentation process calculations

### Distillation Calculations
- **Spiral Packing**: Calculate spiral packing parameters
- **Reflux**: Reflux ratio calculations and related parameters
- **Azeotrope**: Calculate azeotropic point
- **Spirit Run**: Precise calculations for spirit runs
- **Tank Heating Time**: Calculate time required to heat the distillation tank
- **Boiling Point**: Calculate boiling point based on pressure and temperature
- **Column Heat**: Thermal calculations for distillation columns
- **Remaining Liquid**: Calculate remaining liquid volume

### Other Calculations
- **Blood Alcohol Calculator**: Calculate blood alcohol concentration based on beverage consumption
- **Element Power**: Electrical heating element power calculations
- **Refractometer**: Refractometer calculations

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. Clone or download the project:
```bash
git clone https://github.com/Hrnikkhoo/chemical-process-calculator.git
cd iferment1.0.0
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
iferment1.0.0/
├── app.py                 # Main Flask file
├── requirements.txt       # Project dependencies
├── README.md             # This file
├── .gitignore            # Files ignored by Git
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   └── [Other templates]
│
├── static/               # Static files
│   ├── css/
│   ├── js/
│   └── img/
│
└── [Calculation files]   # Python files for calculations
    ├── sugercalc.py
    ├── graincalc.py
    ├── fruitcalc.py
    ├── bloodalco.py
    └── ...
```

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Icons**: Font Awesome

## 📝 Usage

1. After running the application, open the main page
2. Select your desired calculator
3. Enter the values
4. Click the "Calculate" button
5. View the results

## 🔧 Development

To develop and improve the project:

1. Fork the project
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Notes

- This application is designed for educational and research purposes
- When using blood alcohol calculations, always exercise caution and never drive under the influence
- Calculation results are approximate and may differ from actual conditions

## 📄 License

This project is released under the MIT License.

## 👥 Contributing

Contributions, suggestions, and bug reports are always welcome!

## 📧 Contact

For questions and support, please create an Issue on GitHub.

---

**Version**: 1.0.0  
**Last Update**: 2025

---

## Detailed Description

This project, "chemical-process-calculator", is a Flask-based web application designed to provide a comprehensive suite of calculators for various parameters encountered in chemical processes, with a particular emphasis on fermentation and distillation. The application integrates a range of specialized computational tools to assist users in optimizing and understanding key aspects of these processes.

### Key Functionalities:

*   **Specific Gravity and Alcohol Content Analysis:** The SPN Calculator facilitates the determination of specific gravity and potential alcohol yield, crucial for fermentation monitoring.
*   **Thermal Dynamics:** The Heat Time Calculator and Column Heat Calculator enable precise calculation of heating durations and thermal energy requirements for process optimization and energy efficiency.
*   **Distillation Column Optimization:** Two distinct Reflux Calculators provide tools for determining optimal reflux ratios and related operational parameters, critical for achieving desired separation efficiencies in distillation.
*   **Azeotropic Mixture Analysis:** The Azeotrope Calculator assists in identifying and characterizing azeotropic mixtures, which are fundamental to understanding distillation limitations and strategies.
*   **Fermentation Process Modeling:** The Sugar, Grain, and Fruit Calculators provide specialized tools for feedstock analysis and fermentation parameter prediction, while the Fermentation Calculator offers a broader overview of the fermentation process.
*   **Refractometry and Concentration:** The Refractometer Calculator aids in interpreting refractometric data, essential for accurate concentration measurements in various solutions.
*   **Spirit Production Optimization:** The Spirit Run Calculator is tailored for optimizing spirit distillation, considering factors such as cuts and yield.
*   **Ancillary Chemical Engineering Tools:** Additional calculators include the Element Power Calculator for electrical heating elements, Remaining Liquid Calculator for volume assessments, and Boiling Point Calculator for phase equilibrium analysis.
*   **Blood Alcohol Content:** The Blood Alcohol Calculator helps estimate blood alcohol concentration based on beverage consumption, gender, weight, and time factors.

This platform serves as an invaluable resource for chemical engineers, distillers, brewers, and researchers, offering precise computational support for process design, control, and troubleshooting in chemical and biochemical industries.

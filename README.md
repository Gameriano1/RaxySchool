<a id="readme-top"></a>
 
<br />
<div align="center">
  <a href="https://github.com/leonifrazao/RaxySchool">
    <img src="itens/logo.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">RaxySchool</h3>

  <p align="center">
    School Absence Analysis System for São Paulo State Public Schools
    <br />
    <a href="https://github.com/leonifrazao/RaxySchool"><strong>Explore the documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/leonifrazao/RaxySchool/releases">View Releases</a>
    ·
    <a href="https://github.com/leonifrazao/RaxySchool/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/leonifrazao/RaxySchool/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#analysis-examples">Analysis Examples</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![product-screenshot](itens/logo.png)

RaxySchool is a comprehensive tool for analyzing student absences in São Paulo's state education network, using data provided by the São Paulo State Department of Education (SED). The system enables school administrators, pedagogical coordinators, and educators to identify absence patterns and make data-driven decisions to improve attendance and academic performance.

Why use RaxySchool?

**Detailed Analysis**: Visualize absence patterns by period, school, classroom, and region

**Automated Notifications**: Send automatic messages to parents about student absences

**Visual Reports**: Intuitive graphs and reports to facilitate decision-making

**Risk Identification**: Detect students at risk of school dropout

**User-Friendly Interface**: Modern and easy-to-use graphical interface

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

![Python.py](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To start using RaxySchool, follow these simple installation steps.

### Prerequisites

Before you begin, make sure you have the following requirements:

**Python**: Version 3.7 or higher

```sh
python --version
```

**Google Chrome**: Updated browser (for Selenium automation)

**SED Access**: Valid credentials to access the Department of Education system

### Installation

1. Clone the repository

```sh
git clone https://github.com/leonifrazao/RaxySchool.git
```

2. Navigate to the project directory

```sh
cd RaxySchool
```

3. Install the required dependencies

```sh
pip install -r requirements.txt
```

4. Configure your SED access credentials (if necessary)

```python
# Edit the settings in the configuration file
```

5. Run the application

```sh
python RaxySchool.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->

## Usage

### Main Interface

The RaxySchool interface was developed with CustomTkinter to provide a modern and intuitive experience:

**System Login**: Enter your SED credentials

**Period Selection**: Choose the school term you want to analyze

**Data Visualization**: View reports and graphs in real-time

**Export**: Export reports in PDF or Excel format

### Command Examples

```python
# Load data from a specific school
from RaxySchool import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_school_data(school_id="123456")

# Generate absence report
report = analyzer.generate_absence_report()
report.export_to_pdf()
```

For more examples and detailed documentation, see the [Wiki](https://github.com/leonifrazao/RaxySchool/wiki)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->

## Features

- Automatic Data Collection: Extraction of data directly from SED
- Pattern Analysis: Identification of absence trends
- Parent Notifications: Automated alert system
- Modern Graphical Interface: Developed with CustomTkinter
- Interactive Charts: Dynamic data visualizations
- Report Generation: Export to PDF and Excel
- Period Analysis: Data comparison between quarters/trimesters
- School/Classroom Analysis: Breakdown by school unit

**In Development:**

- Mobile Version
- WhatsApp API Integration
- Interactive Web Dashboard
- Real-Time Alert System

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXAMPLES -->

## Analysis Examples

### 1. Absence Distribution by Period

Temporal analysis that identifies critical periods with high absence rates throughout the school year, enabling preventive actions at strategic moments.

### 2. Automated Messages

Automatic notification system for guardians about student absences, promoting greater family engagement in school life.

### 3. Absences by Classroom

Detailed comparison of absences between different grades and school cycles, helping identify classes that need specific interventions.

### 4. Impact on Academic Performance

Cross-analysis between absence patterns and student academic performance, revealing the correlation between attendance and school achievement.

### 5. Geographic Analysis

Mapping of absences by region, school, and district, allowing identification of areas that need special attention.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] SED data collection system
- [x] Graphical interface with CustomTkinter
- [x] Basic report generation
- [x] Email notification system
- [ ] Implement web dashboard
- [ ] WhatsApp Business API integration
- [ ] School dropout prediction system using ML
- [ ] Mobile application (iOS/Android)
- [ ] REST API for integration with other systems
- [ ] Automatic backup system
- [ ] Multi-language support
- [ ] Offline mode for data analysis

See the [open issues](https://github.com/leonifrazao/RaxySchool/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion to improve the project, please fork the repository and create a pull request. You can also simply open an issue with the "enhancement" tag.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top Contributors

<a href="https://github.com/leonifrazao/RaxySchool/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=leonifrazao/RaxySchool" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Leoni Frazão - [@leonifrazao](https://twitter.com/leonifrazao)

Project Link: [https://github.com/leonifrazao/RaxySchool](https://github.com/leonifrazao/RaxySchool)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Resources and tools that made this project possible:

* [Python Documentation](https://docs.python.org/)
* [Pandas Documentation](https://pandas.pydata.org/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [Selenium WebDriver](https://www.selenium.dev/)
* [Secretaria de Educação do Estado de São Paulo](https://www.educacao.sp.gov.br/)
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<div align="center">

**Developed with a focus on education**

Helping schools improve student attendance and performance through data

[Back to top](#readme-top)

</div>

<!-- MARKDOWN LINKS & IMAGES -->

# Wipro Python Automation

A structured collection of Python automation assignments and practical exercises completed as part of the **Wipro Python Automation training program**.

The repository contains hands-on work covering **Selenium Web Automation, Python BDD & RESTful API Automation, Robot Framework**, and a **Capstone Automation Assignment**.

---

## 📚 Repository Contents

| Section                              | Description                                                       |
| ------------------------------------ | ----------------------------------------------------------------- |
| **Selenium Automation**              | Web UI automation assignments using Python and Selenium WebDriver |
| **Python BDD & RESTful Automations** | REST API automation and BDD-based testing exercises               |
| **Robot Framework**                  | Test automation assignments implemented using Robot Framework     |
| **Capstone Assignment 1**            | End-to-end Selenium automation project with execution reporting   |
| **Certificates**                     | Training and certification documents                              |
| **Video Demonstrations**             | Assignment execution recordings                                   |

---

## 🗂️ Project Structure

```text
Wipro_Python_Automation/
│
├── Assignments/
│   │
│   ├── Automation with Selenium/
│   │   ├── Assignment_1/
│   │   ├── Assignment_2/
│   │   ├── Assignment_3/
│   │   ├── Assignment_4/
│   │   ├── Assignment_5/
│   │   ├── Assignment_6/
│   │   ├── Assignment_7/
│   │   ├── Assignment_8/
│   │   ├── Assignment_9/
│   │   ├── Selenium_1st_video.mp4
│   │   └── requirements.txt
│   │
│   ├── Python BDD Restful Automations/
│   │   ├── assignment_01/
│   │   ├── assignment_02/
│   │   └── assignment_03/
│   │
│   └── Robot Framework/
│       ├── assignment_01/
│       ├── assignment_02/
│       ├── assignment_03/
│       ├── assignment_04/
│       ├── assignment_05/
│       ├── assignment_06/
│       └── assignment_07/
│
├── capstone_assignment_1/
│   ├── capstone_assignment_1.py
│   ├── recording/
│   ├── reports/
│   ├── screenshots/
│   └── requirements.txt
│
├── Certificates/
│
├── Video_Drive_Link
├── .gitattributes
└── .gitignore
```

The structure above reflects the current repository organization.

---

# 🧪 1. Selenium Web Automation

The Selenium section contains practical web automation assignments implemented using **Python and Selenium WebDriver**.

### Covered work

* Browser automation
* Web element identification and interaction
* Forms and user input
* Dropdowns and checkboxes
* Dynamic web elements
* Product and shopping workflows
* Assertions and validation
* Explicit waits
* Screenshots and execution evidence
* End-to-end browser automation

The Selenium assignments are organized sequentially from **Assignment 1 through Assignment 9**.

---

# 🔗 2. Python BDD & RESTful Automations

This section contains Python-based exercises focused on **REST API automation and BDD-style testing**.

```text
Python BDD Restful Automations/
│
├── assignment_01/
├── assignment_02/
└── assignment_03/
```

The assignments are organized independently so that each exercise can be reviewed and executed separately.

---

# 🤖 3. Robot Framework

The Robot Framework section contains practical automation assignments implemented using **Robot Framework**.

```text
Robot Framework/
│
├── assignment_01/
├── assignment_02/
├── assignment_03/
├── assignment_04/
├── assignment_05/
├── assignment_06/
└── assignment_07/
```

Each assignment is maintained in its own directory for independent execution and evaluation.

---

# 🚀 4. Capstone Assignment 1

The capstone is an end-to-end Selenium automation implementation.

```text
capstone_assignment_1/
│
├── capstone_assignment_1.py
├── recording/
├── reports/
├── screenshots/
└── requirements.txt
```

The capstone includes:

* Chrome browser automation
* User login / account handling
* Product search
* Product selection
* Add-to-cart workflow
* Cart quantity validation
* Assertions
* Screenshot capture
* Execution reporting
* HTML execution report generation
* Recorded demonstration

The main automation implementation is contained in `capstone_assignment_1.py`, with separate directories for recordings, reports, and screenshots.

---

# 🛠️ Technologies & Tools

The repository work primarily uses:

* **Python**
* **Selenium WebDriver**
* **Pytest**
* **Robot Framework**
* **REST API testing**
* **BDD**
* **Chrome WebDriver**
* **Git & GitHub**
* **Git LFS**

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone https://github.com/Mayukh27/Wipro_Python_Automation.git
cd Wipro_Python_Automation
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

Navigate to the relevant assignment directory and install its requirements:

```bash
pip install -r requirements.txt
```

For example:

```bash
cd "Assignments/Automation with Selenium"
pip install -r requirements.txt
```

The repository currently maintains separate `requirements.txt` files for the Selenium section and the Capstone.

---

# ▶️ Running the Automation

Navigate to the required assignment directory and execute the corresponding Python script.

Example:

```bash
python assignment_03_dropdowns_checkboxes.py
```

For the capstone:

```bash
cd capstone_assignment_1
python capstone_assignment_1.py
```

> Test data and credentials used by individual assignments may need to be configured according to the assignment requirements before execution.

---

# 🎥 Demonstration Videos

Execution recordings are provided for demonstration and evaluation purposes.

### Google Drive

A consolidated Google Drive folder containing the assignment recordings is available here:

**[📁 View Assignment Demonstration Videos](https://drive.google.com/drive/folders/13hHv1CmXM-gd4oN5LhwraoYLWVpvDJHe?usp=drive_link)**

The repository also contains video recordings tracked using **Git LFS**.

For large video files, GitHub may not display an in-browser preview. In that case, the recordings can be accessed through the Google Drive folder above.

The Drive link is also maintained in the repository's `Video_Drive_Link` file.

---

# 📄 Certificates

Training and certification documents are available in:

```text
Certificates/
```

---

# 📦 Large Files

Large video recordings are managed using **Git Large File Storage (Git LFS)**.

The repository contains a `.gitattributes` configuration for LFS-tracked files.

To work with the video files after cloning:

```bash
git lfs install
git lfs pull
```

---

# 🧹 Repository Hygiene

The repository excludes generated and environment-specific files such as:

```text
venv/
.venv/
__pycache__/
.pytest_cache/
```

through `.gitignore`.

---

# 👤 Author

**Mayukh Ghosh**

GitHub: [@Mayukh27](https://github.com/Mayukh27)

---

## 📌 Submission

This repository contains the source code, automation assignments, supporting files, execution evidence, and demonstration recordings required for the **Wipro Python Automation** training and assignment submission.

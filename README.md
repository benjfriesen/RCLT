<img src="https://github.com/user-attachments/assets/dd4fec50-cb2d-4261-bc7f-192e6187ff10" align="center" alt="Department Logo" />

# RCLT (Recycled Cross-Laminated Timber)
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54) ![OpenCV](https://img.shields.io/badge/opencv-%23fff.svg?style=for-the-badge&logo=opencv&logoColor=black) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) 

## Introduction
This repository encompasses my work as a research assistant under Dr. Julie Cool and Dr. Minghao Li, working on evaluting the feasibility of using recycled (pre-stressed) wood in structural applications.

The primary goal of this study is to support the path to standardization and code compliance of reclaimed wood, by evaluating performance metrics and creating standardized testing protocols.

The secondary goal of this study is to create a machine learning model trained on the results of the structural tests in correlation to the defects and characteristics of the reclaimed wood samples. This model should be able to predict an ideal use case of a reclaimed wood sample from a set of input conditions.

## Database
The central database for this project uses SQLite 3.51.1, but some initial data entry was done in Microsoft Access before being ported over.

SQLite was chosen since it is natively supported in the Python Standard Library

```mermaid
%%{init: {'theme': 'neutral'}}%%
erDiagram
    boards {
TEXT board_id PK
TEXT species_name
TEXT grade_name
    }
    species {
TEXT species_id PK
    }
    grades {
TEXT grade_id PK
    }
    impurities {
TEXT board_id PK
INTEGER nails
INTEGER staples
INTEGER connected_boards
INTEGER screws
INTEGER misc_fasteners
    }
    moe {
TEXT board_id PK
REAL velocity
    }
    species ||--o{ boards : references
    boards ||--o{ impurities : references
    grades ||--o{ boards : references
    boards ||--o{ moe : references
```

## CV Model

### Background Removal & Batch Processing
To process the board photos (taken on a Sony A7Siii in a controlled environment), OpenCV and Rembg were used to isolate the subject from our makeshift photo studio.

Raw photo (A120)
<img src="./boards/raw/A120_0001.jpg" alt="Raw photo (A120)">

Processed photo (A120)

<img src="./boards/processed/A120_0001_Processed.jpg" alt="Processed photo (A120)">

Further processing for edge case scenarios where the script did not accurately isolate the subject was done in Adobe Photoshop 2026 using a variety of masking tools.

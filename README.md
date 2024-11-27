# CityByte Project 2

[![Test](https://github.com/CSC510-Software-Engineering-Fall-2024/CityByte/actions/workflows/django.yml/badge.svg)](https://github.com/CSC510-Software-Engineering-Fall-2024/CityByte/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/CSC510-Software-Engineering-Fall-2024/CityByte/branch/main/graph/badge.svg?token=PCOHJETYCD)](https://codecov.io/gh/CSC510-Software-Engineering-Fall-2024/CityByte)
[![code_size](https://img.shields.io/github/languages/code-size/CSC510-Software-Engineering-Fall-2024/CityByte)](https://github.com/CSC510-Software-Engineering-Fall-2024/CityByte) 
[![repo_size](https://img.shields.io/github/repo-size/CSC510-Software-Engineering-Fall-2024/CityByte)](https://github.com/CSC510-Software-Engineering-Fall-2024/CityByte)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14026837.svg)](https://doi.org/10.5281/zenodo.14026837)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/CSC510-Software-Engineering-Fall-2024/CityByte.svg)](https://GitHub.com/CSC510-Software-Engineering-Fall-2024/CityByte/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/CSC510-Software-Engineering-Fall-2024/CityByte.svg)](https://GitHub.com/CSC510-Software-Engineering-Fall-2024/CityByte/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub version](https://img.shields.io/github/v/release/CSC510-Software-Engineering-Fall-2024/CityByte)](https://github.com/CSC510-Software-Engineering-Fall-2024/CityByte/tree/v3.0.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code linting: flake8](https://img.shields.io/badge/code%20linting-flake8-blue.svg)](https://flake8.pycqa.org/en/latest/)


## Introduction
Ready to explore? CityByte is the perfect tool to prepare for a trip or just virtually wander the globe. We've been hard at work to deliver new features, and we hope you enjoy. Below you can find an explination of recent updates, information about this codebase, and even how to host it yourself!

### Start Guide
The start guide can be found in the <a href = https://github.com/CSC510-Software-Engineering-Fall-2024/CityByte/blob/main/INSTALL.md> INSTALL.md </a> file.

### Updates! - Phase 3
* Multiple pins on map - quick and easy way to check multiple places one time on the map
* Sheduling and Organizing Improvements - Itinerary items can now be arranged according to the date and time they have been scheduled at!
* Summarization of Trip Itinerary - Save the locations you want to go in each city so you don't forget and review all your favorites locations!

#### About CityByte!

#### Tech Update
https://www.youtube.com/watch?v=LJNfWGS4qw8

#### Animated pitch
https://github.com/user-attachments/assets/5005718f-2813-4870-ae0d-4223904f414c

### Old Project - Phase 1 & 2
The old project's updates can be seen by going to the `old` branch and navigating to that README. In short, Phase 1 was the project's initial creation via command line and Phase 2 was transitioning to a webapp, creating user accounts, and using caching to reduce system crashes and increase overall speed. Project 2 from prior team was trying to add logins, UI improvements and Trip Itinerary.

## Automatic Tools - GitHub Actions
 
First, credit to the prior team's members. They made the project easy to pick up and use and most of the automated tools used for this come from them. We hope that we've ensured the project is as easy to pick up and use as them (if not more so).

We use GitHub actions to automate tasks of linting, code coverage, build, tests, and security checks. The codes that perform these actions are stored as `.yml` files in the `.github/workflows` directory. The GitHub actions are triggered whenever something is pushed (or pulled) into the remote repository. The results of these automated tasks are shown as badges at the top of this README.md file. 

### Unit tests:

Unit test are performed everytime there is a push or pull into the repository. They are present in `/search/tests.py`. 

### Code Coverage: 

Code Coverage is an important metric that allows us to understand how much of the codebase is tested. `django.yml` performs this task. For more information about Code Coverage, please visit this [link](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage). 

### Flake8 - Code Linting:

We are using Flake8 for linting and syntax checking, and it is performed by `Linting.yml`. For more information about Flake8, please visit this [link](https://medium.com/python-pandemonium/what-is-flake8-and-why-we-should-use-it-b89bd78073f2).
Use flake8 before you push code to GitHub. </br>
Config file present in `.flake8`.

```
flake8 <directory>
```

### Black - Code Formatter

We are using the Black code formatter to format our code before pushing it to GitHub. For more information about Black, please visit this [link](https://black.readthedocs.io/en/stable/).
Config file in `pyproject.toml`.

Run the line below every time you push to GitHub.</br>
```
black --line-length 120 <filename>
```

If you prefer using Black in VSCode, you can add the below settings in your vscode settings:

```
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "120"],
    "python.linting.enabled": true
}
```
  
### Pre Commit Hooks for Black Code formatting and Flake8 Linting
Run  `pre-commit install` to automatically enable Black and Flake8 upon commits.

## License
Distributed under the MIT License. See `LICENSE.md` for more information

## Support
Concerns with the software? Please get in touch with us via one of the methods below. We are delighted to address any queries you may have about the program.

Please contact us if you experience any problems with the setting up the problem or would like help understanding the code. You can email us at gunabanagroup [at] gmail [dot] com or by clicking the icon below.

<a href = "mailto:gunabanagroup@gmail.com">
<img width = "35px" src = "https://user-images.githubusercontent.com/73664200/194786335-12b1d3a6-b272-4896-9bd7-d615e28847f3.png"/>
</a>

## Current Members
* Dharani Guda - dguda
* Archismita Ghosh - aghosh7

## Prior Team's Members
* Brody Bond - bbond
* Chaitanya Nagulapalli - cknagula
* Tristan Hall - tdhall6

## Prior Team's Members
1. Rohit Geddam: sgeddam2@ncsu.edu
2. Arun Kumar Ramesh - arames25@ncsu.edu
3. Kiron Jayesh - kjayesh@ncsu.edu
4. Sai Krishna Teja Varma - smanthe@ncsu.edu
5. Shandler Mason - samason4@ncsu.edu

## Prior Prior Team's Members
* Nirav Shah - nshah28
* Vishwa Gandhi - vgandhi
* Pradyumna Khawas - ppkhawas
* Vrushanki Patel - vpatel25
* Priya Saroj - pbsaroj

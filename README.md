<p align="center"><img width="100" src="./client/src/assets/logo.png"></p>

<h2 align="center">Melanoma Diagnosis Using CNN</h2>
<h4 align="center">CS470 Team 30</h4>

---

This project aims at examining skin cancer without manpower. Development is ongoing for further features. We are team 30 of CS470, KAIST.

In order to run the full project at localhost, you should run both frontend and backend in development mode. The instructions are as followed.

<br></br>

# Frontend

Frontend is developed with [Vue.js](https://vuejs.org/), a MVVM Javascript framework. Basic designs and UI components are built with [Vuetify](https://vuetifyjs.com/). 
## Installation

Use the package manager [npm](https://www.npmjs.com/) to install necessary packages.
```bash
npm i
```

## Usage

Script for running in localhost is written in **package.json**, so you can just use npm command to run in development mode.
```bash
npm run dev
```

<br></br>

# Backend
Backend is developed with [Flask](https://flask.palletsprojects.com/en/1.1.x/), a micro web framework written in Python.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary packages. Packages are listed in **requirements.txt**.
```bash
pip3 install -r requirements.txt
```

## Usage

Server can run by the following command.
```bash
flask run
```
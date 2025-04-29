# 💼 Job Search App

A Streamlit-based Job Search Application built using the **JSearch API** from RapidAPI.  
Developed by **Neelmani** and **Saara**, this tool allows users to search for jobs across cities in India using rich filters such as location, job experience, remote-only roles, date posted, and more.

---

## 📌 Features

- 🔎 **Search Jobs** by title, keywords, and location
- 📍 **Location Filter** with popular Indian cities
- 🌐 **Remote Jobs** filter toggle
- ⏳ **Date Posted** filter (Today, 3 Days, Week, Month, All Time)
- 🧠 **Experience Required** filter (under 1/3/5 years)
- 📄 View **Job Descriptions** and application links
- 🖼️ **Company Logos** for better visual context
- 📋 Supports **pagination** and adjustable result count
- 📦 Built entirely using **Python** and **Streamlit**

---

## 🚀 How It Works

### 1. User selects job filters from the sidebar:
- Job title/keywords
- City (optional)
- Country code (default: `in`)
- Date posted
- Experience level
- Remote only toggle
- Results per page & page number
- API endpoint: `Search` or `Job Details`

### 2. App sends requests to:
- **`/search`** – to list jobs based on filters
- **`/job-details`** – to get full details for a specific job ID

### 3. Results are displayed dynamically with:
- Job title, company, location
- Source & application links
- Logos and detailed descriptions (expandable)

---

## 🛠️ Technologies Used

| Tool        | Purpose                      |
|-------------|------------------------------|
| [Streamlit](https://streamlit.io/) | Frontend and interactivity |
| [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) | Job search API |
| Python      | Backend logic                |
| http.client | For API request handling     |
| json, urllib | Data parsing and URL encoding |

---

## 🔐 API Key Configuration

To use the app, you need a valid API key from [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch).

### Option 1: Use a Python file for the key
Create a file named `Jobapi_key.py` with:
```python
rapidapi_key = "your_rapidapi_key_here"

import streamlit as st
import http.client
import json
import urllib.parse
from Jobapi_key import rapidapi_key  # Import the API key from a separate file

# Set page config
st.set_page_config(page_title="Job Search App", layout="wide")

# App title and description
st.title("Job Search Application")
st.markdown("by Neelmani and Saara")
st.markdown("Search for jobs using the JSSearch API and view detailed results")

# Sidebar for search parameters
st.sidebar.header("Search Parameters")

# API key input (in sidebar)
# api_key = st.sidebar.text_input("RapidAPI Key", value=rapidapi_key, type="password")
api_key= rapidapi_key
# Search query
query = st.sidebar.text_input("Job Title/Keywords", value="react developer")

# Location options
location_options = ["Mumbai", "Bengaluru", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Any"]
location = st.sidebar.selectbox("Location", location_options)

# Country
country = st.sidebar.text_input("Country Code", value="in")

# Date posted options
date_posted_options = ["All time", "Today", "3days", "Week", "Month"]
date_posted = st.sidebar.selectbox("Date Posted", date_posted_options)

# Job requirements
job_req_options = ["No preference", "Under 1 year", "Under 3 years", "Under 5 years"]
job_req_mapping = {
    "No preference": "",
    "Under 1 year": "years1under",
    "Under 3 years": "years3under",
    "Under 5 years": "years5under"
}
job_req = st.sidebar.selectbox("Experience Required", job_req_options)

# Remote only
remote_only = st.sidebar.checkbox("Remote only")

# Results per page
page_size = st.sidebar.slider("Results per page", min_value=1, max_value=20, value=10)

# Page number
page = st.sidebar.number_input("Page number", min_value=1, max_value=10, value=1)

# API endpoint options
endpoint_options = ["Search", "Job Details"]
endpoint = st.sidebar.selectbox("API Endpoint", endpoint_options)

# Job ID input (only displayed if Job Details endpoint is selected)
job_id = ""
if endpoint == "Job Details":
    job_id = st.sidebar.text_input("Job ID", value="fZV6GpbKsUxO-7fnAAAAAA==")

# Search button
search_button = st.sidebar.button("Search Jobs")

# Function to make API request for job search
def search_jobs():
    conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
    
    # Build search query string
    search_query = query
    if location != "Any":
        search_query += f" in {location}"
    
    # URL encode the search query
    encoded_query = urllib.parse.quote(search_query)
    
    # Start building the endpoint URL
    endpoint_url = f"/search?query={encoded_query}&page={page}&num_pages=1&country={country}"
    
    # Add date posted if not "All time"
    if date_posted != "All time":
        endpoint_url += f"&date_posted={date_posted.lower()}"
    
    # Add job requirements if selected
    job_req_value = job_req_mapping[job_req]
    if job_req_value:
        endpoint_url += f"&job_requirements={job_req_value}"
    
    # Add remote jobs parameter if selected
    if remote_only:
        endpoint_url += "&remote_jobs_only=true"
    
    # Add page size parameter
    endpoint_url += f"&page_size={page_size}"
    
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': "jsearch.p.rapidapi.com"
    }
    
    try:
        conn.request("GET", endpoint_url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

# Function to make API request for job details
def get_job_details(job_id):
    conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
    
    # URL encode the job ID
    encoded_job_id = urllib.parse.quote(job_id)
    endpoint_url = f"/job-details?job_id={encoded_job_id}&country={country}"
    
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': "jsearch.p.rapidapi.com"
    }
    
    try:
        conn.request("GET", endpoint_url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

# Display results
if search_button:
    with st.spinner("Searching for jobs..."):
        if endpoint == "Search":
            response_data = search_jobs()
        else:  # Job Details
            response_data = get_job_details(job_id)
        
        # Check if there's an error
        if "error" in response_data:
            st.error(f"Error: {response_data['error']}")
        else:
            # Show raw JSON in expandable section
            with st.expander("Raw JSON Response"):
                st.json(response_data)
            
            # Extract and display job information
            if response_data.get("status") == "OK" and "data" in response_data:
                jobs = response_data["data"]
                
                if not jobs:
                    st.warning("No jobs found matching your criteria.")
                else:
                    st.subheader(f"Found {len(jobs)} jobs")
                    
                    # Process each job
                    for idx, job in enumerate(jobs):
                        # Create job card
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                # Title and company
                                st.markdown(f"### {job.get('job_title', 'N/A')}")
                                st.markdown(f"**Company:** {job.get('employer_name', 'N/A')}")
                                
                                # Location
                                location_text = f"{job.get('job_city', 'N/A')}, {job.get('job_state', 'N/A')}, {job.get('job_country', 'N/A')}"
                                st.markdown(f"**Location:** {location_text}")
                                
                                # Posted date
                                st.markdown(f"**Posted:** {job.get('job_posted_at', 'N/A')}")
                                
                                # Job board and application links
                                st.markdown(f"**Source:** {job.get('job_publisher', 'N/A')}")
                                
                                # Display all apply options
                                if job.get('apply_options'):
                                    apply_links = []
                                    for option in job.get('apply_options', []):
                                        portal = option.get('publisher', 'Unknown')
                                        link = option.get('apply_link', '#')
                                        apply_links.append(f"[{portal}]({link})")
                                    
                                    st.markdown("**Apply on:** " + " | ".join(apply_links))
                                else:
                                    # Fallback to main apply link
                                    apply_link = job.get('job_apply_link', '#')
                                    st.markdown(f"**Apply Link:** [Apply]({apply_link})")
                            
                            with col2:
                                # Company logo if available
                                logo_url = job.get('employer_logo')
                                if logo_url:
                                    st.image(logo_url, width=100)
                                
                                # Job details link
                                if job.get('job_id'):
                                    st.markdown(f"**Job ID:** `{job.get('job_id')}`")
                            
                            # Job description (in expandable section)
                            with st.expander("Job Description"):
                                st.markdown(job.get('job_description', 'No description available'))
                            
                            # Add separator between jobs
                            st.markdown("---")
                            
                    # Display pagination info
                    current_page = response_data.get("parameters", {}).get("page", 1)
                    total_pages = response_data.get("parameters", {}).get("num_pages", 1)
                    st.markdown(f"Page {current_page} of {total_pages}")

# Initial app state - show instructions
if not search_button:
    st.info("👈 Set your search parameters in the sidebar and click 'Search Jobs' to begin")
    
    # Sample JSON format for reference
    st.subheader("Sample JSON Output Format")
    sample_job = {
        "company_name": "Example Corp",
        "title": "React Developer",
        "job_description": "We are looking for a skilled React developer...",
        "job_board_link": "https://example.com/job-board",
        "application_link": "https://example.com/apply",
        "posted_date": "3 days ago",
        "location": "Mumbai, Maharashtra",
        "portal_name": "LinkedIn"
    }
    st.json(sample_job)
    
    # Show example URL format
    st.subheader("API URL Format Example")
    st.code("/search?query=react%20developer%20in%20mumbai&page=1&num_pages=1&country=in&date_posted=3days&job_requirements=years3under")
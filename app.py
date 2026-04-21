# ==============================================================================
# STEP 1: IMPORTING LIBRARIES (Zaroori modules import kar rahe hain)
# ==============================================================================
import streamlit as st
import pandas as pd
import mysql.connector
import datetime
import base64

# ==============================================================================
# STEP 2: PAGE CONFIGURATION & ENTERPRISE UI STYLING (CSS)
# ==============================================================================
# Project Name Updated: Degree Calling Analysis
st.set_page_config(page_title="Degree Calling Analysis", page_icon="📞", layout="wide")

# CSS Styling sirf beautification ke liye (Koi option hide nahi kiya gaya hai)
st.markdown("""
<style>
    /* Main Title par premium blue gradient color lagana */
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1px;
    }
    
    /* Sleek Glassmorphism Input Fields */
    .stTextInput>div>div>input, 
    .stDateInput>div>div>input, 
    .stSelectbox>div>div>div {
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease-in-out !important;
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: white !important;
    }
    .stTextInput>div>div>input:focus, 
    .stDateInput>div>div>input:focus, 
    .stSelectbox>div>div>div:focus,
    .stTextInput>div>div>input:hover, 
    .stDateInput>div>div>input:hover, 
    .stSelectbox>div>div>div:hover {
        border-color: #00f2fe !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.25) !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
    }

    /* Login Form ki default border ko chhupana taaki clean dikhe */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }

    /* Data Tables (DataFrames) ko premium borders aur shadow dena */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .stDataFrame:hover {
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.15);
        border-color: rgba(0, 242, 254, 0.3);
        transition: 0.3s ease;
    }

    /* VIP Professional Buttons & Download Buttons */
    .stButton>button, .stFormSubmitButton>button, .stDownloadButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease !important;
        padding: 10px 24px !important;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover, .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #ffffff !important;
        border: 1px solid transparent !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Info Boxes (First Login Tracker) */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        background-color: rgba(0, 242, 254, 0.05) !important;
        color: #e2e8f0 !important;
        backdrop-filter: blur(10px);
    }

    /* Layout ko bada karne ke liye max-width ko 96% karna */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 96% !important;
    }
    
    /* --- SIDEBAR ALIGNMENT & EXTRA SPACE REMOVAL --- */
    [data-testid="stSidebar"] { text-align: center; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 { text-align: center !important; }
    [data-testid="stSidebar"] label p { text-align: center !important; width: 100% !important; display: block !important; }
    [data-testid="stSidebar"] input { text-align: center !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="ValueContainer"] { justify-content: center !important; }
    [data-testid="stSidebar"] [data-testid="stAlert"] { display: flex; justify-content: center; text-align: center; }
    [data-testid="stSidebarHeader"] { padding-top: 1rem !important; padding-bottom: 0rem !important; min-height: auto !important; }
    [data-testid="stSidebarUserContent"] { padding-top: 0rem !important; }
    hr { border-color: rgba(255, 255, 255, 0.1) !important; margin-top: 1rem !important; margin-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# STEP 3: USER CREDENTIALS & LOGIN SYSTEM 
# ==============================================================================
USERS = {
    "hx1001": {"pwd": "hx1001", "name": "Vipul Bhatnagar"},
    "hx1192": {"pwd": "hx1192", "name": "Vipin Rawat"},
    "hx1464": {"pwd": "hx1464", "name": "Pramod Kumar"},
    "hx0000": {"pwd": "hx0000", "name": "Devender"},
    "hx0335": {"pwd": "hx0335", "name": "Vinay Solanki"} 
}

@st.cache_resource
def get_daily_login_tracker():
    return {}

def generate_token(uname):
    tracker = get_daily_login_tracker()
    today_str = str(datetime.date.today())
    
    if today_str not in tracker:
        tracker.clear() 
        tracker[today_str] = {}
        
    if uname not in tracker[today_str]:
        ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        tracker[today_str][uname] = datetime.datetime.now(ist_timezone).strftime("%d %b %Y %H:%M")
        
    login_time = tracker[today_str][uname]
    raw = f"{uname}|{datetime.date.today()}|{login_time}"
    return base64.b64encode(raw.encode()).decode()

def verify_token(token):
    try:
        raw = base64.b64decode(token).decode()
        parts = raw.split("|")
        if len(parts) == 3:
            uname, date_str, login_time = parts
            if date_str == str(datetime.date.today()) and uname in USERS:
                return uname, login_time
    except:
        pass
    return None, None

def check_password():
    if "token" in st.query_params:
        valid_user, login_time = verify_token(st.query_params["token"])
        if valid_user:
            st.session_state["password_correct"] = True
            st.session_state["username"] = valid_user
            st.session_state["current_user"] = USERS[valid_user]["name"]
            st.session_state["login_time"] = login_time

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = None 

    def password_entered():
        uname = st.session_state["username_input"].strip().lower()
        pwd = st.session_state["password_input"].strip().lower()
        
        if uname in USERS and USERS[uname]["pwd"] == pwd:
            st.session_state["password_correct"] = True
            st.session_state["username"] = uname
            st.session_state["current_user"] = USERS[uname]["name"]
            new_token = generate_token(uname)
            st.query_params["token"] = new_token
            _, login_time = verify_token(new_token)
            st.session_state["login_time"] = login_time
            del st.session_state["password_input"]  
        else:
            st.session_state["password_correct"] = False 

    if not st.session_state.get("password_correct"):
        st.markdown("<br><br><br>", unsafe_allow_html=True) 
        col1, col2, col3 = st.columns([1, 1.5, 1]) 
        with col2:
            st.markdown("<h3 style='text-align: center; color: #94a3b8; font-weight: 500; letter-spacing: 2px; margin-bottom: -15px;'>HERO VIRED PVT LTD.</h3>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; font-size: 36px;'>🔐 <span class='gradient-text'>Degree Calling Analysis Login</span></h1>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.text_input("Username", key="username_input")
                st.text_input("Password", type="password", key="password_input")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Secure Login", use_container_width=True, on_click=password_entered)
            
            if st.session_state["password_correct"] == False:
                st.error("😕 Invalid Username or Password")
        return False
    return True

# ==============================================================================
# STEP 4: MAIN DASHBOARD & SIDEBAR LAYOUT
# ==============================================================================
if check_password():
    
    # --- SIDEBAR CREATION ---
    st.sidebar.markdown("<div style='text-align: center; margin-top: -10px; margin-bottom: 5px;'><small style='color: #94a3b8;'><b>Created By Vinay Solanki (HX0335)</b></small></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0px;'>Hero Vired Pvt Ltd.</h2>", unsafe_allow_html=True)
    
    st.sidebar.markdown(f"<div style='text-align: center; border-radius: 8px; border: 1px solid rgba(0, 200, 0, 0.3); background-color: rgba(0, 150, 0, 0.05); padding: 5px; color: #e2e8f0; margin-top: 5px; margin-bottom: 5px;'><p style='margin: 0; font-weight: 600;'>Welcome {st.session_state['current_user']}</p></div>", unsafe_allow_html=True)
    
    if "login_time" in st.session_state:
        st.sidebar.markdown(f"<div style='text-align: center; border-radius: 8px; border: 1px solid rgba(0, 242, 254, 0.3); background-color: rgba(0, 242, 254, 0.05); padding: 5px; color: #e2e8f0; margin-top: 5px; margin-bottom: 5px;'><p style='margin: 0; font-weight: 600;'>🕒 First Login: {st.session_state['login_time']}</p></div>", unsafe_allow_html=True)
        
    st.sidebar.markdown("---")
    
    # ---------------------------------------------------------
    # REPORTS DROPDOWN (For 8-10 Scripts)
    # ---------------------------------------------------------
    st.sidebar.markdown("<h3 style='text-align: center; color: #00f2fe;'>📊 Select Report</h3>", unsafe_allow_html=True)
    report_list = [
        "Calling LC Level", 
        "Report 2 (Coming Soon...)", 
        "Report 3 (Coming Soon...)"
    ]
    selected_report = st.sidebar.selectbox("Choose a script to run:", report_list, label_visibility="collapsed")
    
    st.sidebar.markdown("---")
    
    # Refresh Button
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # ---------------------------------------------------------
    # SMART DATE LOGIC (Restrict to Last 3 Months)
    # ---------------------------------------------------------
    today = datetime.date.today()
    
    if today.month <= 2:
        min_month = today.month + 10
        min_year = today.year - 1
    else:
        min_month = today.month - 2
        min_year = today.year
        
    min_allowed_date = datetime.date(min_year, min_month, 1)
    
    start_date = st.sidebar.date_input("Start Date", value=today.replace(day=1), min_value=min_allowed_date, max_value=today)
    end_date = st.sidebar.date_input("End Date", value=today, min_value=min_allowed_date, max_value=today)
    
    st.sidebar.markdown("---")
    
    # Logout Button
    if st.sidebar.button("Logout", use_container_width=True):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()

    # Main Dashboard Title
    st.markdown("<h1>📞 <span class='gradient-text'>Degree Calling Analysis Dashboard</span></h1>", unsafe_allow_html=True)
    st.markdown(f"#### Currently Viewing: `{selected_report}`")

# ==============================================================================
# STEP 5: SQL DATA FETCHING FUNCTIONS 
# ==============================================================================
    
    @st.cache_data(ttl=600) 
    def load_calling_script_data(start_dt, end_dt):
        try:
            conn = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                port=st.secrets["mysql"]["port"],
                database=st.secrets["mysql"]["database"],
                user=st.secrets["mysql"]["username"],
                password=st.secrets["mysql"]["password"]
            )
            
            query = f"""
            SELECT
                t.dial_date,
                DAYNAME(t.dial_date) AS day_of_week,
                t.lc_email,
                CASE WHEN t.Total_Dials_Calls > 5 THEN 'Present' ELSE 'Absent' END AS attendance,
                t.Total_Dials_Calls AS total_dials_calls,
                t.Unique_Leads AS unique_leads,
                t.Answered AS answered,
                CONCAT(IFNULL(ROUND(CASE WHEN t.Total_Dials_Calls = 0 THEN 0 ELSE (t.Answered / t.Total_Dials_Calls) * 100 END, 2), 0), '%') AS conn_per,
                t.Unique_Answered AS unique_answered,
                CONCAT(IFNULL(ROUND((t.Unique_Answered / NULLIF(t.Unique_Leads, 0)) * 100, 2), 0), '%') AS unique_conn_per,
                IFNULL(TIME_FORMAT(SEC_TO_TIME(t.Talktime_Seconds), '%H:%i:%s'), '00:00:00') AS talktime,
                CONCAT(IFNULL(ROUND((t.Calls_30_Sec / NULLIF(t.Total_Dials_Calls, 0)) * 100, 2), 0), '%') AS calls_30_sec_per,
                t.`2_Minutes_Call` AS calls_2_mins,
                t.`5_Minutes_Call` AS calls_5_mins
            FROM (
                SELECT
                    DATE_FORMAT(DATE_ADD(cscl.Date_Entered, INTERVAL 330 MINUTE), '%Y-%m-%d') AS dial_date,
                    CASE WHEN cscl.owner LIKE '%@%' THEN cscl.owner ELSE IFNULL(user_info.email_address, 'N/A') END AS lc_email,
                    SUM(CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' THEN 1 ELSE 0 END) AS Total_Dials_Calls,
                    COUNT(DISTINCT CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' THEN RIGHT(cscl.mx_custom_2, 10) END) AS Unique_Leads,
                    SUM(CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' AND cscl.mx_custom_5 > 0 THEN 1 ELSE 0 END) AS Answered,
                    COUNT(DISTINCT CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' AND cscl.mx_custom_5 > 0 THEN RIGHT(cscl.mx_custom_2, 10) END) AS Unique_Answered,
                    SUM(CASE WHEN LOWER(cscl.mx_custom_1) IN ('outgoing', 'incoming') THEN cscl.mx_custom_5 ELSE 0 END) AS Talktime_Seconds,
                    COUNT(CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' AND cscl.mx_custom_5 >= 30 THEN 1 END) AS Calls_30_Sec,
                    SUM(CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' AND cscl.mx_custom_5 > 30 AND cscl.mx_custom_5 <= 120 THEN 1 ELSE 0 END) AS `2_Minutes_Call`,
                    SUM(CASE WHEN LOWER(cscl.mx_custom_1) = 'outgoing' AND cscl.mx_custom_5 > 120 AND cscl.mx_custom_5 <= 300 THEN 1 ELSE 0 END) AS `5_Minutes_Call`
                FROM crm_supreconnect_call_log cscl
                LEFT JOIN (
                    SELECT
                        u.id,
                        MIN(ea.email_address) AS email_address
                    FROM users u
                    INNER JOIN email_addr_bean_rel eabr
                        ON u.id = eabr.bean_id
                        AND eabr.bean_module = 'Users'
                        AND eabr.deleted = 0
                    INNER JOIN email_addresses ea
                        ON eabr.email_address_id = ea.id
                        AND ea.deleted = 0
                    GROUP BY u.id
                ) AS user_info
                    ON cscl.owner = user_info.id
                WHERE DATE(DATE_ADD(cscl.Date_Entered, INTERVAL 330 MINUTE)) BETWEEN '{start_dt}' AND '{end_dt}'
                AND cscl.mx_custom_4 = 'degree'
                GROUP BY
                    DATE_FORMAT(DATE_ADD(cscl.Date_Entered, INTERVAL 330 MINUTE), '%Y-%m-%d'),
                    CASE WHEN cscl.owner LIKE '%@%' THEN cscl.owner ELSE IFNULL(user_info.email_address, 'N/A') END
            ) t
            ORDER BY t.dial_date DESC, t.lc_email ASC
            """
            df = pd.read_sql(query, conn)
            conn.close()
            
            df.rename(columns={
                'dial_date': 'Dial Date',
                'day_of_week': 'Day of Week',
                'lc_email': 'LC Email',
                'attendance': 'Attendance',
                'total_dials_calls': 'Total Dials Calls',
                'unique_leads': 'Unique Leads',
                'answered': 'Answered',
                'conn_per': 'Conn %',
                'unique_answered': 'Unique Answered',
                'unique_conn_per': 'Unique Conn %',
                'talktime': 'Talktime',
                'calls_30_sec_per': '30 Sec Conn %',
                'calls_2_mins': '2 Minutes Call',
                'calls_5_mins': '5 Minutes Call'
            }, inplace=True)
            
            return df
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return pd.DataFrame()

# ==============================================================================
# STEP 6: DYNAMIC REPORT RENDERING
# ==============================================================================
    
    if selected_report == "Calling LC Level":
        with st.spinner("Fetching Data from Database... Please wait."):
            report_df = load_calling_script_data(start_date, end_date)
            
        if not report_df.empty:
            search_lc = st.text_input("🔍 Search by LC Email...", placeholder="Type here to filter data by LC...")
            
            if search_lc:
                if 'LC Email' in report_df.columns:
                    mask = report_df['LC Email'].astype(str).str.contains(search_lc, case=False, na=False)
                    display_report_df = report_df[mask]
                else:
                    display_report_df = report_df
            else:
                display_report_df = report_df
                
            colA, colB = st.columns([8, 2])
            with colB:
                st.download_button(
                    label="📥 Download CSV", 
                    data=display_report_df.to_csv(index=False).encode('utf-8'), 
                    file_name=f"Calling_LC_Level_{start_date}_to_{end_date}.csv", 
                    mime="text/csv", 
                    use_container_width=True
                )
            
            st.dataframe(display_report_df, use_container_width=True, height=min(750, (len(display_report_df) + 1) * 36 + 10))
            st.caption(f"Total Rows Fetched: {len(display_report_df)}")
        else:
            st.info("No data found for the selected date range.")

    elif selected_report == "Report 2 (Coming Soon...)":
        st.info("This report module is under construction. Please provide the SQL script to activate it.")
        
    elif selected_report == "Report 3 (Coming Soon...)":
        st.info("This report module is under construction. Please provide the SQL script to activate it.")

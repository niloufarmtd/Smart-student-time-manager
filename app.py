import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# --------------------------------
# Page Config
# --------------------------------
st.set_page_config(
    page_title="🎓 مدیر زمان هوشمند دانشجویان",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# Custom CSS for RTL and Beautiful Design
# --------------------------------
st.markdown("""
<style>
    /* RTL Direction */
    .stApp, .stMarkdown, .stText, .stTitle, .stSubheader, 
    .stMetric, .stDataFrame, .stAlert, .stButton, div, p, h1, h2, h3, h4, h5, h6 {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Vazir', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 20px;
        color: white;
    }
    
    /* Header Styling */
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* Card Styling */
    .metric-card {
        padding: 25px 15px;
        border-radius: 20px;
        background: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Task Cards */
    .task-card {
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateX(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }
    
    .task-high {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        color: white;
    }
    
    .task-medium {
        background: linear-gradient(135deg, #4ECDC4 0%, #6DECE6 100%);
        color: white;
    }
    
    .task-low {
        background: linear-gradient(135deg, #96CEB4 0%, #B8E6B8 100%);
        color: #333;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 15px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .success-btn {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%) !important;
        color: white !important;
    }
    
    .warning-btn {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFA07A 100%) !important;
        color: white !important;
    }
    
/* Sidebar Styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F9F7FE 100%) !important;
    border-left: 3px solid var(--accent-1) !important;
}

/* Sidebar Headers - سفید کردن متن‌های عنوان */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3,
[data-testid="stSidebar"] .stMarkdown h4,
[data-testid="stSidebar"] .stMarkdown h5,
[data-testid="stSidebar"] .stMarkdown h6 {
    color: var(--primary-dark) !important; /* یا color: #6C5CE7 !important; */
    font-weight: 700 !important;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

/* Sidebar Paragraphs - بهبود خوانایی متن‌های معمولی */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] span {
    color: var(--text-dark) !important;
}

/* Sidebar Metric Values */
[data-testid="stSidebar"] .stMetric {
    color: var(--primary-dark) !important;
}

/* Sidebar Labels and Captions */
[data-testid="stSidebar"] .stCaption {
    color: var(--text-light) !important;
}
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4ECDC4, #45B7D1, #96CEB4);
        border-radius: 10px;
    }
    
    /* Schedule Time Slot */
    .time-slot {
        background: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-right: 5px solid #667eea;
    }
    
    /* Icon Styling */
    .icon-large {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Title with Beautiful Design
# --------------------------------
st.markdown("""
<div class="main fade-in">
    <h1 class="header-title">🎓 مدیر زمان هوشمند دانشجویان</h1>
    <h4 style="text-align: center; color: white; opacity: 0.9;">MVP | سیستم هوشمند مدیریت زمان با یادگیری تطبیقی</h4>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# Smart Logic Functions
# --------------------------------
def urgency_score(deadline):
    days_left = (deadline - date.today()).days
    if days_left <= 1:
        return 10
    elif days_left <= 3:
        return 7
    elif days_left <= 7:
        return 4
    return 1

def importance_score(title):
    title = title.lower()
    if "امتحان" in title or "آزمون" in title:
        return 10
    elif "پروژه" in title:
        return 8
    elif "تمرین" in title or "تکلیف" in title:
        return 5
    elif "مقاله" in title or "تحقیق" in title:
        return 6
    return 3

def calculate_priority(task, course_history=None):
    base_score = round(
        urgency_score(task["deadline"]) * 0.5 +
        importance_score(task["title"]) * 0.4 +
        task["estimated_time"] * 0.1,
        2
    )
    
    if course_history and task["course"] in course_history:
        delay_count = course_history[task["course"]].get("delay_count", 0)
        if delay_count > 0:
            adaptive_boost = min(delay_count * 0.5, 3.0)
            base_score += adaptive_boost
    
    return round(base_score, 2)

def get_priority_color(priority):
    if priority >= 7:
        return "task-high"
    elif priority >= 4:
        return "task-medium"
    else:
        return "task-low"

# --------------------------------
# Session State Initialization
# --------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []

if "course_history" not in st.session_state:
    st.session_state.course_history = {}

if "daily_schedule" not in st.session_state:
    st.session_state.daily_schedule = []

# --------------------------------
# Helper Functions
# --------------------------------
def update_course_history(course, delayed=False):
    if not course:
        return
    
    if course not in st.session_state.course_history:
        st.session_state.course_history[course] = {
            "total_tasks": 0,
            "completed_on_time": 0,
            "delay_count": 0
        }
    
    st.session_state.course_history[course]["total_tasks"] += 1
    
    if delayed:
        st.session_state.course_history[course]["delay_count"] += 1
    else:
        st.session_state.course_history[course]["completed_on_time"] += 1

def generate_daily_schedule():
    if not st.session_state.tasks:
        return []
    
    df = pd.DataFrame(st.session_state.tasks)
    df = df[~df.get("completed", False)]  # فقط کارهای تکمیل نشده
    df = df.sort_values(by="priority", ascending=False)
    
    today_tasks = df.head(4).copy()
    
    time_slots = [
        "۸:۰۰ - ۱۰:۰۰ صبح",
        "۱۰:۰۰ - ۱۲:۰۰ ظهر", 
        "۱۳:۰۰ - ۱۵:۰۰ بعدازظهر",
        "۱۵:۰۰ - ۱۷:۰۰ عصر"
    ]
    
    schedule = []
    for i, (_, task) in enumerate(today_tasks.iterrows()):
        if i < len(time_slots):
            schedule.append({
                "زمان": time_slots[i],
                "کار": task["title"],
                "درس": task["course"],
                "مدت": f"{task['estimated_time']} ساعت",
                "اولویت": task["priority"],
                "رنگ": get_priority_color(task["priority"])
            })
    
    st.session_state.daily_schedule = schedule
    return schedule

def check_smart_alerts():
    alerts = []
    
    if not st.session_state.tasks:
        return alerts
    
    today = date.today()
    
    for task in st.session_state.tasks:
        if task.get("completed", False):
            continue
            
        days_left = (task["deadline"] - today).days
        course = task["course"]
        
        if days_left < 0:
            alerts.append({
                "type": "error",
                "message": f"⏰ مهلت '{task['title']}' گذشته است!",
                "priority": "high"
            })
        elif days_left == 0:
            alerts.append({
                "type": "warning",
                "message": f"🔥 امروز آخرین مهلت '{task['title']}' است!",
                "priority": "high"
            })
        elif days_left == 1:
            alerts.append({
                "type": "warning", 
                "message": f"⚠️ فردا مهلت تحویل '{task['title']}' است",
                "priority": "medium"
            })
        
        if course in st.session_state.course_history:
            history = st.session_state.course_history[course]
            if history.get("delay_count", 0) > 2 and days_left <= 3:
                alerts.append({
                    "type": "info",
                    "message": f"📊 در درس '{course}' تأخیر زیادی داشته‌اید! این کار را سریع شروع کنید",
                    "priority": "medium"
                })
    
    return sorted(alerts, key=lambda x: x["priority"], reverse=True)[:5]  # فقط ۵ هشدار اول

def create_progress_chart():
    if not st.session_state.tasks:
        return None
    
    df = pd.DataFrame(st.session_state.tasks)
    completed = len([t for t in st.session_state.tasks if t.get("completed", False)])
    total = len(st.session_state.tasks)
    
    fig = go.Figure(data=[
        go.Pie(
            labels=['تکمیل شده', 'در انتظار'],
            values=[completed, total - completed],
            hole=.6,
            marker_colors=['#4ECDC4', '#FF6B6B']
        )
    ])
    
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=0, b=0, l=0, r=0),
        height=250
    )
    
    return fig

# --------------------------------
# Sidebar with Alerts and Stats
# --------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: white;">🚀 پنل مدیریت</h2>
        <p style="color: #a0a0d8;">مدیریت هوشمند زمان تحصیلی</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Smart Alerts
    st.markdown("### 🔔 هشدارهای هوشمند")
    alerts = check_smart_alerts()
    
    if alerts:
        for alert in alerts:
            if alert["type"] == "error":
                st.error(alert["message"])
            elif alert["type"] == "warning":
                st.warning(alert["message"])
            else:
                st.info(alert["message"])
    else:
        st.success("✅ همه کارها تحت کنترل هستند!")
    
    st.markdown("---")
    
    # Course History Stats
    st.markdown("### 📊 آمار دروس")
    if st.session_state.course_history:
        for course, history in list(st.session_state.course_history.items())[:5]:
            if course:
                total = history["total_tasks"]
                completed = history.get("completed_on_time", 0)
                delay = history.get("delay_count", 0)
                
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown(f"**{course}**")
                with col2:
                    if total > 0:
                        success_rate = (completed / total) * 100
                        st.markdown(f"`{int(success_rate)}%`")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### ⚡ آمار سریع")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t.get("completed", False)])
    
    if total_tasks > 0:
        progress = (completed_tasks / total_tasks) * 100
        st.progress(progress / 100)
        st.markdown(f"**{completed_tasks} از {total_tasks} کار تکمیل شده**")
        st.markdown(f"**پیشرفت: {progress:.1f}%**")
    else:
        st.info("هنوز کاری ثبت نشده")

# --------------------------------
# Main Layout
# --------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🏠 داشبورد", "➕ افزودن کار", "📅 برنامه‌ریزی", "📊 تحلیل عملکرد"])

# --------------------------------
# Tab 1: Dashboard
# --------------------------------
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="icon-large">📌</div>
            <h3>کل کارها</h3>
            <h2>{}</h2>
        </div>
        """.format(len(st.session_state.tasks)), unsafe_allow_html=True)
    
    with col2:
        high_priority = len([t for t in st.session_state.tasks if t.get("priority", 0) >= 7])
        st.markdown("""
        <div class="metric-card">
            <div class="icon-large">🔥</div>
            <h3>اولویت بالا</h3>
            <h2>{}</h2>
        </div>
        """.format(high_priority), unsafe_allow_html=True)
    
    with col3:
        completed = len([t for t in st.session_state.tasks if t.get("completed", False)])
        st.markdown("""
        <div class="metric-card">
            <div class="icon-large">✅</div>
            <h3>تکمیل شده</h3>
            <h2>{}</h2>
        </div>
        """.format(completed), unsafe_allow_html=True)
    
    with col4:
        active_courses = len(set([t["course"] for t in st.session_state.tasks if t["course"]]))
        st.markdown("""
        <div class="metric-card">
            <div class="icon-large">📚</div>
            <h3>درس‌های فعال</h3>
            <h2>{}</h2>
        </div>
        """.format(active_courses), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # High Priority Tasks
    st.markdown("### 🔥 کارهای با اولویت بالا")
    if st.session_state.tasks:
        high_tasks = [t for t in st.session_state.tasks if t.get("priority", 0) >= 7 and not t.get("completed", False)]
        
        if high_tasks:
            for task in high_tasks[:3]:
                days_left = (task["deadline"] - date.today()).days
                color_class = get_priority_color(task["priority"])
                
                st.markdown(f"""
                <div class="task-card {color_class} fade-in">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0;">{task['title']}</h4>
                            <p style="margin: 5px 0; opacity: 0.9;">درس: {task['course']} | ⏱ {task['estimated_time']} ساعت</p>
                        </div>
                        <div style="text-align: left;">
                            <h3 style="margin: 0;">🎯 {task['priority']}</h3>
                            <p style="margin: 5px 0;">{days_left} روز باقی‌مانده</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button("✅ تکمیل شد", key=f"complete_{task['title']}_{task['deadline']}", type="primary"):
                        for idx, t in enumerate(st.session_state.tasks):
                            if t["title"] == task["title"] and t["deadline"] == task["deadline"]:
                                st.session_state.tasks[idx]["completed"] = True
                                st.session_state.tasks[idx]["completed_date"] = date.today()
                                
                                delayed = days_left < 0
                                update_course_history(task["course"], delayed)
                                
                                st.success(f"کار '{task['title']}' تکمیل شد!")
                                st.rerun()
        else:
            st.success("🎉 هیچ کار با اولویت بالایی ندارید!")
    else:
        st.info("📝 هنوز کاری ثبت نکرده‌اید. اولین کار خود را اضافه کنید!")
    
    st.markdown("---")
    
    # Progress Chart
    st.markdown("### 📈 نمودار پیشرفت")
    if st.session_state.tasks:
        fig = create_progress_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("برای نمایش نمودار، کارهایی اضافه کنید")

# --------------------------------
# Tab 2: Add Task (با طراحی زیبا)
# --------------------------------
with tab2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px;">
        <h2 style="text-align: center; color: #2D3047;">➕ افزودن کار جدید</h2>
        <p style="text-align: center; color: #666;">اطلاعات کار جدید خود را وارد کنید</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("task_form"):
            st.markdown("### 📝 جزئیات کار")
            
            title = st.text_input("عنوان کار*", placeholder="مثال: پروژه هوش مصنوعی")
            course = st.text_input("نام درس*", placeholder="مثال: هوش مصنوعی")
            
            col_a, col_b = st.columns(2)
            with col_a:
                deadline = st.date_input("مهلت تحویل*", min_value=date.today())
            with col_b:
                estimated_time = st.number_input("زمان تخمینی (ساعت)*", min_value=1, max_value=20, value=2)
            
            priority_tags = st.multiselect(
                "برچسب‌های اولویت",
                ["فوری", "مهم", "پروژه", "امتحان", "تمرین", "مقاله"],
                help="برای تشخیص بهتر اهمیت کار"
            )
            
            description = st.text_area("توضیحات اضافی (اختیاری)", height=100, 
                                      placeholder="جزئیات بیشتر درباره کار...")
            
            submitted = st.form_submit_button("➕ ثبت کار جدید", type="primary")
            
            if submitted and title and course:
                new_task = {
                    "title": title,
                    "course": course,
                    "deadline": deadline,
                    "estimated_time": estimated_time,
                    "priority": calculate_priority({
                        "title": title,
                        "deadline": deadline,
                        "estimated_time": estimated_time,
                        "course": course
                    }, st.session_state.course_history),
                    "status": "در انتظار",
                    "created_date": date.today(),
                    "tags": priority_tags,
                    "description": description,
                    "completed": False
                }
                
                st.session_state.tasks.append(new_task)
                update_course_history(course)
                generate_daily_schedule()
                
                st.balloons()
                st.success("✅ کار جدید با موفقیت اضافه شد!")
    
    with col2:
        st.markdown("### 🎯 پیش‌نمایش اولویت")
        
        if 'title' in locals() and title and course:
            preview_priority = calculate_priority({
                "title": title,
                "deadline": deadline,
                "estimated_time": estimated_time,
                "course": course
            }, st.session_state.course_history)
            
            color_class = get_priority_color(preview_priority)
            
            st.markdown(f"""
            <div class="task-card {color_class}" style="margin-top: 20px;">
                <h4>پیش‌نمایش کار:</h4>
                <p><strong>عنوان:</strong> {title}</p>
                <p><strong>درس:</strong> {course}</p>
                <p><strong>مهلت:</strong> {deadline}</p>
                <p><strong>زمان تخمینی:</strong> {estimated_time} ساعت</p>
                <div style="text-align: center; margin-top: 20px;">
                    <h2>اولویت تخمینی: {preview_priority}</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 💡 نکات هوشمند")
        st.info("""
        - **کارهای با مهلت کمتر از ۲ روز** اولویت بالایی دریافت می‌کنند
        - **کارهای با برچسب 'امتحان'** اهمیت بیشتری دارند
        - **سیستم از عملکرد گذشته شما یاد می‌گیرد** و اولویت‌ها را تنظیم می‌کند
        """)

# --------------------------------
# Tab 3: Planning
# --------------------------------
with tab3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px;">
        <h2 style="text-align: center; color: #2D3047;">📅 برنامه‌ریزی هوشمند</h2>
        <p style="text-align: center; color: #666;">برنامه روزانه شخصی‌سازی شده برای شما</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🗓️ برنامه روزانه پیشنهادی")
        
        if not st.session_state.daily_schedule:
            generate_daily_schedule()
        
        if st.session_state.daily_schedule:
            for i, item in enumerate(st.session_state.daily_schedule):
                st.markdown(f"""
                <div class="time-slot fade-in">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="margin: 0; color: #667eea;">⏰ {item['زمان']}</h4>
                            <h3 style="margin: 10px 0;">{item['کار']}</h3>
                            <p style="margin: 5px 0; color: #666;">📚 {item['درس']} | ⏱ {item['مدت']}</p>
                        </div>
                        <div style="background: #f0f0f0; padding: 10px 15px; border-radius: 10px;">
                            <h4 style="margin: 0;">اولویت</h4>
                            <h2 style="margin: 0; color: #667eea;">{item['اولویت']}</h2>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 کارهایی برای برنامه‌ریزی وجود ندارد. کار جدید اضافه کنید!")
    
    with col2:
        st.markdown("### ⚙️ تنظیمات برنامه")
        
        if st.button("🔄 تولید برنامه جدید", use_container_width=True, type="secondary"):
            generate_daily_schedule()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 📊 بهره‌وری تخمینی")
        if st.session_state.daily_schedule:
            total_hours = sum([int(s['مدت'].split()[0]) for s in st.session_state.daily_schedule])
            efficiency = min(total_hours * 15, 100)  # محاسبه ساده بهره‌وری
            
            st.metric("⏱ زمان کل", f"{total_hours} ساعت")
            st.metric("📈 بهره‌وری تخمینی", f"{efficiency}%")
            
            if efficiency >= 80:
                st.success("🎯 برنامه بسیار مؤثر است!")
            elif efficiency >= 60:
                st.warning("👍 برنامه مناسب است")
            else:
                st.info("💡 می‌توانید بهره‌وری را افزایش دهید")
        
        st.markdown("---")
        
        st.markdown("### 💾 ذخیره برنامه")
        if st.button("📥 ذخیره به PDF", use_container_width=True, disabled=True):
            st.info("این قابلیت در نسخه کامل فعال می‌شود")

# --------------------------------
# Tab 4: Analytics
# --------------------------------
with tab4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px;">
        <h2 style="text-align: center; color: #2D3047;">📊 تحلیل هوشمند عملکرد</h2>
        <p style="text-align: center; color: #666;">تحلیل عملکرد و پیشنهادات بهبود</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 توزیع اولویت‌ها")
            if not df.empty:
                priority_dist = df['priority'].value_counts().sort_index()
                fig1 = px.bar(
                    x=priority_dist.index,
                    y=priority_dist.values,
                    labels={'x': 'سطح اولویت', 'y': 'تعداد کارها'},
                    color=priority_dist.values,
                    color_continuous_scale='Viridis'
                )
                fig1.update_layout(height=300)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("### 📚 توزیع دروس")
            if not df.empty and 'course' in df.columns:
                course_dist = df['course'].value_counts().head(5)
                fig2 = px.pie(
                    values=course_dist.values,
                    names=course_dist.index,
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                fig2.update_layout(height=300, showlegend=True)
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### 🧠 توصیه‌های هوشمند")
        
        if st.session_state.course_history:
            recommendations = []
            
            for course, history in st.session_state.course_history.items():
                if history.get("total_tasks", 0) > 2:
                    delay_rate = (history.get("delay_count", 0) / history["total_tasks"]) * 100
                    
                    if delay_rate > 50:
                        recommendations.append(f"📉 در درس **{course}** تأخیر زیادی دارید ({delay_rate:.0f}%). زمان بیشتری به آن اختصاص دهید.")
                    elif delay_rate > 30:
                        recommendations.append(f"⚠️ در درس **{course}** کمی تأخیر دارید ({delay_rate:.0f}%). برنامه‌ریزی خود را بررسی کنید.")
            
            if recommendations:
                for rec in recommendations[:3]:
                    st.warning(rec)
            else:
                st.success("🎉 عملکرد خوبی دارید! به همین روال ادامه دهید.")
        
        # All Tasks Table
        st.markdown("### 📋 همه کارها")
        
        display_df = df.copy()
        if not display_df.empty:
            display_df['وضعیت'] = display_df.get('completed', False).apply(lambda x: '✅ تکمیل' if x else '⏳ در انتظار')
            display_df['روزهای باقی‌مانده'] = display_df['deadline'].apply(lambda x: (x - date.today()).days)
            
            cols_to_show = ['title', 'course', 'deadline', 'estimated_time', 'priority', 'وضعیت', 'روزهای باقی‌مانده']
            cols_to_show = [c for c in cols_to_show if c in display_df.columns]
            
            st.dataframe(
                display_df[cols_to_show].rename(columns={
                    'title': 'عنوان',
                    'course': 'درس',
                    'deadline': 'مهلت',
                    'estimated_time': 'زمان تخمینی',
                    'priority': 'اولویت'
                }),
                use_container_width=True,
                height=400
            )
    else:
        st.info("📊 برای نمایش تحلیل‌ها، کارهایی اضافه کنید")

# --------------------------------
# Footer
# --------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #2D3047 0%, #1C1E30 100%); border-radius: 15px; color: white;">
    <h3>🎓 مدیر زمان هوشمند دانشجویان</h3>
    <p>MVP نسخه ۲.۰ | توسعه‌یافته توسط فاطمه طاهری و نیلوفر معتمدی</p>
    <p style="opacity: 0.7;">سیستم هوشمند مدیریت زمان با قابلیت یادگیری تطبیقی و برنامه‌ریزی شخصی‌شده</p>
</div>
""", unsafe_allow_html=True)
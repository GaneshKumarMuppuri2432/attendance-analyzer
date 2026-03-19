import streamlit as st
import matplotlib.pyplot as plt
from utils import calculate_attendance, get_status, classes_needed_for_75, predict_future

st.markdown("## 🎓 Smart Attendance Dashboard")
st.markdown("Track your attendance and predict your future 📊")

total_classes = st.number_input("Enter Total Classes", min_value=0, step=1)
attended_classes = st.number_input("Enter Attended Classes", min_value=0, step=1)

if st.button("Analyze"):
    
    # Validation
    if attended_classes > total_classes:
        st.error("Attended classes cannot be more than total classes!")
    
    else:
        # Calculate attendance
        percentage = calculate_attendance(total_classes, attended_classes)
        
        # Get status
        status = get_status(percentage)
        
        # Classes needed
        needed = classes_needed_for_75(total_classes, attended_classes)
        
        # Display results
        st.subheader("📊 Results")
        st.metric(label="Attendance %", value=f"{percentage:.2f}%")        
        if "Safe" in status:
            st.success(f"Status: {status}")
        elif "Almost" in status or "Warning" in status:
            st.warning(f"Status: {status}")
        else:
            st.error(f"Status: {status}")
        st.divider()
        st.subheader("🔮 Future Predictions")

        col1, col2 = st.columns(2)
        
        # LEFT SIDE → Miss
        with col1:
            st.error("📉 If you MISS classes")

            miss_3 = predict_future(total_classes, attended_classes, 3)
            miss_5 = predict_future(total_classes, attended_classes, 5)
            miss_10 = predict_future(total_classes, attended_classes, 10)

            st.write(f"Miss 3 classes → {miss_3:.2f}%")
            st.write(f"Miss 5 classes→ {miss_5:.2f}%")
            st.write(f"Miss 10 classes → {miss_10:.2f}%")


        # RIGHT SIDE → Attend
        with col2:
            st.success("📈 If you ATTEND classes")

            def attend_future(total, attended, extra):
                return ((attended + extra) / (total + extra)) * 100

            attend_3 = attend_future(total_classes, attended_classes, 3)
            attend_5 = attend_future(total_classes, attended_classes, 5)

            st.write(f"Attend 3 classes → {attend_3:.2f}%")
            st.write(f"Attend 5 classes → {attend_5:.2f}%")
        st.divider()
        st.subheader("📈 Attendance Trend")
        future_classes = list(range(0, 11))  # 0 to 10
        
        percentages = []
        
        for i in future_classes:
            percent = ((attended_classes + i) / (total_classes + i)) * 100
            percentages.append(percent)
        fig, ax = plt.subplots()

        ax.plot(future_classes, percentages, marker='o')

        ax.set_xlabel("Future Classes Attended")
        ax.set_ylabel("Attendance %")
        ax.set_title("Attendance Improvement Trend")
        ax.axhline(y=75, linestyle='--', label='Minimum Required (75%)')
        ax.legend()
        st.info("📌 The dashed line represents the minimum required attendance (75%). Stay above this line to remain safe.")
        st.pyplot(fig)
        # Suggestion
        if percentage < 75:
            st.warning(f"⚠️ You must attend {needed} continuous classes to reach 75%")
        else:
            st.success("✅ You are in a safe zone. Maintain consistency!")

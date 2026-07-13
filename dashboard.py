import streamlit as st
import json
import os

# Force wide bento-like presentation window
st.set_page_config(layout="wide", page_title="Curriculum Image Verification")

# Dark cyber minimalist inject styling
st.markdown("""
    
""", unsafe_allow_html=True)

IMAGE_FOLDER = "grade-3-images"
JSON_DATA_PATH = "web_viewer_data.json"

if not os.path.exists(JSON_DATA_PATH):
    st.error(f"Missing clean dataset file! Run your 'prepare_viewer_json.py' pipeline first.")
else:
    with open(JSON_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Sidebar Navigation Column
    st.sidebar.markdown("QUESTIONS SCOPE", unsafe_allow_html=True)
    q_labels = [f"Ch {item['chapter']} — Q {item['question_number']}" for item in data]
    selected_label = st.sidebar.radio("Select an item to verify:", q_labels, label_visibility="collapsed")

    # Extract current item match
    item = data[q_labels.index(selected_label)]

    # 2. Main Bento Column Split View
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(f"CURRICULUM ITEM CONTEXT — CHAPTER {item['chapter']}", unsafe_allow_html=True)
        st.markdown(f"### {item['question']}")
        
        # Render MCQ options if they exist
        if item.get("mcq_options"):
            for opt in item["mcq_options"]:
                st.markdown(f"`{opt}`")
        
        st.markdown("---")
        st.markdown(f"**Expected Answer Key:** {item['correct_answer']}", unsafe_allow_html=True)
        st.markdown("#### Solution Explanation Validation")
        st.write(item.get("explanation", "No description mapped."))

    with col2:
        st.markdown("TARGET PHYSICAL ASSETS", unsafe_allow_html=True)
        
        # Group all assets linked to this index block
        all_assets = [(img, "Base", item.get("image_question_exp", [])) for img in item["image_question"]] + \
                     [(img, "Option", item.get("image_option_exp", [])) for img in item["image_option"]]

        if not all_assets:
            st.info("No local image records passed filters for this question.")
        else:
            for idx, (img, role, exp_list) in enumerate(all_assets):
                img_path = os.path.join(IMAGE_FOLDER, img)
                st.markdown(f"[{role} Asset File]: {img}", unsafe_allow_html=True)
                
                if os.path.exists(img_path):
                    # Streamlit automatically displays the image at full scale inside the column without cropping
                    st.image(img_path, use_container_width=False)
                else:
                    st.error(f"File system mismatch: '{img}' not found inside folder.")
                
                # Target spec caption layout
                desc_text = exp_list[idx] if idx < len(exp_list) else "No structural spec description mapped."
                st.markdown(f"Spec Target: {desc_text}", unsafe_allow_html=True)
                st.markdown("", unsafe_allow_html=True)
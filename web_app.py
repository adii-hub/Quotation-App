import streamlit as st
import pandas as pd
import quotation  # මීට පෙර හැදූ PDF සාදන කේතය
import os

# වෙබ් පිටුවේ සැකසුම්
st.set_page_config(page_title="Sivilima Quotation Generator", page_icon="📄", layout="centered")

st.title("📄 Sivilima - Quotation Generator")
st.markdown("මෙමඟින් ඔබට පහසුවෙන් පාරිභෝගික දත්ත සහ භාණ්ඩ ඇතුළත් කර PDF එකක් සාදාගත හැක.")

# 1. පාරිභෝගික දත්ත අංශය
st.header("1. Customer Details")
col1, col2 = st.columns(2)

with col1:
    c_name = st.text_input("Customer Name")
    c_phone = st.text_input("Phone Number")
with col2:
    c_address = st.text_input("Address")
    c_date = st.text_input("Date", value="2026-08-02")

# 2. භාණ්ඩ දත්ත අංශය
st.header("2. Item Details")
st.write("පහත වගුවට භාණ්ඩ ඇතුළත් කරන්න. අලුත් පේළියක් එක් කිරීමට වගුව පහළින් ඇති ලකුණ ඔබන්න.")

# ආරම්භක දත්ත වගුව (Default table)
initial_data = pd.DataFrame([
    {"Description": "", "Quantity": 1, "Unit Price (LKR)": 0.0}
])

# Excel වැනි දත්ත ඇතුළත් කරන වගුව
edited_df = st.data_editor(initial_data, num_rows="dynamic", use_container_width=True)

st.divider()

# 3. අමතර කරුණු (Terms & Conditions) අංශය - අලුතින් එකතු කළ කොටස
st.header("3. Terms & Conditions (Optional)")
st.write("අමතර කොන්දේසි (උදා: වගකීම් කාලය, ගෙවීම් විස්තර) ඇත්නම් පහතින් ඇතුළත් කරන්න. එක් කරුණක් සඳහා එක් පේළියක් භාවිතා කරන්න. අවශ්‍ය නැතිනම් හිස්ව තබන්න.")
terms_input = st.text_area("කරුණු ඇතුළත් කරන්න:", height=100)

st.divider()

# 4. PDF එක සෑදීමේ බොත්තම
if st.button("Generate Quotation PDF", type="primary"):
    if not c_name:
        st.warning("කරුණාකර පාරිභෝගිකයාගේ නම ඇතුළත් කරන්න.")
    else:
        customer_info = {
            "name": c_name,
            "address": c_address,
            "phone": c_phone,
            "date": c_date
        }

        # වගුවෙන් දත්ත ලබා ගැනීම
        invoice_items = []
        for index, row in edited_df.iterrows():
            # හිස් නැති පේළි පමණක් තෝරාගැනීම
            if pd.notna(row["Description"]) and str(row["Description"]).strip() != "":
                invoice_items.append({
                    "desc": str(row["Description"]),
                    "qty": float(row.get("Quantity", 0)),
                    "unit_price": float(row.get("Unit Price (LKR)", 0.0))
                })
        
        # Terms & Conditions වෙන් කර ලැයිස්තුවක් (List) එකක් බවට පත් කිරීම
        terms_list = []
        if terms_input.strip():
            # පේළියෙන් පේළිය කඩා, හිස් පේළි ඉවත් කර ගැනීම
            terms_list = [line.strip() for line in terms_input.split('\n') if line.strip()]

        if len(invoice_items) == 0:
            st.error("කරුණාකර එක් භාණ්ඩයක් හෝ ඇතුළත් කරන්න.")
        else:
            pdf_filename = "Sivilima_Quotation.pdf"
            try:
                # PDF එක සෑදීමට පෙර හැදූ function එක Call කිරීම (terms_list ද සමඟ)
                quotation.generate_quotation_pdf(pdf_filename, customer_info, invoice_items, terms_list)
                st.success("🎉 PDF එක සාර්ථකව නිර්මාණය විය!")
                
                # හදාගත් PDF එක Download කරගැනීමට බොත්තමක් ලබා දීම
                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_file,
                        file_name=f"Quotation_{c_name}.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"දෝෂයක් මතු විය: {e}")
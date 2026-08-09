import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_quotation_pdf(file_name, customer_data, items, terms=None, remarks=None):
    # A4 පිටුවේ margins සකස් කිරීම
    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    
    # පාට සහ Formatting සකස් කිරීම
    PURPLE_HEADER = colors.HexColor("#632c8b")
    PURPLE_LIGHT = colors.HexColor("#f3e8ff")
    PURPLE_ROW_ALT = colors.HexColor("#faf5ff")
    BORDER_COLOR = colors.HexColor("#d8b4fe")
    
    styles = getSampleStyleSheet()
    
    # ----------------------------------------------------
    # 1. TOP HEADER 
    # ----------------------------------------------------
    company_title_style = ParagraphStyle(
        'CompanyTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor("#642c8c"),
        alignment=2 # Right aligned
    )
    
    company_details_style = ParagraphStyle(
        'CompanyDetails',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.HexColor("#6b7280"),
        alignment=2,
        leading=12
    )

    logo_path = "logo.png" 
    
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=150, height=60)
    else:
        logo_img = Paragraph("<b>[LOGO]</b>", styles['Normal'])

    # Title එක සහ Address එක එක උඩ එක වැටීම වැළැක්වීමට Spacer එකක් යෙදීම
    company_info = [
        Paragraph("<b>Sivilima - Aluthgama</b>", company_title_style),
        Spacer(1, 10),  
        Paragraph("No.111/A, Galle road, Kaluwamodara, Aluthgama.<br/>"
                  "Phone: 0774663177 / 0714188644 | Email: sivilima.aluthgama@gmail.com", company_details_style)
    ]

    header_table = Table([[logo_img, company_info]], colWidths=[200, 320])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # ----------------------------------------------------
    # 2. "QUOTATION" BANNER 
    # ----------------------------------------------------
    quotation_banner_style = ParagraphStyle(
        'Banner',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.white,
        alignment=1 # Horizontally Center
    )
    
    # Padding ඉවත් කර rowHeights සහ VALIGN යෙදීමෙන් අකුරු හරියටම මැදට (Center) වේ
    banner_table = Table([[Paragraph("QUOTATION", quotation_banner_style)]], colWidths=[520], rowHeights=[35])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#5b21b6")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 15))

    # ----------------------------------------------------
    # 3. DATE & BILL TO SECTION
    # ----------------------------------------------------
    bill_to_text = f"""
    <b>Bill To:</b><br/>
    <b>Customer Name:</b> {customer_data.get('name', '')}<br/>
    <b>Address:</b> {customer_data.get('address', '')}<br/>
    <b>Phone:</b> {customer_data.get('phone', '')}
    """
    
    date_text = f"<b>Date:</b> {customer_data.get('date', '')}"
    
    bill_style = ParagraphStyle('BillStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13)
    
    info_table = Table([
        [Paragraph(date_text, bill_style), Paragraph(bill_to_text, bill_style)]
    ], colWidths=[260, 260])
    
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (1,0), PURPLE_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))

    # ----------------------------------------------------
    # 4. ITEMS TABLE
    # ----------------------------------------------------
    table_data = [
        [
            Paragraph("<b>#</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', textColor=colors.white, fontSize=9, alignment=1)),
            Paragraph("<b>Description</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', textColor=colors.white, fontSize=9, alignment=1)),
            Paragraph("<b>Quantity</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', textColor=colors.white, fontSize=9, alignment=1)),
            Paragraph("<b>Unit Price (LKR)</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', textColor=colors.white, fontSize=9, alignment=1)),
            Paragraph("<b>Amount (LKR)</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', textColor=colors.white, fontSize=9, alignment=1)),
        ]
    ]

    total_amount = 0.0

    for idx, item in enumerate(items, start=1):
        qty = item.get('qty', 0)
        unit_price = item.get('unit_price', 0.0)
        amount = qty * unit_price
        total_amount += amount

        cell_style_center = ParagraphStyle('TD', fontName='Helvetica', fontSize=9, alignment=1)
        cell_style_left = ParagraphStyle('TDL', fontName='Helvetica', fontSize=9, alignment=0)
        cell_style_right = ParagraphStyle('TDR', fontName='Helvetica', fontSize=9, alignment=2)

        # Format quantity to show as whole number when appropriate (no trailing .0)
        try:
            qf = float(qty)
            if qf.is_integer():
                qty_display = str(int(qf))
            else:
                qty_display = str(qf)
        except Exception:
            qty_display = str(qty) if qty is not None else ""

        table_data.append([
            Paragraph(str(idx), cell_style_center),
            Paragraph(item.get('desc', ''), cell_style_left),
            Paragraph(qty_display if qty and float(qty) != 0 else "", cell_style_center),
            Paragraph(f"{unit_price:,.2f}" if unit_price > 0 else "", cell_style_right),
            Paragraph(f"{amount:,.2f}" if amount > 0 else "", cell_style_right)
        ])

    items_table = Table(table_data, colWidths=[30, 230, 70, 95, 95])
    t_style = [
        ('BACKGROUND', (0,0), (-1,0), PURPLE_HEADER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]

    for i in range(1, len(table_data)):
        if i % 2 == 0:
            t_style.append(('BACKGROUND', (0, i), (-1, i), PURPLE_ROW_ALT))

    items_table.setStyle(TableStyle(t_style))
    story.append(items_table)
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # 5. TOTAL AMOUNT SECTION
    # ----------------------------------------------------
    total_label = ParagraphStyle('TL', fontName='Helvetica-Bold', textColor=colors.HexColor("#632c8b"), fontSize=10, alignment=2)
    total_val = ParagraphStyle('TV', fontName='Helvetica-Bold', textColor=colors.HexColor("#6b21a8"), fontSize=10, alignment=2)

    total_table = Table([
        ["", Paragraph("TOTAL AMOUNT:", total_label), Paragraph(f"LKR {total_amount:,.2f}", total_val)]
    ], colWidths=[230, 100, 190])

    total_table.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (2,0), PURPLE_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (1,0), (2,0), 1, colors.HexColor("#6b21a8")),
        ('LINEABOVE', (1,0), (2,0), 1, colors.HexColor("#6b21a8")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(total_table)
    story.append(Spacer(1, 15))

    # ----------------------------------------------------
    # 6. REMARKS (Optional) - only include if provided
    # ----------------------------------------------------
    if remarks and str(remarks).strip():
        remarks_title_style = ParagraphStyle(
            'RemarksTitle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#632c8b"), spaceAfter=6
        )
        story.append(Paragraph("<b>Remarks:</b>", remarks_title_style))
        # Use same styling as terms for bullet items
        remarks_term_style = ParagraphStyle('RemarksTerm', fontName='Helvetica', fontSize=9, textColor=colors.black, leading=14)

        for line in str(remarks).split('\n'):
            clean = line.strip()
            if not clean:
                continue
            # remove any leading bullets/dashes the user may have typed to avoid double bullets
            while clean.startswith('•') or clean.startswith('-'):
                clean = clean[1:].lstrip()
            bullet_line = f'<font color="#632c8b">&bull;</font> &nbsp;{clean}'
            story.append(Paragraph(bullet_line, remarks_term_style))
            story.append(Spacer(1, 2))
        story.append(Spacer(1, 12))

    # ----------------------------------------------------
    # 7. TERMS & CONDITIONS (Optional)
    # ----------------------------------------------------
    if terms and len(terms) > 0:
        terms_title_style = ParagraphStyle(
            'TermsTitle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#632c8b"), spaceAfter=6
        )
        story.append(Paragraph("<b>Terms & Conditions:</b>", terms_title_style))
        
        term_style = ParagraphStyle(
            'TermText', fontName='Helvetica', fontSize=9, textColor=colors.black, leading=14
        )
        
        for term in terms:
            # දම් පැහැති තිත් සලකුණ (Purple Bullet Point)
            bullet_term = f'<font color="#632c8b">&bull;</font> &nbsp;{term}'
            story.append(Paragraph(bullet_term, term_style))
            story.append(Spacer(1, 2))
            
        story.append(Spacer(1, 15))

    # ----------------------------------------------------
    # 7. FOOTER BANNER
    # ----------------------------------------------------
    footer_text = """
    <b>Thank you for your business!</b><br/>
    <font size="7" color="#d8b4fe">We look forward to serving you and building a lasting partnership.</font><br/><br/>
    <font size="7" color="#ffffff">For inquiries: sivilima.aluthgama@gmail.com  |  0774663177 / 0714188644</font>
    """
    footer_style = ParagraphStyle('FS', fontName='Helvetica-Bold', textColor=colors.white, fontSize=11, alignment=1, leading=12)
    
    footer_table = Table([[Paragraph(footer_text, footer_style)]], colWidths=[520])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PURPLE_HEADER),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(footer_table)

    # PDF එක නිර්මාණය කිරීම
    doc.build(story)
    print(f"PDF සාර්ථකව නිර්මාණය විය: {file_name}")


# ==========================================
#  Run Script (කේතය පරීක්ෂා කිරීම සඳහා)
# ==========================================
if __name__ == "__main__":
    customer_info = {
        "date": "2026-08-02",
        "name": "aaa",
        "address": "aa",
        "phone": "aa"
    }

    invoice_items = [
        {"desc": "aa", "qty": 74.0, "unit_price": 47.00},
        {"desc": "aaa", "qty": 85.0, "unit_price": 47.00},
    ]
    
    # පරීක්ෂා කිරීම සඳහා කොන්දේසි
    sample_terms = [
        "10 Years Warranty for specific items.",
        "Cash transactions only."
    ]

    generate_quotation_pdf("Quotation_aaa.pdf", customer_info, invoice_items, sample_terms)
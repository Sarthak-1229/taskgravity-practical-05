import os
import subprocess
import html
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def generate_docx():
    doc = docx.Document()
    
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Header
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("Department of Computer Engineering (Software Engineering)\n")
    r_dept.font.size = Pt(14)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_dept.add_run("Web Technology Laboratory — Academic Year 2026-27\n")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Practical No. 05: RESTful Web Services & Middleware Architecture using Express.js")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(37, 99, 235)

    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Name:", "Sarthak Bhosale"), ("PRN:", "202401100051")],
        [("Batch:", "TY SE-A2"), ("Roll No:", "A50")]
    ]
    for row_idx, row in enumerate(meta_data):
        col_offset = 0
        for label, val in row:
            cell_lbl = meta_table.cell(row_idx, col_offset)
            cell_val = meta_table.cell(row_idx, col_offset + 1)
            cell_lbl.text = label
            cell_lbl.paragraphs[0].runs[0].font.bold = True
            cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(71, 85, 105)
            cell_val.text = val
            cell_val.paragraphs[0].runs[0].font.bold = True
            cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(15, 23, 42)
            set_cell_bg(cell_lbl, "F1F5F9")
            set_cell_bg(cell_val, "FFFFFF")
            set_cell_margins(cell_lbl, 80, 80, 100, 100)
            set_cell_margins(cell_val, 80, 80, 100, 100)
            col_offset += 2

    doc.add_paragraph()

    def add_section_heading(num_str, title_str):
        h = doc.add_paragraph()
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        return h

    def add_code_block(title, code_str):
        p_t = doc.add_paragraph()
        r_t = p_t.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(37, 99, 235)
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, "0F172A")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(code_str)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(241, 245, 249)
        doc.add_paragraph()

    # 1. Aim
    add_section_heading("1", "Aim")
    doc.add_paragraph(
        "To design, develop, test, and deploy a RESTful web service for the TaskGravity system using Express.js, "
        "implementing custom middleware pipelines (request logging, authentication guards, security headers), "
        "modular routing, payload validation, and centralized error handling."
    )

    # 2. Problem Statement
    add_section_heading("2", "Problem Statement")
    doc.add_paragraph(
        "Enterprise web services require robust request lifecycle management. The objective is to build an Express.js "
        "application structured around modular middleware interceptors. The pipeline must intercept every incoming request "
        "for logging, parse JSON payloads, authenticate API consumers via custom headers, enforce strict field validation "
        "on task records, provide full CRUD endpoints, gracefully handle unmatched routes with 404 handlers, and trap "
        "unhandled exceptions via a four-argument global error middleware."
    )

    # 3. Theory & Concept Review
    add_section_heading("3", "Theory & Concept Review")
    doc.add_paragraph(
        "3.1 Express.js Middleware Chain (Pipeline Architecture)\n"
        "Express functions as a routing and middleware web framework. Middleware functions have access to the request object (req), "
        "response object (res), and the next middleware in line via next(). They can execute arbitrary code, mutate request/response "
        "objects, end the request-response cycle, or invoke next()."
    )
    doc.add_paragraph(
        "3.2 Types of Middleware\n"
        "• Application-level middleware: app.use() bound to the main app instance (e.g. express.json(), logger).\n"
        "• Router-level middleware: Bound to express.Router() instances for modular endpoint isolation.\n"
        "• Built-in middleware: express.static() for static file hosting, express.json() for body parsing.\n"
        "• Error-handling middleware: Defined with four arguments (err, req, res, next) to trap operational and runtime errors."
    )
    doc.add_paragraph(
        "3.3 RESTful Principles & HTTP Verbs\n"
        "Endpoints represent resource entities using standard HTTP methods: GET (read), POST (create), PUT (idempotent replace/update), "
        "and DELETE (remove), accompanied by standardized HTTP status codes (200, 201, 400, 404, 500)."
    )

    # 4. Software & Hardware Requirements
    add_section_heading("4", "Software & Hardware Requirements")
    req_table = doc.add_table(rows=5, cols=2)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    req_data = [
        ("Operating System", "Microsoft Windows 11 x64 / Linux x64 (Render Cloud)"),
        ("Runtime & Framework", "Node.js v20.x, Express.js v4.x, cors, dotenv"),
        ("Development Tools", "Antigravity IDE, npm package manager"),
        ("Testing Suite", "Postman Collection, Chrome DevTools Network Tab"),
        ("Cloud Deployment", "Render Web Service (PaaS), Git, GitHub")
    ]
    for idx, (lbl, val) in enumerate(req_data):
        c1, c2 = req_table.cell(idx, 0), req_table.cell(idx, 1)
        c1.text = lbl
        c1.paragraphs[0].runs[0].font.bold = True
        c2.text = val
        set_cell_bg(c1, "F8FAFC")
        set_cell_bg(c2, "FFFFFF")
        set_cell_margins(c1, 80, 80, 100, 100)
        set_cell_margins(c2, 80, 80, 100, 100)
    doc.add_paragraph()

    # 5. Design & Architectural Implementation
    add_section_heading("5", "Design & Architectural Implementation")
    doc.add_paragraph(
        "1. Middleware Pipeline: Requests enter through express.json(), followed by custom logger (method, url, IP, timestamp), "
        "and CORS middleware.\n"
        "2. Authentication Interceptor: authMiddleware checks for valid authorization credentials or API tokens.\n"
        "3. Validation Layer: taskValidator.js ensures incoming payloads satisfy business invariants before reaching business logic.\n"
        "4. Resource Controllers: CRUD handler functions manage in-memory task entities.\n"
        "5. Global Error Interceptor: Four-argument middleware formats clean JSON error payloads without leaking stack traces in production.\n"
        "6. Static UI Serving: express.static('public') exposes the TaskGravity minimalist dashboard."
    )

    # 6. Source Code
    add_section_heading("6", "Source Code Implementation")
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical5"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    server_js = read_code("server.js")
    validator_js = read_code(r"validators\taskValidator.js")
    app_js = read_code(r"public\app.js")
    index_html = read_code(r"public\index.html")

    add_code_block("6.1 server.js (Express Application, Middleware Chain & REST Endpoints)", server_js)
    add_code_block("6.2 validators/taskValidator.js (Input Sanitization & Validation Middleware)", validator_js)
    add_code_block("6.3 public/app.js (Client Dashboard Controller & Fetch Bridge)", app_js)
    add_code_block("6.4 public/index.html (TaskGravity Minimalist UI Frontend)", index_html)

    # 7. Verification & Test Results
    add_section_heading("7", "Verification & Test Results")
    test_table = doc.add_table(rows=6, cols=3)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Middleware / Route", "Test Scenario & Observed Result", "Status"]
    for c_idx, h in enumerate(test_headers):
        cell = test_table.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 100, 100)
    
    tests = [
        ("Logger Middleware", "Console logs method, path, status, and response latency for each inbound HTTP request.", "Passed"),
        ("GET /api/tasks", "Returns HTTP 200 with structured JSON task list and custom API headers.", "Passed"),
        ("Validation Middleware", "Malformed payload rejected with HTTP 400 Bad Request and validation error array.", "Passed"),
        ("POST /api/tasks", "Valid payload processed, entity assigned id/timestamps, returns HTTP 201 Created.", "Passed"),
        ("Global Error Handler", "Traps unexpected runtime errors, returning standard { error: 'Internal Server Error' } JSON.", "Passed")
    ]
    for r_idx, row in enumerate(tests, start=1):
        for c_idx, val in enumerate(row):
            cell = test_table.cell(r_idx, c_idx)
            cell.text = val
            if c_idx == 2:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "DCFCE7")
            else:
                set_cell_bg(cell, "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
    doc.add_paragraph()

    # 8. Conclusion
    add_section_heading("8", "Conclusion")
    doc.add_paragraph(
        "Practical 05 effectively demonstrates how to build scalable and maintainable RESTful web services using Express.js. "
        "By structuring the application around composable middleware pipelines, critical cross-cutting concerns (logging, "
        "security, validation, error handling) are decoupled from core business logic. The API operates reliably and is deployed "
        "live on Render Cloud."
    )

    # Links Box
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(14)
    tbl_links = doc.add_table(rows=1, cols=1)
    tbl_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_links = tbl_links.cell(0, 0)
    set_cell_bg(c_links, "F8FAFC")
    set_cell_margins(c_links, 120, 120, 150, 150)
    p_l = c_links.paragraphs[0]
    r_lh = p_l.add_run("Project Links & Deployment Information:\n")
    r_lh.font.bold = True
    r_lh.font.size = Pt(11)
    r_lh.font.color.rgb = RGBColor(15, 23, 42)

    r_gh = p_l.add_run("GitHub Link / Code Link: ")
    r_gh.font.bold = True
    p_l.add_run("https://github.com/Sarthak-1229/taskgravity-practical-05\n")

    r_live = p_l.add_run("Live Deployment Link: ")
    r_live.font.bold = True
    p_l.add_run("https://taskgravity-practical-05.onrender.com")

    docx_path = r"D:\_TY\Web-Tech\Practicals\Practical5\Practical_05_Report.docx"
    doc.save(docx_path)
    print(f"Generated DOCX: {docx_path}")

def generate_pdf():
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical5"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    server_js = html.escape(read_code("server.js"))
    validator_js = html.escape(read_code(r"validators\taskValidator.js"))
    app_js = html.escape(read_code(r"public\app.js"))
    index_html = html.escape(read_code(r"public\index.html"))

    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Practical 05 Report - Sarthak Bhosale</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  .header {{
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }}
  .dept-title {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.2px;
    text-transform: uppercase;
  }}
  .sub-title {{
    font-size: 10pt;
    font-weight: 600;
    color: #64748b;
    margin-top: 2px;
  }}
  .prac-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #2563eb;
    margin-top: 8px;
  }}
  .meta-grid {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 9.5pt;
  }}
  .meta-grid td {{
    border: 1px solid #cbd5e1;
    padding: 6px 10px;
  }}
  .meta-grid .lbl {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #475569;
    width: 15%;
  }}
  .meta-grid .val {{
    font-weight: 700;
    color: #0f172a;
    width: 35%;
  }}
  h2.sec-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h3.subsec-title {{
    font-size: 10pt;
    font-weight: 700;
    color: #2563eb;
    margin-top: 14px;
    margin-bottom: 4px;
  }}
  p, li {{
    font-size: 9.5pt;
    color: #334155;
    text-align: justify;
    margin-top: 4px;
    margin-bottom: 6px;
  }}
  ul, ol {{
    padding-left: 20px;
    margin-top: 4px;
    margin-bottom: 8px;
  }}
  .code-block {{
    background-color: #0f172a;
    color: #f8fafc;
    font-family: "Consolas", "Fira Code", monospace;
    font-size: 8pt;
    line-height: 1.4;
    padding: 10px 14px;
    border-radius: 4px;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 8px 0 14px 0;
  }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9pt;
  }}
  .data-table th, .data-table td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }}
  .data-table th {{
    background-color: #f8fafc;
    font-weight: 700;
    color: #0f172a;
  }}
  .badge-pass {{
    color: #15803d;
    font-weight: 700;
    background-color: #dcfce7;
    padding: 2px 6px;
    border-radius: 3px;
    display: inline-block;
  }}
  .links-box {{
    margin-top: 20px;
    padding: 12px 14px;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  .links-box a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="dept-title">Department of Computer Engineering (Software Engineering)</div>
  <div class="sub-title">Web Technology Laboratory — Academic Year 2026-27</div>
  <div class="prac-title">Practical No. 05: RESTful Web Services & Middleware Architecture using Express.js</div>
</div>

<table class="meta-grid">
  <tr>
    <td class="lbl">Name:</td>
    <td class="val">Sarthak Bhosale</td>
    <td class="lbl">PRN:</td>
    <td class="val">202401100051</td>
  </tr>
  <tr>
    <td class="lbl">Batch:</td>
    <td class="val">TY SE-A2</td>
    <td class="lbl">Roll No:</td>
    <td class="val">A50</td>
  </tr>
</table>

<h2 class="sec-title">1. Aim</h2>
<p>
To design, develop, test, and deploy a RESTful web service for the TaskGravity system using Express.js, implementing custom middleware pipelines (request logging, authentication guards, security headers), modular routing, payload validation, and centralized error handling.
</p>

<h2 class="sec-title">2. Problem Statement</h2>
<p>
Enterprise web services require robust request lifecycle management. The objective is to build an Express.js application structured around modular middleware interceptors. The pipeline must intercept every incoming request for logging, parse JSON payloads, authenticate API consumers via custom headers, enforce strict field validation on task records, provide full CRUD endpoints, gracefully handle unmatched routes with 404 handlers, and trap unhandled exceptions via a four-argument global error middleware.
</p>

<h2 class="sec-title">3. Theory & Concept Review</h2>
<p>
<strong>3.1 Express.js Middleware Chain:</strong> Middleware functions act as interceptors in the request-response lifecycle. Each middleware accepts <code>(req, res, next)</code> and either terminates the request with a response or yields control to downstream functions by invoking <code>next()</code>.
</p>
<p>
<strong>3.2 Modular Route Separation:</strong> Utilizing <code>express.Router()</code> allows partitioning endpoints logically by resource domains, isolating task management from authentication and health monitoring.
</p>
<p>
<strong>3.3 Centralized Error Trapping:</strong> Defining special four-argument middleware <code>(err, req, res, next)</code> catches both synchronous runtime exceptions and asynchronous errors passed via <code>next(err)</code>, preventing unhandled promise rejections and server crashes.
</p>

<h2 class="sec-title">4. Software & Hardware Requirements</h2>
<table class="data-table">
  <tr><th style="width: 30%;">Component</th><th>Specification</th></tr>
  <tr><td>Operating System</td><td>Microsoft Windows 11 x64 / Linux x64 (Render PaaS)</td></tr>
  <tr><td>Runtime & Framework</td><td>Node.js v20.x, Express.js v4.x, cors, dotenv</td></tr>
  <tr><td>Development Tools</td><td>Antigravity IDE, npm package manager</td></tr>
  <tr><td>Testing Suite</td><td>Postman Collection, Chrome DevTools Network Tab</td></tr>
  <tr><td>Version Control & Cloud</td><td>Git, GitHub, Render Web Services</td></tr>
</table>

<h2 class="sec-title">5. Design & Architectural Implementation</h2>
<ol>
  <li>Initialize Express app instance with environment configuration via <code>dotenv</code>.</li>
  <li>Mount core middlewares: <code>express.json()</code>, <code>cors()</code>, and custom request logger.</li>
  <li>Apply authentication guard middleware inspecting request headers.</li>
  <li>Mount task validation middleware checking title length, category, and status.</li>
  <li>Expose REST CRUD operations: <code>GET /api/tasks</code>, <code>POST /api/tasks</code>, <code>PUT /api/tasks/:id</code>, <code>DELETE /api/tasks/:id</code>.</li>
  <li>Implement 404 NotFound fallback and four-parameter global error handler.</li>
  <li>Serve static frontend dashboard from <code>public/</code>.</li>
</ol>

<h2 class="sec-title">6. Source Code Implementation</h2>

<h3 class="subsec-title">6.1 server.js (Express Application, Middleware Chain & REST Endpoints)</h3>
<pre class="code-block">{server_js}</pre>

<h3 class="subsec-title">6.2 validators/taskValidator.js (Input Sanitization & Validation Middleware)</h3>
<pre class="code-block">{validator_js}</pre>

<h3 class="subsec-title">6.3 public/app.js (Client Dashboard Controller & Fetch Bridge)</h3>
<pre class="code-block">{app_js}</pre>

<h3 class="subsec-title">6.4 public/index.html (TaskGravity Minimalist UI Frontend)</h3>
<pre class="code-block">{index_html}</pre>

<h2 class="sec-title">7. Verification & Test Results</h2>
<table class="data-table">
  <thead>
    <tr>
      <th>Middleware / Route</th>
      <th>Test Scenario & Observed Result</th>
      <th>Verification Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Logger Middleware</strong></td>
      <td>Console logs method, path, status, and response latency for each inbound HTTP request.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>GET /api/tasks</strong></td>
      <td>Returns HTTP 200 with structured JSON task list and custom API headers.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>Validation Middleware</strong></td>
      <td>Malformed payload rejected with HTTP 400 Bad Request and validation error array.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>POST /api/tasks</strong></td>
      <td>Valid payload processed, entity assigned id/timestamps, returns HTTP 201 Created.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>Global Error Handler</strong></td>
      <td>Traps unexpected runtime errors, returning standard JSON error payload without stack leaks.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
  </tbody>
</table>

<h2 class="sec-title">8. Conclusion</h2>
<p>
Practical 05 effectively demonstrates how to build scalable and maintainable RESTful web services using Express.js. By structuring the application around composable middleware pipelines, critical cross-cutting concerns (logging, security, validation, error handling) are decoupled from core business logic. The API operates reliably and is deployed live on Render Cloud.
</p>

<div class="links-box">
  <div style="font-weight: 700; font-size: 11pt; margin-bottom: 6px; color: #0f172a;">Project Links & Deployment Information</div>
  <div><strong>GitHub Link / Code Link:</strong> <a href="https://github.com/Sarthak-1229/taskgravity-practical-05" target="_blank">https://github.com/Sarthak-1229/taskgravity-practical-05</a></div>
  <div style="margin-top: 4px;"><strong>Live Deployment Link:</strong> <a href="https://taskgravity-practical-05.onrender.com" target="_blank">https://taskgravity-practical-05.onrender.com</a></div>
</div>

</body>
</html>
"""
    html_report_path = r"D:\_TY\Web-Tech\Practicals\Practical5\report_temp.html"
    pdf_report_path = r"D:\_TY\Web-Tech\Practicals\Practical5\Practical_05_Report.pdf"

    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    chrome_cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_report_path}",
        html_report_path
    ]
    subprocess.run(chrome_cmd, check=True)
    
    if os.path.exists(html_report_path):
        os.remove(html_report_path)
    
    print(f"Generated PDF: {pdf_report_path}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()

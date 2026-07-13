# 🔄 Odoo Complete Flow Diagram & Architecture

Panduan lengkap alur kerja Odoo dari awal sampai akhir dengan semua file dan fungsinya.

---

## 1. STRUKTUR FOLDER & FILE ODOO

```mermaid
graph TD
    A["🎯 ODOO PROJECT"] --> B["📁 addons/"]
    A --> C["📁 config/"]
    A --> D["📁 python-libs/"]
    
    B --> B1["📁 my_first_module/"]
    B1 --> B1a["🐍 __init__.py (Import models)"]
    B1 --> B1b["📋 __manifest__.py (Metadata)"]
    B1 --> B1c["📁 models/"]
    B1 --> B1d["📁 views/"]
    B1 --> B1e["📁 security/"]
    B1 --> B1f["📁 static/"]
    B1 --> B1g["📁 controllers/"]
    
    B1c --> B1c1["🐍 __init__.py"]
    B1c --> B1c2["🐍 todo.py (Model definition)"]
    
    B1d --> B1d1["📄 todo_views.xml (UI Form)"]
    B1d --> B1d2["📄 todo_actions.xml (Menu)"]
    
    B1e --> B1e1["📄 ir.model.access.csv (ACL)"]
    
    B1g --> B1g1["🐍 controller.py (Web routes)"]
    
    C --> C1["📄 odoo.conf (Config)"]
    D --> D1["Third-party libs"]
```

---

## 2. ALUR LENGKAP DARI USER MEMBUKA FORM SAMPAI DATA TERSIMPAN

```mermaid
graph LR
    Start["👤 User membuka form\ndi browser"] 
    --> Step1["📡 Browser request ke\nserver Odoo"]
    --> Step2["🔍 Cek Security & ACL\n(ir.model.access.csv)"]
    --> Step3["📄 Load View XML\n(views/todo_views.xml)"]
    --> Step4["🎨 Render HTML/JS form\ndi browser"]
    --> Step5["✏️ User isi form\n& click SAVE"]
    --> Step6["📨 JavaScript kirim\ndata ke backend"]
    --> Step7["🔐 Server cek permission\nlagi"]
    --> Step8["🐍 Controller/Model\njalankan ORM.create()"]
    --> Step9["🗄️ PostgreSQL database\ntambah record"]
    --> Step10["✅ Response OK\nke browser"]
    --> End["🎉 Form close,\ndata tersimpan"]
    
    style Start fill:#90EE90
    style Step8 fill:#87CEEB
    style Step9 fill:#FFB6C1
    style End fill:#90EE90
```

---

## 3. FILE STRUCTURE DAN FUNGSI MASING-MASING

### 📋 A. `__manifest__.py` - Metadata Modul
**Lokasi:** `addons/my_first_module/__manifest__.py`

```python
{
    'name': 'My First Module',           # Nama modul di UI
    'version': '1.0',                    # Versi
    'depends': ['base', 'sale'],         # Modul yang dibutuhkan
    'data': [                            # File XML yang di-load
        'security/ir.model.access.csv',
        'views/todo_views.xml',
    ],
    'installable': True,
}
```

**Fungsi:**
- Menginformasikan Odoo tentang modul apa yang akan di-install
- Menentukan dependencies (modul lain yang diperlukan)
- Mengatur file XML yang akan di-load

---

### 🐍 B. `models/__init__.py` - Import Model

**Lokasi:** `addons/my_first_module/models/__init__.py`

```python
from . import todo
```

**Fungsi:**
- Membuat Python paket recognizable
- Import file model agar Odoo mengenali modelnya

---

### 🐍 C. `models/todo.py` - Definisi Model & Logic Bisnis

**Lokasi:** `addons/my_first_module/models/todo.py`

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name = 'todo.task'                    # Nama model (table database)
    _description = 'To-Do Task'
    
    # ===== FIELD DEFINITIONS (KOLOM DATABASE) =====
    name = fields.Char(string='Task Title', required=True)
    description = fields.Text()
    is_done = fields.Boolean(default=False)
    priority = fields.Selection([('0', 'Low'), ('1', 'High')])
    responsible_id = fields.Many2one('res.users', string='Responsible')
    
    # ===== METHODS (BUSINESS LOGIC) =====
    def action_mark_done(self):
        """Tandai task sebagai selesai"""
        for record in self:
            record.write({'is_done': True})  # ORM: UPDATE
    
    @api.constrains('name')
    def _validate_name(self):
        """Validasi nama task"""
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("Nama minimal 3 karakter!")
```

**Fungsi:**
- Definisi tabel database
- Definisi field/kolom
- Business logic (ORM CREATE, READ, UPDATE, DELETE)
- Validasi data

---

### 📄 D. `views/todo_views.xml` - UI Form

**Lokasi:** `addons/my_first_module/views/todo_views.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <!-- FORM VIEW (Form input) -->
    <record id="view_todo_form" model="ir.ui.view">
        <field name="name">Todo Task Form</field>
        <field name="model">todo.task</field>
        <field name="arch" type="xml">
            <form string="Task">
                <sheet>
                    <group>
                        <field name="name"/>           <!-- Input field -->
                        <field name="priority"/>        <!-- Selection field -->
                        <field name="is_done"/>         <!-- Checkbox -->
                        <field name="responsible_id"/> <!-- Many2one relation -->
                    </group>
                </sheet>
                <!-- BUTTON: Panggil method Python -->
                <footer>
                    <button name="action_mark_done" type="object" 
                            string="Mark as Done" class="btn-success"/>
                </footer>
            </form>
        </field>
    </record>
    
    <!-- LIST VIEW (Tabel data) -->
    <record id="view_todo_list" model="ir.ui.view">
        <field name="name">Todo Task List</field>
        <field name="model">todo.task</field>
        <field name="arch" type="xml">
            <list string="Tasks">
                <field name="name"/>
                <field name="priority"/>
                <field name="is_done"/>
            </list>
        </field>
    </record>
</odoo>
```

**Fungsi:**
- Render UI form di browser
- Definisi field yang ditampilkan
- Button yang trigger method Python

---

### 📄 E. `views/todo_actions.xml` - Menu & Action

**Lokasi:** `addons/my_first_module/views/todo_actions.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <!-- ACTION: Window action yang buka list/form -->
    <record id="action_todo_task" model="ir.actions.act_window">
        <field name="name">Tasks</field>
        <field name="res_model">todo.task</field>           <!-- Model mana yang dibuka -->
        <field name="view_mode">list,form</field>           <!-- View apa saja -->
        <field name="help">Create new task</field>
    </record>
    
    <!-- MENU ITEM: Menu di sidebar -->
    <menuitem id="menu_todo" name="Tasks"
              action="action_todo_task"
              sequence="10"/>
</odoo>
```

**Fungsi:**
- Definisi action window (buka list/form view)
- Definisi menu di sidebar

---

### 📄 F. `security/ir.model.access.csv` - Role-Based Access Control

**Lokasi:** `addons/my_first_module/security/ir.model.access.csv`

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_todo_task_user,todo.task user,model_todo_task,base.group_user,1,1,1,0
access_todo_task_manager,todo.task manager,model_todo_task,base.group_user,1,1,1,1
```

**Arti Kolom:**
- `id`: ID unik untuk ACL
- `name`: Deskripsi ACL
- `model_id:id`: Model mana (reference ke ir.model)
- `group_id:id`: Role/group mana (base.group_user, dll)
- `perm_read`: 1=bisa baca, 0=tidak
- `perm_write`: 1=bisa edit, 0=tidak
- `perm_create`: 1=bisa buat, 0=tidak
- `perm_unlink`: 1=bisa hapus, 0=tidak

---

### 🐍 G. `__init__.py` Root Module

**Lokasi:** `addons/my_first_module/__init__.py`

```python
from . import models
```

**Fungsi:**
- Python package marker
- Import subpackage (models folder)

---

### 🐍 H. `controllers/main.py` - Web Routes (Optional)

**Lokasi:** `addons/my_first_module/controllers/main.py`

```python
from odoo import http
from odoo.http import request

class TodoController(http.Controller):
    @http.route('/todo/list', type='http', auth='user')
    def todo_list(self, **kw):
        """Endpoint khusus untuk API atau custom page"""
        tasks = request.env['todo.task'].search([])
        return request.render('my_first_module.todo_template', {
            'tasks': tasks
        })
    
    @http.route('/todo/create', type='json', auth='user', methods=['POST'])
    def todo_create(self, **kw):
        """API endpoint untuk create task"""
        task = request.env['todo.task'].create({
            'name': kw.get('name'),
            'priority': kw.get('priority'),
        })
        return {'id': task.id, 'name': task.name}
```

**Fungsi:**
- Custom web routes (selain UI standard Odoo)
- REST API endpoints
- Custom templates

---

## 4. ALUR LENGKAP: USER CLICK BUTTON SAMPAI DATA UPDATE

```mermaid
graph TD
    A["🎨 UI: User lihat FORM\n(dari views/todo_views.xml)"]
    --> B["✏️ User isi field nama\n& click 'Mark as Done'"]
    --> C["🔘 Form button trigger\nname='action_mark_done'"]
    --> D["📨 JavaScript kirim request\nke backend Odoo server"]
    --> E["🔐 Server cek permission\n(ir.model.access.csv)"]
    --> F{User punya\naccess?}
    
    F -->|Tidak| G["❌ Error: Permission Denied"]
    F -->|Ya| H["🐍 Python jalankan\naction_mark_done method"]
    
    H --> I["📝 Method jalankan:\nfor record in self:\n  record.write(...)"]
    --> J["🗄️ ORM kerjakan SQL:\nUPDATE todo_task\nSET is_done=1"]
    --> K["💾 PostgreSQL\nexecute SQL"]
    --> L["✅ Database return OK"]
    --> M["🔄 ORM return recordset\nyang updated"]
    --> N["📤 Server kirim response\nke frontend"]
    --> O["🎨 Frontend refresh form\ndan tampilkan data baru"]
    --> P["✨ User lihat field\nis_done sekarang TRUE"]
    
    style A fill:#FFE4B5
    style H fill:#87CEEB
    style K fill:#FFB6C1
    style P fill:#90EE90
    style G fill:#FF6347
```

---

## 5. FLOW DATA DALAM DATABASE

```mermaid
graph LR
    A["🐍 Python Model\n(models/todo.py)"] 
    -->|.create| B["🗄️ PostgreSQL Table\n(todo_task)"]
    -->|Insert Row| C["📊 Record with ID"]
    
    C -->|.search| D["🗄️ Query database"]
    -->|Select rows| E["Return Recordset"]
    
    C -->|.write| F["🗄️ Update database"]
    -->|Update rows| G["Updated Record"]
    
    C -->|.unlink| H["🗄️ Delete database"]
    -->|Delete rows| I["Record removed"]
    
    style A fill:#87CEEB
    style B fill:#FFB6C1
    style C fill:#FFE4B5
```

---

## 6. STRUKTUR FOLDER + FILES YANG DILOAD SAAT MODULE DI-INSTALL

```mermaid
graph TD
    Install["🚀 Module di-install"]
    --> Read1["📖 Baca __manifest__.py"]
    --> Parse1["Parse 'data' & 'depends'"]
    --> Check["✓ Validasi dependencies"]
    --> Load["📥 Load semua file XML:"]
    
    Load --> File1["📄 security/ir.model.access.csv"]
    Load --> File2["📄 views/todo_views.xml"]
    Load --> File3["📄 views/todo_actions.xml"]
    
    File1 --> DB1["🗄️ Create ir.model.access\nrecords di database"]
    File2 --> DB2["🗄️ Create ir.ui.view\nrecords"]
    File3 --> DB3["🗄️ Create ir.actions & menu\nrecords"]
    
    DB1 --> Finish["✅ Module installed\nReady to use!"]
    DB2 --> Finish
    DB3 --> Finish
    
    style Install fill:#90EE90
    style Finish fill:#90EE90
```

---

## 7. ALUR KOMUNIKASI FORM ↔ BACKEND

```mermaid
sequenceDiagram
    participant Browser as 🌐 Browser
    participant Server as 🖥️ Odoo Server
    participant ORM as 🐍 ORM Layer
    participant DB as 🗄️ PostgreSQL

    Browser->>Server: GET /form (Minta form halaman)
    Server->>Server: Cek ACL (ir.model.access.csv)
    Server->>ORM: Ambil data dari model
    ORM->>DB: SELECT * FROM todo_task
    DB-->>ORM: Return data
    ORM-->>Server: Recordset
    Server-->>Browser: Render HTML form + data
    
    Note over Browser: User isi form & click SAVE
    
    Browser->>Server: POST /save (Kirim data)
    Server->>Server: Validasi permission
    Server->>ORM: call model.create({...}) atau .write({...})
    ORM->>DB: INSERT/UPDATE SQL query
    DB-->>ORM: Success
    ORM-->>Server: Return recordset updated
    Server-->>Browser: Response 200 OK + new data
    
    Browser->>Browser: Refresh form dengan data baru
```

---

## 8. FILE YANG PERLU DIBUAT UNTUK MODULE BARU

```
✅ WAJIB DIBUAT:
├── __manifest__.py ...................... Metadata modul
├── __init__.py .......................... Import marker
├── models/
│   ├── __init__.py ...................... Import models
│   └── nama_model.py .................... Definisi model + logic
├── views/
│   └── views.xml ........................ UI Form, List, Search
└── security/
    └── ir.model.access.csv .............. Role-based ACL

⭐ OPSIONAL (tapi recommended):
├── controllers/
│   └── main.py .......................... Web routes / API
├── views/
│   └── actions.xml ...................... Menu & window actions
├── views/
│   └── templates.xml .................... HTML templates (QWeb)
├── security/
│   └── security.xml ..................... Record rules (domain)
├── static/
│   ├── css/ ............................ Custom CSS
│   └── js/ ............................. Custom JavaScript
├── i18n/
│   └── id.po ........................... Terjemahan
└── data/
    └── data.xml ......................... Default data
```

---

## 9. COMMAND LINE UNTUK TEST ORM

```bash
# Buka shell interaktif Odoo + akses database
docker compose exec odoo odoo shell -d odoo_dev

# Di dalam shell, bisa langsung pakai ORM:
>>> env['todo.task'].create({'name': 'Test', 'priority': '1'})
<Record>

>>> env['todo.task'].search([('priority', '=', '1')])
<RecordSet>

>>> records = env['todo.task'].search([])
>>> records.write({'is_done': True})

>>> env['todo.task'].search_count([])
10
```

---

## 10. RINGKASAN FLOW LENGKAP

```
┌─────────────────────────────────────────────────────────────┐
│                    ODOO COMPLETE FLOW                        │
└─────────────────────────────────────────────────────────────┘

1️⃣  USER MEMBUKA APLIKASI
    └─→ Browser request ke http://odoo-server/

2️⃣  SERVER MEMPROSES REQUEST
    └─→ Baca __manifest__.py & load semua file XML
    └─→ Parse views/todo_views.xml
    └─→ Cek ir.model.access.csv untuk permission

3️⃣  FRONTEND RENDER FORM
    └─→ views/todo_views.xml convert ke HTML
    └─→ Tampilkan form dengan field dari models/todo.py
    └─→ Button "Mark as Done" siap diklik

4️⃣  USER INTERACT DENGAN FORM
    └─→ Klik button atau isi field
    └─→ JavaScript mengirim event ke server

5️⃣  BACKEND PROCESS ORM
    └─→ Validate permission (ir.model.access.csv)
    └─→ Jalankan method di models/todo.py
    └─→ ORM generate SQL query

6️⃣  DATABASE OPERATION
    └─→ PostgreSQL execute SQL (INSERT/UPDATE/DELETE)
    └─→ Return hasil ke ORM

7️⃣  RESPONSE KE FRONTEND
    └─→ Server kirim updated data
    └─→ Browser refresh form

8️⃣  UI UPDATE
    └─→ Form menampilkan data terbaru
    └─→ User lihat perubahan

```

---

## 11. CONTOH REAL: CREATE TASK WORKFLOW

```
📝 Step-by-step membuat task baru

1. User klik Menu "Tasks" (dari views/todo_actions.xml)
   ↓
2. Odoo load action_todo_task window action
   ↓
3. Tampilkan list + button "Create"
   ↓
4. User klik "Create" → buka form kosong
   ↓
5. Form render dari views/todo_views.xml dengan field:
   - name (Char)
   - priority (Selection)
   - responsible_id (Many2one)
   ↓
6. User isi:
   name = "Belajar Odoo"
   priority = "High"
   responsible_id = "Budi" (user)
   ↓
7. User klik "SAVE"
   ↓
8. JavaScript trigger POST request dengan data
   ↓
9. Server cek permission di ir.model.access.csv
   perm_create = 1 ✅ (allowed)
   ↓
10. Server panggil ORM create():
    task = self.env['todo.task'].create({
        'name': 'Belajar Odoo',
        'priority': '2',
        'responsible_id': 1
    })
    ↓
11. ORM generate SQL:
    INSERT INTO todo_task (name, priority, responsible_id)
    VALUES ('Belajar Odoo', '2', 1);
    ↓
12. PostgreSQL execute & return ID (e.g., id=5)
    ↓
13. Server response {"id": 5, "status": "success"}
    ↓
14. Frontend close form & refresh list
    ↓
15. ✅ Task muncul di list view
```

---

## 12. TROUBLESHOOTING: FILE MANA YANG PERLU DIUBAH?

| Masalah | File yang perlu diubah |
|--------|----------------------|
| Form tidak tampil | `views/todo_views.xml` |
| Menu tidak muncul | `views/todo_actions.xml` |
| User tidak bisa akses | `security/ir.model.access.csv` |
| Logic tidak berjalan | `models/todo.py` |
| Field baru tidak ada | `models/todo.py` (tambah field) + migration |
| Validasi tidak work | `models/todo.py` (@api.constrains) |
| Permission denied | `security/ir.model.access.csv` + `ir_rule` |
| Button tidak trigger | `views/todo_views.xml` (check button definition) |
| Data tidak tersimpan | `models/todo.py` (.write/.create error) |

---

Semoga diagram ini membantu Anda memahami flow lengkap Odoo! 🚀


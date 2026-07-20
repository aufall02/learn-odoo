# Odoo Field Mastery — Video 21–23

Catatan materi dari **Odoo Mates** video 21, 22, dan 23 tentang pengembangan field di modul Odoo.

---

## 📋 Overview

| Video | Topik |
|-------|-------|
| Video 21 | Date & Datetime Field |
| Video 22 | Default Value |
| Video 23 | Related Field |

---

## 📅 Video 21 — Date & Datetime Field

### Perbedaan `fields.Date` vs `fields.Datetime`

| | `fields.Date` | `fields.Datetime` |
|---|---|---|
| Isi | Tanggal saja | Tanggal + waktu |
| Format | `YYYY-MM-DD` | `YYYY-MM-DD HH:MM:SS` |
| Python type | `datetime.date` | `datetime.datetime` |
| Use case | Deadline, tanggal lahir | Waktu transaksi, log |
| Timezone | Tidak ada | Disimpan UTC di DB |

### Implementasi

```python
# models/my_model.py
from odoo import fields, models

class MyModel(models.Model):
    _name = 'my.model'

    # Date field — tanggal saja
    tanggal_lahir = fields.Date(
        string='Tanggal Lahir',
        required=True
    )

    # Datetime field — tanggal + waktu
    waktu_transaksi = fields.Datetime(
        string='Waktu Transaksi'
    )
```

> 💡 **Tip:** `fields.Datetime` otomatis dikonversi ke timezone user saat ditampilkan di UI, tapi disimpan dalam UTC di database.

---

## ⚙️ Video 22 — Default Value

### Apa itu Default Value?

Nilai yang **otomatis diisi** ke field saat user membuat record baru, tanpa perlu input manual.

### 3 Cara Mendefinisikan Default Value

**1. Static Value** — nilai tetap langsung di parameter

```python
status = fields.Selection([
    ('draft', 'Draft'),
    ('done', 'Done'),
], default='draft')

is_active = fields.Boolean(default=True)
urutan   = fields.Integer(default=10)
```

**2. Lambda Function** — nilai dinamis

```python
# Ambil user yang sedang login
salesperson_id = fields.Many2one(
    'res.users',
    default=lambda self: self.env.user
)

# Ambil company aktif
company_id = fields.Many2one(
    'res.company',
    default=lambda self: self.env.company
)
```

**3. Method / Function** — nilai dari method di class

```python
order_date = fields.Date(default='_get_today')

def _get_today(self):
    return fields.Date.today()
```

### Contoh Lengkap

```python
class SalesOrder(models.Model):
    _name = 'sale.order'

    # Static
    status = fields.Selection([...], default='draft')

    # Lambda — user saat ini
    salesperson_id = fields.Many2one('res.users',
        default=lambda self: self.env.user)

    # Method
    order_date = fields.Date(default='_get_today')

    def _get_today(self):
        return fields.Date.today()
```

> 💡 **Tips:**
> - `fields.Date.today()` → default tanggal hari ini
> - `fields.Datetime.now()` → default waktu sekarang (UTC)
> - Hindari mutable object (`list`/`dict`) sebagai default langsung

---

## 🔗 Video 23 — Related Field

### Apa itu Related Field?

Field yang nilainya **dimirror/diambil** dari field model lain melalui relasi (`Many2one`, dll), tanpa perlu menulis compute function.

### Cara Kerja

```
Model A (sale.order)          Model B (res.partner)
─────────────────────         ─────────────────────
partner_id ──────────────────► name
partner_email (related) ─────► email
```

### Properti Penting

| Properti | Keterangan |
|----------|------------|
| `related` | Path ke field target, contoh: `'partner_id.email'` |
| `readonly` | Default `True` — tidak bisa diedit langsung |
| `store` | `store=True` → disimpan di DB, bisa untuk filter/search |

### Implementasi

```python
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    # Relasi ke header order
    order_id = fields.Many2one('sale.order')

    # Related field — ambil partner dari order
    partner_id = fields.Many2one(
        related='order_id.partner_id',
        store=True
    )

    # Related dengan store=True untuk search/filter
    partner_email = fields.Char(
        related='order_id.partner_id.email',
        store=True
    )
```

### Best Practices

- ✅ Gunakan `store=True` jika field sering dipakai sebagai filter atau group by
- ✅ Gunakan `readonly=False` dengan hati-hati — bisa overwrite data di model asal
- ✅ Gunakan `related` untuk display-only di form view tanpa duplikasi data
- ⚠️ Hindari chain relasi terlalu panjang (>2 hop) — bisa pengaruh ke performa

---

*Sumber: Odoo Mates — Video 21, 22, 23*


---

# Odoo List View Enhancement - vidio 38 - 40
### Membuat List View Lebih Informatif & User Friendly

---

## Agenda

1. Give Color for List View
2. Widget List Activity
3. Dynamic List View (Optional Columns)

---

## 1. Give Color for List View

### Apa itu?
Fitur untuk memberikan warna pada baris list view berdasarkan kondisi tertentu, sehingga user bisa langsung mengetahui status record **tanpa membuka satu per satu**.

### Kenapa Perlu?
- User langsung tau status record dari warna
- Meningkatkan efisiensi & UX
- Mengurangi kesalahan baca data

### Cara Pakai

```xml
<list decoration-success="status == 'done'"
      decoration-warning="status == 'in_consultation'"
      decoration-danger="status == 'cancel'"
      decoration-info="status == 'draft'">
    <field name="patient_id"/>
    <field name="status"/>
</list>
```

### Decoration yang Tersedia

| Decoration | Warna | Contoh Penggunaan |
|---|---|---|
| `decoration-success` | Hijau | Status selesai/done |
| `decoration-warning` | Kuning | Status pending/proses |
| `decoration-danger` | Merah | Status cancel/error |
| `decoration-info` | Biru | Status draft/baru |
| `decoration-muted` | Abu-abu | Data tidak aktif |
| `decoration-bf` | **Bold** | Data penting |
| `decoration-it` | *Italic* | Catatan/keterangan |

### Hasil

```
✅ Hijau  → Appointment Done
⚠️ Kuning → In Consultation
❌ Merah  → Cancelled
ℹ️ Biru   → Draft
```

---

## 2. Widget List Activity

### Apa itu?
Widget khusus yang menampilkan **ikon aktivitas** langsung di list view, sehingga user bisa melihat & menjadwalkan aktivitas tanpa membuka form record.

### Kenapa Perlu?
- Tracking aktivitas lebih efisien
- User tidak perlu buka record satu per satu
- Terintegrasi dengan sistem activity Odoo

### Cara Pakai

```xml
<!-- Di list view -->
<list>
    <field name="patient_id"/>
    <field name="activity_ids" widget="list_activity"/>
</list>
```

### Syarat Wajib di Model

```python
class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    
    # Wajib inherit ini!
    _inherit = ['mail.thread', 'mail.activity.mixin']
```

### Schedule Activity via Code

```python
def action_confirm(self):
    self.activity_schedule(
        'mail.mail_activity_data_todo',
        summary='Appointment Confirmed',
        note='Patient has been confirmed',
        user_id=self.env.user.id,
    )
```

### Tipe Activity Bawaan Odoo

| XML ID | Keterangan |
|---|---|
| `mail.mail_activity_data_todo` | To-Do |
| `mail.mail_activity_data_call` | Phone Call |
| `mail.mail_activity_data_meeting` | Meeting |
| `mail.mail_activity_data_email` | Email |

---

## 3. Dynamic List View

### Apa itu?
Fitur yang memungkinkan **user memilih sendiri kolom** mana yang ingin ditampilkan di list view, sesuai kebutuhan masing-masing.

### Kenapa Perlu?
- Tampilan lebih fleksibel per kebutuhan user
- Kolom tidak terlalu penuh/crowded
- Setiap user bisa punya preferensi berbeda

### Cara Pakai

```xml
<list>
    <field name="patient_id"        optional="show"/>
    <field name="appointment_time"  optional="show"/>
    <field name="booking_date"      optional="show"/>
    <field name="activity_ids"      optional="show" widget="list_activity"/>
    <field name="status"            optional="hide"/>
</list>
```

### Perbedaan `show` vs `hide`

| Value | Default | Keterangan |
|---|---|---|
| `optional="show"` | Tampil ✅ | Bisa disembunyikan user |
| `optional="hide"` | Sembunyi | Bisa ditampilkan user |
| *(tanpa optional)* | Tampil | Tidak bisa diubah user |

### Cara User Menggunakannya
```
List View → Icon Kolom (pojok kanan atas tabel)
         → Centang/uncentang kolom yang diinginkan
         → Preferensi tersimpan otomatis per user
```

---

## Kombinasi Ketiganya

```xml
<list decoration-success="status == 'done'"
      decoration-warning="status == 'in_consultation'"
      decoration-danger="status == 'cancel'"
      decoration-info="status == 'draft'">

    <field name="patient_id"       optional="show"/>
    <field name="appointment_time" optional="show"/>
    <field name="booking_date"     optional="show"/>
    <field name="activity_ids"     optional="show" widget="list_activity"/>
    <field name="status"
           optional="show"
           decoration-info="status == 'draft'"
           decoration-success="status == 'done'"
           decoration-warning="status == 'in_consultation'"
           decoration-danger="status == 'cancel'"
           widget="badge"/>
</list>
```

---

## Kesimpulan

| Fitur | Manfaat Utama |
|---|---|
| **Give Color** | User langsung tau status dari warna |
| **Widget Activity** | Tracking aktivitas tanpa buka form |
| **Dynamic Columns** | Tampilan fleksibel sesuai kebutuhan user |

### Key Takeaway
> Ketiga fitur ini berfokus pada **UX & Efisiensi** — membuat user bekerja lebih cepat dan nyaman tanpa perlu buka record satu per satu.

---

*Odoo List View Enhancement — 2026*
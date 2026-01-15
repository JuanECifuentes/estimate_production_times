# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Activate Virtual Environment

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Step 2: Install Dependencies (if needed)

```bash
pip install -r requirements.txt
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Generate Sample File

```bash
python generate_sample.py
```

This creates `sample_time_study.xlsx` with test data.

### Step 5: Start Server

```bash
python manage.py runserver
```

### Step 6: Test the Application

**Option A: Web Interface**
1. Open browser: http://127.0.0.1:8000/
2. Drag and drop `sample_time_study.xlsx`
3. Click "Procesar Archivo"
4. Download processed file automatically

**Option B: API Test**
```bash
python test_api.py
```

**Option C: cURL**
```bash
curl -X POST http://127.0.0.1:8000/api/process-time-study/ \
  -F "file=@sample_time_study.xlsx" \
  --output resultado.xlsx
```

### Step 7: Verify Output

```bash
python verify_output.py
```

## 📁 Expected Excel Format

Your Excel file must have these columns:

| Column | Required | Type | Example |
|--------|----------|------|---------|
| Operador | ✅ Yes | Text | Juan Pérez |
| Operación | ✅ Yes | Text | Coser manga |
| Máquina | ✅ Yes | Text | Overlock |
| Tiempo 1, Tiempo 2, ... | ✅ Yes | Number | 45.2 |
| Suplemento | ✅ Yes | Number | 15 |

**Notes:**
- Time columns can be named "Tiempo 1", "Tiempo 2", etc.
- You need at least one time measurement column
- Supplement (Suplemento) is in percentage (15 = 15%)
- Times are in seconds

## 🔧 Configuration

Edit `production_estimator/settings.py`:

```python
TIME_ESTIMATION_CONFIG = {
    'WORKING_HOURS_PER_DAY': 8,      # Change work hours
    'MAX_FILE_SIZE_MB': 10,           # Change max file size
    'ALLOWED_EXTENSIONS': ['.xlsx'],  # File extensions
}
```

## 📊 Output Format

The processed Excel will contain:

| Column | Description |
|--------|-------------|
| Operador | Operator name (preserved) |
| Operación | Operation name |
| Máquina | Machine type |
| Tiempo Promedio (seg) | Average observed time |
| Suplemento (%) | Supplement percentage |
| Tiempo Estándar (seg) | Standard time in seconds |
| Tiempo Estándar (min) | Standard time in minutes |
| Unidades/Hora | Target units per hour |
| Unidades/Día | Target units per day |

## 🧪 Test Files Included

- `generate_sample.py` - Creates sample Excel file
- `test_api.py` - Tests the API endpoint
- `verify_output.py` - Verifies output calculations

## 🆘 Troubleshooting

### Server won't start
```bash
# Check if virtual environment is active
python --version
pip list | grep Django

# Reinstall dependencies
pip install -r requirements.txt

# Run migrations again
python manage.py migrate
```

### Import errors
```bash
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Verify installation
pip list
```

### Port already in use
```bash
# Use different port
python manage.py runserver 8080
```

### File upload fails
- Check file is .xlsx format
- Verify file size < 10MB
- Ensure all required columns exist
- Check column names match exactly

## 📚 More Documentation

See `README.md` for complete documentation including:
- Full API documentation
- Error handling details
- Architecture overview
- Production deployment guide

## 🎯 What This MVP Does

✅ Reads Excel time-study files  
✅ Validates data structure  
✅ Calculates standard times  
✅ Computes production targets  
✅ Generates formatted Excel output  
✅ Provides API and web interface  

## 🚫 What This MVP Does NOT Do

❌ Machine learning or predictions  
❌ Production line simulation  
❌ Workload optimization  
❌ Operation sequencing  
❌ Grouping operations by operator  

Each operation remains independent for detailed analysis.

---

**Need Help?** Check the full README.md for detailed documentation.

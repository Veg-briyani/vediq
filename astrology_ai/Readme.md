# 🌌 Astrology AI - Phase 1: Foundation & Rule Extraction System

An intelligent system for extracting structured astrological knowledge from classical Vedic texts and building a comprehensive knowledge base.

## 📋 Table of Contents
- [🎯 Project Mission](#-project-mission)
- [⚡ Quick Start](#-quick-start)
- [🏗️ Architecture](#️-architecture)
- [🔧 Configuration System](#-configuration-system)
- [📚 Usage Examples](#-usage-examples)
- [📊 Features](#-features)
- [🛠️ Development](#️-development)

## 🎯 Project Mission

Building a bridge between ancient Vedic wisdom and modern AI to create an intelligent astrology companion that learns from classical texts and provides accurate, source-attributed interpretations.

### Phase 1 Goals (Current)
- ✅ **Foundation**: Robust text extraction and processing
- ✅ **Rule Extraction**: NLP-based extraction from classical texts
- ✅ **Knowledge Storage**: SQLite database with source attribution
- ✅ **Configuration System**: Centralized path and settings management
- ✅ **CLI Interface**: Complete command-line tools
- ✅ **Source Hierarchy**: Authority-based source management

### Phase 2 Goals (Future)
- 🔮 **Chart Calculation**: Swiss Ephemeris integration
- 🔮 **Rule Matching**: Apply extracted rules to birth charts
- 🔮 **Interpretation Engine**: Generate natural language readings
- 🔮 **Web Interface**: API and frontend for broader access

## ⚡ Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd astrology_ai

# Install dependencies
pip install -r requirements.txt

# Initialize the system
python main.py setup
```

### Basic Usage
```bash
# Add PDF books to data/books/ then process them
python main.py cli process-book data/books/your_book.pdf \
    --source-title "Classical Astrology Text" \
    --authority classical \
    --extract-rules

# Search for rules
python main.py cli search-rules --planet Mars --house 7

# View system statistics
python main.py cli stats

# Export knowledge base
python main.py cli export-knowledge
```

## 🏗️ Architecture

### Project Structure
```
astrology_ai/
├── 📁 src/                          # Core system modules
│   ├── __init__.py                  # Main AstrologyAI class + config integration
│   ├── data_models.py               # Pydantic models for rules and charts
│   ├── document_processor.py        # PDF extraction & text cleaning
│   ├── rule_extractor.py            # NLP-based rule parsing with regex
│   ├── knowledge_base.py            # SQLite database with search capabilities
│   ├── source_manager.py            # Source hierarchy and authority management
│   ├── cli.py                       # Click-based command interface
│   ├── chart_calculator.py          # Phase 2: Chart calculation (placeholder)
│   ├── interpreter.py               # Phase 2: Rule interpretation (placeholder)
│   └── source_manager.py            # Source authority and conflict resolution
├── 📁 data/                         # Data storage with organized subdirectories
│   ├── 📚 books/                    # PDF storage for classical texts
│   ├── 📝 rules/                    # SQLite database files
│   ├── 📈 charts/                   # Future: generated chart data
│   ├── 📤 exports/                  # JSON exports and backups
│   ├── 📋 logs/                     # Application logs
│   ├── 💾 cache/                    # Cached processing results
│   ├── 🔄 backup/                   # Database backups
│   └── 🗂️ temp/                     # Temporary processing files
├── 📁 config/                       # Configuration management
│   ├── settings.py                  # Centralized configuration system
│   ├── sources.yaml                 # Source authority hierarchy
│   └── app_config.yaml.sample       # Sample configuration file
├── main.py                          # Application entry point
└── requirements.txt                 # Python dependencies
```

## 🔧 Configuration System

### Centralized Path Management
The system now uses a centralized configuration approach that eliminates hardcoded paths and provides flexible directory management.

#### Configuration Features
- **Automatic Directory Creation**: All required directories are created automatically
- **Flexible Paths**: Easy to customize directory structure via configuration
- **Environment Adaptation**: Works across different deployment scenarios
- **Validation**: Built-in validation to ensure proper setup

#### View Current Configuration
```bash
# See all configuration details
python main.py config

# CLI configuration info
python main.py cli config-info
```

#### Directory Structure
| Directory | Purpose | Configurable |
|-----------|---------|--------------|
| `data/books/` | PDF storage for classical texts | ✅ |
| `data/rules/` | SQLite database files | ✅ |
| `data/charts/` | Future chart data storage | ✅ |
| `data/exports/` | JSON exports and knowledge dumps | ✅ |
| `data/logs/` | Application and processing logs | ✅ |
| `data/cache/` | Cached processing results | ✅ |
| `data/backup/` | Database backups | ✅ |
| `data/temp/` | Temporary processing files | ✅ |

#### Custom Configuration
Create a custom `config/app_config.yaml` file to override defaults:
```yaml
directories:
  data_dir: "my_data"
  books_subdir: "classical_texts"
  exports_subdir: "knowledge_exports"

processing:
  min_confidence_threshold: 0.4
  enable_ocr_correction: true
  max_concurrent_files: 5
```

## 📚 Usage Examples

### Document Processing
```bash
# Process a single book with full rule extraction
python main.py cli process-book data/books/saravali.pdf \
    --source-title "Saravali" \
    --author "Kalyana Varma" \
    --authority classical \
    --extract-rules \
    --show-samples

# Batch process all PDFs in the books directory
python main.py cli batch-process \
    --authority classical \
    --extract-rules

# Process with custom output
python main.py cli process-book data/books/modern_text.pdf \
    --authority modern \
    --output exports/processing_results.json
```

### Knowledge Base Operations
```bash
# Advanced rule searching
python main.py cli search-rules \
    --planet Jupiter \
    --house 10 \
    --min-confidence 0.7 \
    --limit 20 \
    --export exports/jupiter_10th_rules.json

# Export complete knowledge base
python main.py cli export-knowledge \
    --output exports/complete_knowledge_$(date +%Y%m%d).json

# View detailed statistics
python main.py cli stats
```

### System Administration
```bash
# Validate system setup
python main.py cli test-setup

# View configuration details
python main.py cli config-info

# Initialize/reset system
python main.py setup
```

## 📊 Features

### Core Components

#### DocumentProcessor
- **Multi-format PDF support**: PyPDF2 and pdfplumber integration
- **Intelligent text cleaning**: OCR error correction and normalization
- **Astrological content detection**: Filters non-relevant content
- **Source attribution**: Maintains connection to original text

#### RuleExtractor
- **Pattern-based extraction**: Sophisticated regex patterns for Vedic astrology
- **Sanskrit term recognition**: Handles both Sanskrit and English terminology
- **Confidence scoring**: Each extracted rule includes confidence metrics
- **OCR correction**: Fixes common OCR errors in scanned texts

#### KnowledgeBase
- **SQLite backend**: Fast, reliable local storage
- **Full-text search**: Advanced querying capabilities
- **Source tracking**: Every rule linked to its source
- **Conflict handling**: Authority-based rule weighting

#### SourceManager
- **Authority hierarchy**: Classical > Traditional > Modern > Commentary
- **Conflict resolution**: Automatic handling of contradictory rules
- **Source validation**: Ensures proper attribution
- **Processing settings**: Configurable extraction parameters

### Search & Export Capabilities
- **Multi-criteria search**: Planet, house, sign, source, confidence filters
- **JSON export**: Complete knowledge base dumps
- **Source attribution**: All rules maintain connection to original texts
- **Statistics dashboard**: Comprehensive system metrics

## 🛠️ Development

### Code Quality Standards
- **Type Hints**: Comprehensive type annotations throughout
- **Error Handling**: Robust exception handling with meaningful messages
- **Configuration-driven**: No hardcoded paths or settings
- **Modular Design**: Clear separation of concerns
- **Documentation**: Comprehensive docstrings and comments

### Testing the System
```bash
# Run comprehensive system test
python main.py test

# Test individual components
python main.py cli test-setup

# Validate configuration
python main.py config
```

### Adding New Sources
1. **Add PDF to books directory**: `data/books/new_text.pdf`
2. **Update sources.yaml**: Add source metadata
3. **Process with authority level**:
   ```bash
   python main.py cli process-book data/books/new_text.pdf \
       --source-title "New Classical Text" \
       --authority classical \
       --extract-rules
   ```

### Configuration Management
The system supports flexible configuration through:
- **Default settings**: Sensible defaults that work out-of-the-box
- **YAML configuration**: Override defaults with `config/app_config.yaml`
- **Environment adaptation**: Automatically adapts to different environments
- **Validation**: Built-in checks ensure proper configuration

### Directory Customization
Customize the directory structure by creating `config/app_config.yaml`:
```yaml
directories:
  data_dir: "astrology_data"           # Main data directory
  books_subdir: "source_texts"        # PDF storage
  rules_subdir: "extracted_rules"     # Database storage
  exports_subdir: "knowledge_exports" # Export files
  logs_subdir: "application_logs"     # Log files
```

## 🔄 Phase 2 Roadmap

### Chart Calculation Engine
- **Swiss Ephemeris integration**: Precise astronomical calculations
- **Multiple chart types**: D-1, D-9, D-10, and other divisional charts
- **Ayanamsa support**: Various calculation methods (Lahiri, etc.)
- **House systems**: Placidus, Equal House, and others

### Interpretation Engine
- **Rule matching**: Apply extracted rules to birth charts
- **Conflict resolution**: Handle contradictory predictions intelligently
- **Natural language generation**: Human-readable interpretations
- **Confidence weighting**: Source authority impacts interpretation confidence

### Advanced Features
- **Dasha calculations**: Planetary periods and sub-periods
- **Transit analysis**: Current planetary influences
- **Yoga identification**: Complex planetary combinations
- **Remedial suggestions**: Based on classical recommendations

## 📈 Current Status

### Phase 1 Achievements ✅
- **Rock-solid foundation**: Configurable, modular architecture
- **Intelligent extraction**: High-accuracy rule extraction from classical texts
- **Comprehensive storage**: SQLite database with full-text search
- **Source attribution**: Every rule traced to its original source
- **Authority hierarchy**: Classical texts prioritized over modern interpretations
- **Professional CLI**: Complete command-line interface
- **Configuration system**: Centralized, flexible path and settings management

### Knowledge Base Statistics
- **Sources processed**: Multiple classical and traditional texts
- **Rules extracted**: Growing database of astrological principles
- **Search capabilities**: Multi-criteria filtering and export
- **Export formats**: JSON with complete metadata

---

**🌟 Happy Building!** You're creating a bridge between ancient wisdom and modern AI. Each book you process makes the system smarter and more knowledgeable about the timeless art of astrology.

### Quick Commands Reference
```bash
python main.py setup              # Initialize system
python main.py config             # Show configuration
python main.py cli --help         # Full CLI help
python main.py cli stats          # Knowledge base statistics
python main.py cli export-knowledge  # Export all rules
```
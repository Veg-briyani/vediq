"""
Centralized configuration system for Astrology AI
Eliminates hardcoded paths and provides flexible configuration management
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import yaml


@dataclass
class DirectoryConfig:
    """Configuration for project directory structure"""
    
    # Base directories
    project_root: Path
    data_dir: Path
    config_dir: Path
    src_dir: Path
    
    # Data subdirectories
    books_dir: Path
    rules_dir: Path
    charts_dir: Path
    temp_dir: Path
    logs_dir: Path
    exports_dir: Path
    cache_dir: Path
    
    # Database files
    main_database: Path
    test_database: Path
    backup_dir: Path
    
    def __post_init__(self):
        """Ensure all directories exist"""
        directories_to_create = [
            self.data_dir, self.books_dir, self.rules_dir, self.charts_dir,
            self.temp_dir, self.logs_dir, self.exports_dir, self.cache_dir,
            self.backup_dir
        ]
        
        for directory in directories_to_create:
            directory.mkdir(parents=True, exist_ok=True)


@dataclass 
class ProcessingConfig:
    """Configuration for document processing and rule extraction"""
    
    # Text processing settings
    min_sentence_length: int = 10
    max_sentence_length: int = 500
    min_confidence_threshold: float = 0.3
    
    # Batch processing
    max_concurrent_files: int = 3
    chunk_size: int = 1000
    
    # Rule extraction
    enable_ocr_correction: bool = True
    strict_pattern_matching: bool = False
    preserve_original_text: bool = True


class AstrologyAIConfig:
    """
    Main configuration class for the Astrology AI system
    Provides centralized access to all configuration settings
    """
    
    def __init__(self, config_file: str = None):
        self.project_root = Path(__file__).parent.parent
        self.config_file = config_file or self.project_root / "config" / "app_config.yaml"
        
        # Load custom configuration if it exists
        self.custom_config = self._load_custom_config()
        
        # Initialize directory configuration
        self.directories = self._setup_directories()
        
        # Initialize processing configuration
        self.processing = self._setup_processing_config()
    
    def _setup_directories(self) -> DirectoryConfig:
        """Setup directory configuration with custom overrides"""
        
        # Default directory structure
        defaults = {
            'data_dir': 'data',
            'books_subdir': 'books',
            'rules_subdir': 'rules', 
            'charts_subdir': 'charts',
            'temp_subdir': 'temp',
            'logs_subdir': 'logs',
            'exports_subdir': 'exports',
            'cache_subdir': 'cache',
            'backup_subdir': 'backup'
        }
        
        # Apply custom overrides
        config = {**defaults, **self.custom_config.get('directories', {})}
        
        # Resolve paths
        data_dir = self.project_root / config['data_dir']
        
        return DirectoryConfig(
            project_root=self.project_root,
            data_dir=data_dir,
            config_dir=self.project_root / "config",
            src_dir=self.project_root / "src",
            
            # Data subdirectories
            books_dir=data_dir / config['books_subdir'],
            rules_dir=data_dir / config['rules_subdir'],
            charts_dir=data_dir / config['charts_subdir'],
            temp_dir=data_dir / config['temp_subdir'],
            logs_dir=data_dir / config['logs_subdir'],
            exports_dir=data_dir / config['exports_subdir'],
            cache_dir=data_dir / config['cache_subdir'],
            
            # Database files
            main_database=data_dir / "astrology_rules.db",
            test_database=data_dir / config['rules_subdir'] / "test_astrology.db",
            backup_dir=data_dir / config['backup_subdir']
        )
    
    def _setup_processing_config(self) -> ProcessingConfig:
        """Setup processing configuration with custom overrides"""
        
        defaults = {
            'min_sentence_length': 10,
            'max_sentence_length': 500,
            'min_confidence_threshold': 0.3,
            'max_concurrent_files': 3,
            'chunk_size': 1000,
            'enable_ocr_correction': True,
            'strict_pattern_matching': False,
            'preserve_original_text': True
        }
        
        config = {**defaults, **self.custom_config.get('processing', {})}
        
        return ProcessingConfig(**config)
    
    def _load_custom_config(self) -> Dict[str, Any]:
        """Load custom configuration from YAML file"""
        
        if self.config_file and Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
        
        return {}
    
    def get_database_path(self, database_type: str = "main") -> Path:
        """Get database path by type"""
        
        database_paths = {
            "main": self.directories.main_database,
            "test": self.directories.test_database
        }
        
        return database_paths.get(database_type, self.directories.main_database)
    
    def get_export_path(self, filename: str) -> Path:
        """Get path for export files"""
        return self.directories.exports_dir / filename
    
    def get_temp_path(self, filename: str) -> Path:
        """Get path for temporary files"""
        return self.directories.temp_dir / filename
    
    def validate_setup(self) -> Dict[str, bool]:
        """Validate that the configuration and directories are properly set up"""
        
        results = {}
        
        # Check directory existence
        critical_dirs = [
            ('data_dir', self.directories.data_dir),
            ('books_dir', self.directories.books_dir),
            ('config_dir', self.directories.config_dir),
            ('src_dir', self.directories.src_dir)
        ]
        
        for name, path in critical_dirs:
            results[f"{name}_exists"] = path.exists()
        
        # Check write permissions
        for name, path in critical_dirs:
            if path.exists():
                results[f"{name}_writable"] = os.access(path, os.W_OK)
            else:
                results[f"{name}_writable"] = False
        
        # Check configuration file
        results['config_file_exists'] = self.config_file and Path(self.config_file).exists()
        results['sources_yaml_exists'] = (self.directories.config_dir / "sources.yaml").exists()
        
        return results
    
    def create_sample_config(self) -> None:
        """Create a sample configuration file"""
        
        sample_config = {
            'directories': {
                'data_dir': 'data',
                'books_subdir': 'books',
                'rules_subdir': 'rules',
                'charts_subdir': 'charts',
                'temp_subdir': 'temp',
                'logs_subdir': 'logs',
                'exports_subdir': 'exports',
                'cache_subdir': 'cache',
                'backup_subdir': 'backup'
            },
            'processing': {
                'min_sentence_length': 10,
                'max_sentence_length': 500,
                'min_confidence_threshold': 0.3,
                'max_concurrent_files': 3,
                'chunk_size': 1000,
                'enable_ocr_correction': True,
                'strict_pattern_matching': False,
                'preserve_original_text': True
            },
            'logging': {
                'level': 'INFO',
                'file_logging': True,
                'console_logging': True,
                'log_rotation': True,
                'max_log_files': 5
            }
        }
        
        sample_path = self.directories.config_dir / "app_config.yaml.sample"
        
        with open(sample_path, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False, indent=2)
        
        print(f"✅ Sample configuration created at: {sample_path}")


# Global configuration instance
_config_instance = None

def get_config() -> AstrologyAIConfig:
    """Get the global configuration instance"""
    global _config_instance
    
    if _config_instance is None:
        _config_instance = AstrologyAIConfig()
    
    return _config_instance

def reset_config():
    """Reset the global configuration instance (useful for testing)"""
    global _config_instance
    _config_instance = None


# Convenience functions for common paths
def get_books_dir() -> Path:
    """Get the books directory path"""
    return get_config().directories.books_dir

def get_rules_dir() -> Path:
    """Get the rules directory path"""
    return get_config().directories.rules_dir

def get_database_path(db_type: str = "main") -> Path:
    """Get database path"""
    return get_config().get_database_path(db_type)

def get_export_path(filename: str) -> Path:
    """Get export file path"""
    return get_config().get_export_path(filename)


if __name__ == "__main__":
    # Test configuration setup
    config = AstrologyAIConfig()
    
    print("🔧 Astrology AI Configuration Test")
    print("=" * 50)
    
    print(f"Project Root: {config.directories.project_root}")
    print(f"Data Directory: {config.directories.data_dir}")
    print(f"Books Directory: {config.directories.books_dir}")
    print(f"Database Path: {config.get_database_path()}")
    
    # Validate setup
    validation = config.validate_setup()
    print("\n📊 Validation Results:")
    for check, result in validation.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}: {result}")
    
    # Create sample config
    config.create_sample_config()

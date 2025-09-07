# VR Metadata Inserter

A simple web application that helps you rename VR video files with proper naming conventions for compatibility across different VR players.

## Features

- **Multi-Player Support**: Works with Playa VR, Skybox VR Player, Pigasus VR, Rad TV, Commedia, Oculus Video App, and more
- **Automatic Naming**: Applies correct filename patterns based on your chosen VR player
- **Batch Processing**: Select multiple MP4 files and rename them all at once
- **Live Preview**: See exactly how your files will be renamed before exporting
- **No Re-encoding**: Simply copies files with new names - no quality loss

## Supported VR Players

- **Universal Patterns** (work with most players)
- **Playa VR** - `_180_LR`, `_VR180_LR`, `_SBS_180`, `_stereo_180`
- **Skybox VR Player** - `_3dh`, `_LR`, `_SBS`, `_180x180`, `_360`
- **Pigasus VR** - `_LRF`, `_LR`
- **Rad TV** - `_180`, `_360`, `_sbs`, `_lr`, `_tb`
- **Commedia** - `_SBS`, `_LR`, `_3Dh`, `_180`, `_360`
- **Oculus Video App** - `_180_LR`, `_180_TB`, `_360_LR`, `_360_TB`

## Quick Start

1. **Install Dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Add Your Videos**:
   - Place your original MP4 files in the `raw/` directory
   - The app will automatically detect them

3. **Run the Application**:
   ```bash
   python app.py
   ```
   - The app will open in your browser at `http://127.0.0.1:5001`

4. **Use the Interface**:
   - Select your VR player from the dropdown
   - Choose the naming convention
   - Select which files to rename
   - Preview the new names
   - Click "Export renamed copies" to save to `fixed_metadata/`

## Directory Structure

```
VR-Metadata-Inserter/
├── app.py                 # Flask web application
├── requirements.txt       # Python dependencies
├── naming_convention.txt  # VR player naming patterns
├── templates/
│   └── index.html        # Web interface
├── raw/                  # Place your original MP4 files here
│   └── .gitkeep
└── fixed_metadata/       # Renamed files will be saved here
    └── .gitkeep
```

## How It Works

This tool solves a common problem: **VR players often require specific filename patterns to automatically detect VR content**, even when the video files contain proper VR metadata.

Your Qoocam exports already have correct VR metadata, but some players (like Playa VR) check filenames first. This tool adds the appropriate naming convention to make your files compatible with any VR player.

## Example

**Original filename**: `Test_1_2k_test_low_mp4.mp4`
**After processing with Playa VR `_180_LR`**: `Test_1_2k_test_low_mp4_180_LR.mp4`

The renamed file will now be automatically recognized as VR180 content by Playa VR and other compatible players.

## Contributing

Feel free to submit issues or pull requests to add support for more VR players or improve the interface.

## License

MIT License - feel free to use and modify as needed.

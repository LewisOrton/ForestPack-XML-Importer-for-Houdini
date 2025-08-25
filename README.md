# Forest Pack XML Importer for Houdini

This repository provides a Python SOP scriptto help bring **ForestPack** scatter data (from 3ds Max) into Houdini.

---

## Features

- **Python SOP**:  
  - Reads a Forest Pack XML file exported from 3ds Max.  
  - Creates one point per scattered item.  
  - Extracts attributes:
    - `geoID` (integer ID)  
    - `geomName` (original asset name)  
    - `finalTM` (row-major 4×4 transform matrix, with translation scaled down by `0.001`)  
  - Adds a global attribute `import_count` with the number of items imported.  

---

## Usage

### Python SOP Node

1. Create a **Python SOP** in Houdini.  
2. Add a **String parameter** to the node and name it `xmlfile`.  
3. Paste the [python_sop.py](./python_sop.py) code into the Python SOP.  
4. Point the `xmlfile` parameter to your Forest Pack XML file.  
5. Cook the node. You will get one point per scattered item, with the attributes above.
![Preview](./screenshot.jpg)
> The `finalTM` attribute is stored as a 16-float tuple.  
> You can convert it to a matrix in VEX if you want to instance geometry.

# Python SOP
import os, re, xml.etree.ElementTree as ET
import hou

node = hou.pwd()
geo  = node.geometry()

# ---- config: file path from a string parm "xmlfile" ----
xml_path = node.evalParm("xmlfile")  # add a String parameter named "xmlfile" on the node
if not xml_path or not os.path.isfile(xml_path):
    raise hou.NodeError("Set a valid XML file path on parameter 'xmlfile'.")

# ---- helpers ----
_triplets_re = re.compile(r"\[([^\]]+)\]")

def parse_finalTM(s, scale=0.001):
    """
    Input: '[[r1][r2][r3][pos]]'
    Output: 16-float row-major 4x4, translation scaled down
    """
    blocks = _triplets_re.findall(s)
    if len(blocks) != 4:
        raise ValueError("finalTM must contain exactly 4 bracketed triplets")
    rows = []
    for b in blocks[:3]:
        rows.append([float(x) for x in b.split(",")])
    pos = [float(x) * scale for x in blocks[3].split(",")]
    # build 4x4 row-major
    m = [
        rows[0][0], rows[0][1], rows[0][2], 0.0,
        rows[1][0], rows[1][1], rows[1][2], 0.0,
        rows[2][0], rows[2][1], rows[2][2], 0.0,
        pos[0],     pos[1],     pos[2],     1.0,
    ]
    return m

# ---- prepare geometry ----
geo.clear()

a_geoID   = geo.addAttrib(hou.attribType.Point, "geoID", 0)
a_geomName = geo.addAttrib(hou.attribType.Point, "geomName", "")
a_final   = geo.addAttrib(hou.attribType.Point, "finalTM", tuple([0.0]*16))

# ---- parse and build ----
root = ET.parse(xml_path).getroot()

count = 0
for elem in root.iter():
    if "geomID" in elem.attrib and "finalTM" in elem.attrib:
        try:
            gid = int(elem.attrib.get("geomID", "0"))
            gname = elem.attrib.get("geomName", "")
            mat = parse_finalTM(elem.attrib["finalTM"], scale=0.001)
        except Exception:
            continue
        pt = geo.createPoint()
        pt.setAttribValue(a_geoID, gid)
        pt.setAttribValue(a_geomName, gname)
        pt.setAttribValue(a_final, tuple(mat))
        count += 1

geo.addAttrib(hou.attribType.Global, "import_count", 0)
geo.setGlobalAttribValue("import_count", count)

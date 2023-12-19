"""
Author: Johannes Volz 4 IPA Fraunhofer
Email: Johannes.Volz@ipa.fraunhofer.de



"""
import os
import xml.etree.ElementTree as et



def writer(marker_size, AB0, AC0, AB1, AC1, called = True):
    
    xml_file_path = 'piTagIni.xml'
    i=0
    # Check if the XML file exists in the current folder
    while True:
        if not os.path.exists(xml_file_path):
            ID=1
            root = et.Element("FiducialDetector")
            tree = et.ElementTree(root)

            break
        else:
            
            verify = input(f"\nFile with name: '{xml_file_path}' exist, want to add marker into it?[y,N]")
            
            if verify == 'y':
                tree = et.parse(xml_file_path)
                root = tree.getroot()
                max_id=0

                for pi in root.findall(".//PI[ID]"):
                    existing_id = int(pi.find("ID").get("value", 0))
                    max_id = max(max_id, existing_id)
                
                ID=max_id+1
                
                break    
            else: 

                i_prev=i-1
                base_path, extension = os.path.splitext(xml_file_path)
                base_path = base_path.replace('_', '')  # Remove all underscores from the base path
                base_path = ''.join(char for char in base_path if not char.isdigit())    
                xml_file_path = f"{base_path}_{i}.xml"
                i+=1


    data = {
        
        ID: {
            "marker_size": marker_size/100, #convert from [cm] into [m]
            "AB0": AB0,
            "AC0": AC0,
            "AB1": AB1,
            "AC1": AC1,
            "offset_x": "PLACEHOLDER",
            "offset_y": "PLACEHOLDER",
            "sharpness_area_x": -0.01,
            "sharpness_area_y": -0.01,
            "sharpness_area_width": 0.12,
            "sharpness_area_height": 0.12
        },
    }

    print(f"\nEnter data for Marker {ID} (Press Enter to use default values):")

    marker_data = data.get(ID, {})  # Get defaults for the marker

    if not called: #ask all values if not called by external function
        marker_data["marker_size"] = float(input(f"Enter marker size in m [{marker_data.get('marker_size', '')}]: ") or marker_data.get("marker_size", ""))
        marker_data["AB0"] = float(input(f"Enter CrossRatioLine0 AB value [{marker_data.get('AB0', '')}]: ") or marker_data.get("AB0", ""))
        marker_data["AC0"] = float(input(f"Enter CrossRatioLine0 AC value [{marker_data.get('AC0', '')}]: ") or marker_data.get("AC0", ""))
        marker_data["AB1"] = float(input(f"Enter CrossRatioLine1 AB value [{marker_data.get('AB1', '')}]: ") or marker_data.get("AB1", ""))
        marker_data["AC1"] = float(input(f"Enter CrossRatioLine1 AC value [{marker_data.get('AC1', '')}]: ") or marker_data.get("AC1", ""))

    marker_data["offset_x"] = input(f"Enter Offset x value [{marker_data.get('offset_x', '')}]: ") or str(marker_data.get("offset_x", ""))
    marker_data["offset_y"] = input(f"Enter Offset y value [{marker_data.get('offset_y', '')}]: ") or str(marker_data.get("offset_y", ""))
    marker_data["sharpness_area_x"] = float(input(f"Enter SharpnessArea x value [{marker_data.get('sharpness_area_x', '')}]: ") or marker_data.get("sharpness_area_x", ""))
    marker_data["sharpness_area_y"] = float(input(f"Enter SharpnessArea y value [{marker_data.get('sharpness_area_y', '')}]: ") or marker_data.get("sharpness_area_y", ""))
    marker_data["sharpness_area_width"] = float(input(f"Enter SharpnessArea width value [{marker_data.get('sharpness_area_width', '')}]: ") or marker_data.get("sharpness_area_width", ""))
    marker_data["sharpness_area_height"] = float(input(f"Enter SharpnessArea height value [{marker_data.get('sharpness_area_height', '')}]: ") or marker_data.get("sharpness_area_height", ""))

        
    pi = et.SubElement(root, "PI")
    et.SubElement(pi, "ID", value=str(ID))
    pi.append(et.Comment('Tag size in [m]'))
    et.SubElement(pi, "LineWidthHeight", value=str(float(marker_data.get("marker_size"))))
    pi.append(et.Comment('Cross ratios line 0 and 1'))
    pi.append(et.Comment('Measurements in percent relative to the tag size'))
    et.SubElement(pi, "CrossRatioLine0", AB=str(marker_data.get("AB0")), AC=str(marker_data.get("AC0")))
    et.SubElement(pi, "CrossRatioLine1", AB=str(marker_data.get("AB1")), AC=str(marker_data.get("AC1")))
    pi.append(et.Comment('Offset for native tag corrdinates'))
    pi.append(et.Comment('e.g. position of tag in object centric ccordinate system'))
    et.SubElement(pi, "Offset", x=str(marker_data.get("offset_x", -0.125)), y=str(marker_data.get("offset_y", 0.175)))

    sharpness_area_attrs = {
        "x": str(marker_data.get("sharpness_area_x", -0.01)),
        "y": str(marker_data.get("sharpness_area_y", -0.01)),
        "width": str(marker_data.get("sharpness_area_width", 0.12)),
        "height": str(marker_data.get("sharpness_area_height", 0.12))
    }
    pi.append(et.Comment('Rectangle describing the area for sharpness computation in 2d coordinates within the marker plane with respect to the marker origin'))
    et.SubElement(pi, "SharpnessArea", **sharpness_area_attrs)

    et.indent(tree, space="    ")
    tree.write(xml_file_path)


if __name__ == "__main__":
    writer(10, 0.4, 0.6, 0.2, 0.8, False)

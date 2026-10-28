# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import modules for file system operations (os), JSON parsing (json), 
# and regular expressions -- regex (re)
import os, json, re
from pathlib import Path

# Import PIL for image loading and matplotlib for visualization
from PIL import Image
import matplotlib.pyplot as plt


# Class for visualizing SEM images alongside selected metadata
class SEMVisualizer:
    def __init__(self, json_path, image_path):
        # Store the path to the cleaned metadata JSON file
        self.json_path = json_path
        
        # Store the path to the SEM image file
        self.image_path = image_path
        
        # Define the list of metadata variables to extract and display
        self.variables = [
            "AP_WD",
            "AP_BEAM_TIME",
            "AP_IMAGE_PIXEL_SIZE",
            "AP_HOLDER_HEIGHT",
            "AP_BEAM_CURRENT",
            "AP_HOLDER_DIAMETER"]        
        
        # Initialize an empty dictionary to hold loaded metadata
        self.metadata = {}

    # Load metadata from JSON file into self.metadata
    def load_metadata(self):
        """
        Reads the cleaned JSON file (self.json_path) into self.metadata.
        """

        # TODO (Task 3): implement this method
        with open(self.json_path, 'r') as f:
            self.metatdata = json.load(f)
        
        # raise NotImplementedError("load_metadata is not implemented yet")       


    def clean_value(self, raw_value, variable_name=None):
        """
        Splits a cleaned metadata value into its number and unit.

        The value must be a (signed) number, optionally in scientific
        notation, followed by a unit. Otherwise ("N/A", "N/A") is returned.

        Examples:
            "3.18 mm"         ->  ("3.18", "mm")
            "-13 pA"          ->  ("-13", "pA")
            "2.34e-006 mbar"  ->  ("2.34e-006", "mbar")
            "InLens" or None  ->  ("N/A", "N/A")

        Returns:
            (value, unit) as strings, or ("N/A", "N/A") if no
            number followed by a unit is found
        """

        # Ensure the input is a string before applying regex
        if not isinstance(raw_value, str):
            return ("N/A", "N/A")

        # Use regex to match a signed number (optionally in scientific notation)
        # followed by its unit, e.g. '-13 pA', '2.34e-006 mbar'
        match = re.fullmatch(
            r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([^\d\s].*)', raw_value.strip())

        # If a match is found, return the value and the unit
        if match:
            value, unit = match.groups()
            return (value, unit)

        # Return fallback values (Not Available) if no match is found
        return ("N/A", "N/A")

    def extract_variables(self):
        """
        Extracts selected metadata variables and formats
        them into (name, value, unit) tuples for display.        
        Missing variables give (name, "N/A", "N/A").
        Return the list of formatted metadata rows
        """

        # TODO (Task 3): implement this method
        
        meta_list = []
        
        for var in self.variables:
            value = self.clean_value(self.metadata, var)
            meta_list.append((var, value[0], value[1]))
            
        return meta_list
            
        # raise NotImplementedError("extract_variables is not implemented yet")



    def show_image_with_table(self):
        """
        Displays the SEM image alongside a formatted metadata
        table and saves the combined output as a figure.

        1. Loads the metadata.
        2. Builds a figure with two vertically stacked panels:
           the grayscale SEM image (top) and a table with the
           column labels "Variable", "Value", "Unit" (bottom).
        3. Creates the folder ./output if needed.
        4. Saves the figure as ./output/<image name without extension>.png
        5. Displays the figure, then closes it.
        """

        # TODO (Task 3): implement this method
        column = ['Variable', 'Value', 'Unit']

	image_name = Path(self.image_path).with_suffix(".png").name
        
        self.load_metadata()
        
        meta_table = self.extract_variables()
        
        with Image.open(self.image_path) as im_sem:
            
            fig, (ax_img, ax_tab) = plt.subplots(2,1)
            
            #plotting the image on the top half
            ax_img.imshow(im_sem, cmap="gray")
            ax_img.axis("off")
            
            #displaying the table on the bottom half
            ax_tab.axis("off")
            table = ax_tab.table(
                cellText=meta_table,
                colLabels=column,
                loc="center",
                cellLoc="center"
            )
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            
            #create the directory and save the image
            out_dir = Path("output")
            out_dir.mkdir(parents=True, exist_ok=True)
            plt.savefig(out_dir / image_name, dpi=150, bbox_inches="tight")
        
        #raise NotImplementedError("show_image_with_table is not implemented yet")    
        

 

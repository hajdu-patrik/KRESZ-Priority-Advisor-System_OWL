import os
import sys
from owlready2 import *

# Add the current directory to the paths to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# IMPORT THE COMMON LOGIC
from business_logic import setup_kresz_ontology

def generate_static_model():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    model_dir = os.path.join(project_root, 'model')
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    save_path = os.path.join(model_dir, "kresz_model.owl")

    # Create a clean ontology for saving
    onto = get_ontology("http://test.org/kresz_model.owl")

    print("KRESZ ontológia generálása a business_logic.py alapján...")

    # CALL THE COMMON FUNCTION -> It builds the classes and rules
    setup_kresz_ontology(onto)

    # Save
    onto.save(file=save_path, format="rdfxml")
    print(f"✅ SIKERES MENTÉS! Helye: {save_path}")

if __name__ == "__main__":
    generate_static_model()
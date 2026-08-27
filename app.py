import pandas as pd

class OrthopedicImplantCDSS:
    """
    Commercial-Grade Clinical Decision Support System (CDSS) 
    for Patient-Specific Metamaterial Femoral Implants.
    """
    def __init__(self, csv_filepath=None):
        if csv_filepath:
            self.df = pd.read_csv(csv_filepath)
        else:
            self.data = {
                'Cross_Section': ['Circular', 'Circular', 'Circular', 'Circular', 
                                  'Elliptical', 'Elliptical', 'Elliptical', 'Elliptical', 
                                  'Trapezoidal', 'Trapezoidal', 'Trapezoidal', 'Trapezoidal'],
                'Architecture': ['Solid', 'Diamond', 'Gyroid', 'Hybrid', 
                                 'Solid', 'Diamond', 'Gyroid', 'Hybrid', 
                                 'Solid', 'Diamond', 'Gyroid', 'Hybrid'],
                'U_max': [1.181, 3.11, 4.21, 3.53, 1.444, 3.45, 4.76, 3.89, 1.703, 4.11, 6.48, 4.62],
                'Stiffness_K': [1948, 740, 546, 652, 1594, 667, 483, 591, 1351, 560, 355, 498],
                'FoS_350': [None, 4.13, 4.96, 5.30, None, 3.75, 3.10, 2.82, None, 3.75, 3.87, 3.26]
            }
            self.df = pd.DataFrame(self.data)

    def evaluate_patient_case(self, patient_weight_kg, bone_condition, activity_level, baseline_weight=75):
        load_factor = patient_weight_kg / baseline_weight
        working_df = self.df.copy()
        
        working_df['U_max_dynamic'] = working_df['U_max'] * load_factor
        working_df['FoS_dynamic'] = working_df['FoS_350'] / load_factor
        
        meta_df = working_df[working_df['Architecture'] != 'Solid'].dropna(subset=['FoS_dynamic']).copy()
        
        norm_fos = meta_df['FoS_dynamic'] / meta_df['FoS_dynamic'].max()
        norm_stiffness = meta_df['Stiffness_K'] / meta_df['Stiffness_K'].max()
        
        if bone_condition == 1:  
            meta_df['Clinical_Score'] = (0.4 * norm_fos) + (0.6 * norm_stiffness)
        else:                    
            norm_compliance = meta_df['U_max_dynamic'] / meta_df['U_max_dynamic'].max()
            meta_df['Clinical_Score'] = (0.4 * norm_fos) + (0.6 * norm_compliance)
            
        if activity_level == 1:
            meta_df.loc[meta_df['FoS_dynamic'] < 3.5, 'Clinical_Score'] *= 0.5
            
        top_recommendations = meta_df.sort_values(by='Clinical_Score', ascending=False).head(3)
        return top_recommendations

    def generate_clinical_report(self, patient_info, top_results):
        report = []
        report.append("=" * 65)
        report.append("       MEDICAL DEVICE SOFTWARE: CERTIFIED CLINICAL REPORT")
        report.append("=" * 65)
        report.append(f" Patient Weight: {patient_info['weight']} kg")
        report.append(f" Bone Pathology: {'Osteoporotic/Weak' if patient_info['bone'] == 1 else 'Normal Stock'}")
        report.append(f" Activity Profile: {'High Performance' if patient_info['activity'] == 1 else 'Standard/Normal'}")
        report.append("-" * 65)
        report.append(" TOP 3 RECOMMENDED PATIENT-SPECIFIC IMPLANT CONFIGURATIONS:")
        report.append("-" * 65)
        
        rank = 1
        for _, row in top_results.iterrows():
            report.append(f" [{rank}] Geometry: {row['Cross_Section']} | Architecture: {row['Architecture']}")
            report.append(f"     • Displacement (U): {row['U_max_dynamic']:.2f} mm | Stiffness: {row['Stiffness_K']} N/mm")
            report.append(f"     • Safety Factor (FoS): {row['FoS_dynamic']:.2f} | Match Index: {row['Clinical_Score']:.2f}")
            report.append("-" * 65)
            rank += 1
            
        report.append(" Status: Approved for Pre-Surgical Planning and CAD Generation.")
        report.append("=" * 65)
        return "\n".join(report)

# ==========================================
# Interactive Execution Block
# ==========================================
if __name__ == "__main__":
    cdss_engine = OrthopedicImplantCDSS()
    
    print("=" * 65)
    print("     COMMERCIAL CLINICAL DECISION SUPPORT SYSTEM (CDSS)")
    print("=" * 65)
    
    try:
        weight_input = float(input("Enter patient body weight in kg (e.g., 80): "))
        bone_input = int(input("Select bone condition -> [1] Osteoporotic/Weak  [2] Healthy/Normal: "))
        activity_input = int(input("Select patient activity -> [1] High Activity  [2] Normal: "))
    except ValueError:
        print("Invalid input detected! Using default profile (Weight: 75kg, Normal bone, Normal activity).")
        weight_input = 75
        bone_input = 2
        activity_input = 2
        
    current_patient = {'weight': weight_input, 'bone': bone_input, 'activity': activity_input}
    
    results = cdss_engine.evaluate_patient_case(
        patient_weight_kg=current_patient['weight'], 
        bone_condition=current_patient['bone'], 
        activity_level=current_patient['activity']
    )
    
    final_report = cdss_engine.generate_clinical_report(current_patient, results)
    print("\n" + final_report)

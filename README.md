# 🦿 Patient-Specific Metamaterial Femoral Implant - CDSS

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![Domain](https://img.shields.io/badge/Domain-Biomedical%20Engineering%20%7C%20Biomechanics-orange.svg)]()

## 📋 Overview
This repository contains an advanced **Clinical Decision Support System (CDSS)** developed in Python utilizing Object-Oriented Programming (OOP). The software bridges the gap between finite element analysis (FEA) and clinical practice by automatically evaluating and recommending optimal **metamaterial femoral implant configurations** tailored to individual patient profiles.

The algorithm processes mechanical dataset parameters—including cross-sectional geometries (Circular, Elliptical, Trapezoidal) and lattice architectures (Diamond, Gyroid, Hybrid)—to deliver patient-specific, multi-criteria optimized implant selections.

---

## 🚀 Key Features
* **Object-Oriented Architecture (OOP):** Modular, scalable, and structured codebase designed following software engineering best practices.
* **Dynamic Mechanical Scaling:** Automatically scales stress, maximum displacement ($U_{max}$), and safety factors ($FoS$) based on patient-specific body weight and physiological load variations.
* **Clinical-to-Engineering Translation Layer:** Translates qualitative clinical parameters (such as bone stock pathology/osteoporosis and patient activity levels) into quantitative engineering constraints and adaptive weighting systems.
* **Multi-Criteria Decision Making (MCDM):** Evaluates trade-offs between structural stiffness, compliance (to prevent stress-shielding), and safety factors to rank and output the **Top 3 optimal configurations**.
* **Certified Clinical Reporting:** Generates structured, professional English text reports ready for pre-surgical planning.

---

## 📊 Dataset Parameters
The baseline FEA dataset incorporates structural responses across multiple design parameters:
* **Cross-Sections:** Circular, Elliptical, Trapezoidal
* **Lattice Architectures:** Solid, Diamond, Gyroid, Hybrid
* **Evaluated Metrics:** Maximum Displacement ($U_{max}$), Structural Stiffness ($K$), and Factor of Safety ($FoS$).

---

## 🛠️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/Metamaterial-Femoral-Implant-CDSS.git](https://github.com/YOUR-USERNAME/Metamaterial-Femoral-Implant-CDSS.git)
   cd Metamaterial-Femoral-Implant-CDSS

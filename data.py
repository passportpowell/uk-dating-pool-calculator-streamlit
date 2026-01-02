"""
UK Dating Pool Calculator - Data Module
Contains all statistical data, distributions, and constants
"""

# Helper function to normalize distributions
def _normalize(dist):
    """Normalize a distribution dictionary to sum to exactly 1.0"""
    s = sum(dist.values())
    return {k: v/s for k, v in dist.items()}

# UK Population data based on ONS statistics
UK_TOTAL_POPULATION = 67_736_802  # Mid-2022 estimate
UK_ADULT_POPULATION = 52_600_000  # Ages 18+

# Age distribution (% of adults 18+)
AGE_DISTRIBUTION = {
    "18-24": 0.119,
    "25-34": 0.187,
    "35-44": 0.172,
    "45-54": 0.186,
    "55-64": 0.162,
    "65+": 0.174
}

# Detailed ethnicity distribution (Census 2021)
# Normalized to sum to exactly 1.0
ETHNICITY_DISTRIBUTION = _normalize({
    "White British": 0.744,
    "White Irish": 0.009,
    "White Other": 0.062,
    "Asian/Asian British - Indian": 0.030,
    "Asian/Asian British - Pakistani": 0.024,
    "Asian/Asian British - Bangladeshi": 0.010,
    "Asian/Asian British - Chinese": 0.009,
    "Asian/Asian British - Other": 0.020,
    "Black/Black British - African": 0.025,
    "Black/Black British - Caribbean": 0.010,
    "Black/Black British - Other": 0.005,
    "Mixed - White & Black Caribbean": 0.009,
    "Mixed - White & Black African": 0.005,
    "Mixed - White & Asian": 0.008,
    "Mixed - Other": 0.007,
    "Arab": 0.006,
    "Other ethnic group": 0.018
})

# Height distributions (cm)
# Based on NHS and academic studies
MALE_HEIGHT_MEAN = 175.3
MALE_HEIGHT_STD = 7.1
FEMALE_HEIGHT_MEAN = 161.6
FEMALE_HEIGHT_STD = 6.5

# Income brackets (% of working age population)
# Source: ONS ASHE 2023 + HMRC Self Assessment data for high earners
INCOME_DISTRIBUTION_MALE = {
    "Under £20k": 0.25,
    "£20k-£30k": 0.22,
    "£30k-£40k": 0.18,
    "£40k-£50k": 0.13,
    "£50k-£75k": 0.14,
    "£75k-£100k": 0.05,
    "£100k-£150k": 0.02,  # HMRC Self Assessment data
    "£150k-£250k": 0.007, # HMRC: ~400k taxpayers
    "£250k-£500k": 0.003, # HMRC: ~180k taxpayers
    "£500k-£1M": 0.0006,  # HMRC: ~35k taxpayers
    "£1M+": 0.0004        # HMRC: ~23k taxpayers (millionaires+)
}

INCOME_DISTRIBUTION_FEMALE = {
    "Under £20k": 0.32,
    "£20k-£30k": 0.25,
    "£30k-£40k": 0.17,
    "£40k-£50k": 0.11,
    "£50k-£75k": 0.10,
    "£75k-£100k": 0.03,
    "£100k-£150k": 0.015, # HMRC Self Assessment data
    "£150k-£250k": 0.003, # HMRC: ~180k taxpayers
    "£250k-£500k": 0.0012,# HMRC: ~70k taxpayers
    "£500k-£1M": 0.0002,  # HMRC: ~12k taxpayers
    "£1M+": 0.0001        # HMRC: ~6k taxpayers (millionaires+)
}

# Education levels (% of adults)
EDUCATION_DISTRIBUTION = {
    "Below GCSE": 0.15,
    "GCSE/O-Level": 0.23,
    "A-Level or equivalent": 0.21,
    "Undergraduate degree": 0.27,
    "Postgraduate degree": 0.14
}

# BMI/Body Type Distribution (NHS Health Survey for England 2021)
# Based on BMI categories for adults aged 18+
BODY_TYPE_DISTRIBUTION_MALE = {
    "Underweight (BMI < 18.5)": 0.02,
    "Healthy weight (BMI 18.5-24.9)": 0.31,
    "Overweight (BMI 25-29.9)": 0.41,
    "Obese (BMI 30+)": 0.26
}

BODY_TYPE_DISTRIBUTION_FEMALE = {
    "Underweight (BMI < 18.5)": 0.06,
    "Healthy weight (BMI 18.5-24.9)": 0.40,
    "Overweight (BMI 25-29.9)": 0.28,
    "Obese (BMI 30+)": 0.26
}

# Relationship status (% of adults)
SINGLE_RATE = 0.35  # Approximately 35% of UK adults are single

# Children distribution (% of adults by number of children)
# Source: ONS Families and Households 2022
CHILDREN_DISTRIBUTION = {
    "No children": 0.43,
    "1 child": 0.18,
    "2 children": 0.24,
    "3+ children": 0.15
}

# Marriage history (% of adults)
# Source: ONS Marriage statistics 2022
# Note: Same-sex marriage legalized in 2014, so currently married rates are lower for same-sex couples
MARRIAGE_HISTORY = {
    "opposite-sex": {
        "Never married": 0.42,
        "Currently married": 0.46,
        "Divorced": 0.09,
        "Widowed": 0.03
    },
    "same-sex": {
        "Never married": 0.89,  # Much higher as same-sex marriage only legal since 2014
        "Currently married": 0.08,  # Lower due to recent legalization
        "Divorced": 0.02,  # Lower due to shorter time period
        "Widowed": 0.01   # Lower due to younger average age and recent legalization
    }
}

# Marriage rates by ethnicity (% of adults aged 16+ who are married or in civil partnership)
# Source: ONS Census 2021 - England & Wales
MARRIAGE_RATE_BY_ETHNICITY = {
    "Asian/Asian British - Indian": 0.658,
    "Asian/Asian British - Pakistani": 0.634,
    "Asian/Asian British - Bangladeshi": 0.621,
    "Asian/Asian British - Chinese": 0.548,
    "Asian/Asian British - Other": 0.512,
    "White British": 0.448,
    "White Irish": 0.442,
    "Arab": 0.438,
    "White Other": 0.423,
    "Black/Black British - African": 0.387,
    "Other ethnic group": 0.378,
    "Mixed - White & Asian": 0.361,
    "Black/Black British - Caribbean": 0.342,
    "Mixed - Other": 0.328,
    "Black/Black British - Other": 0.312,
    "Mixed - White & Black Caribbean": 0.298,
    "Mixed - White & Black African": 0.289
}

# Interracial marriage statistics (% of married couples)
# Source: ONS Census 2021 - England & Wales
INTERRACIAL_MARRIAGE_DATA = {
    # % of married people in each ethnic group who have a partner of different ethnicity
    "interracial_rate_by_ethnicity": {
        "Mixed - White & Black Caribbean": 0.892,
        "Mixed - White & Black African": 0.881,
        "Mixed - White & Asian": 0.865,
        "Mixed - Other": 0.847,
        "Black/Black British - Caribbean": 0.489,
        "Arab": 0.387,
        "Black/Black British - Other": 0.376,
        "Chinese": 0.364,
        "Other ethnic group": 0.341,
        "Black/Black British - African": 0.284,
        "White Irish": 0.267,
        "White Other": 0.245,
        "Asian/Asian British - Other": 0.198,
        "White British": 0.112,
        "Asian/Asian British - Chinese": 0.187,
        "Asian/Asian British - Indian": 0.143,
        "Asian/Asian British - Pakistani": 0.078,
        "Asian/Asian British - Bangladeshi": 0.063
    },
    # Overall statistics
    "overall": {
        "same_ethnicity": 0.867,
        "different_ethnicity": 0.133
    },
    # Most common interracial pairings (% of all interracial marriages)
    "common_pairings": {
        "White British & White Other": 0.312,
        "White British & Asian Indian": 0.118,
        "White British & Black Caribbean": 0.094,
        "White British & Mixed": 0.087,
        "White British & Asian Pakistani": 0.061,
        "White British & Black African": 0.058,
        "White British & Asian Chinese": 0.047,
        "Asian Indian & Asian Other": 0.038,
        "Other combinations": 0.185
    }
}

# Male baldness distribution by age
# Source: British Association of Dermatologists & Academic research on androgenetic alopecia
BALDNESS_BY_AGE = {
    "18-29": 0.16,
    "30-39": 0.32,
    "40-49": 0.53,
    "50-59": 0.63,
    "60+": 0.80
}

# Sexual orientation distribution (ONS 2022)
SEXUAL_ORIENTATION_DISTRIBUTION = {
    "Heterosexual/Straight": 0.932,
    "Gay or Lesbian": 0.015,
    "Bisexual": 0.017,
    "Other": 0.006,
    "Prefer not to say": 0.030
}

# UK Regional Population Distribution (ONS 2022)
# Population by region with coordinates for mapping
UK_REGIONS = {
    "London": {
        "population": 9_002_488,
        "lat": 51.5074,
        "lon": -0.1278,
        "adult_pop": 7_200_000
    },
    "South East": {
        "population": 9_278_144,
        "lat": 51.3,
        "lon": -0.8,
        "adult_pop": 7_400_000
    },
    "North West": {
        "population": 7_417_397,
        "lat": 53.4808,
        "lon": -2.2426,
        "adult_pop": 5_900_000
    },
    "East of England": {
        "population": 6_398_497,
        "lat": 52.2405,
        "lon": 0.5186,
        "adult_pop": 5_100_000
    },
    "West Midlands": {
        "population": 6_021_653,
        "lat": 52.4862,
        "lon": -1.8904,
        "adult_pop": 4_800_000
    },
    "South West": {
        "population": 5_764_881,
        "lat": 50.7,
        "lon": -3.5,
        "adult_pop": 4_700_000
    },
    "Yorkshire and The Humber": {
        "population": 5_541_262,
        "lat": 53.9583,
        "lon": -1.0803,
        "adult_pop": 4_400_000
    },
    "East Midlands": {
        "population": 4_934_939,
        "lat": 52.8,
        "lon": -1.2,
        "adult_pop": 3_900_000
    },
    "Scotland": {
        "population": 5_479_900,
        "lat": 55.9533,
        "lon": -3.1883,
        "adult_pop": 4_400_000
    },
    "Wales": {
        "population": 3_107_494,
        "lat": 52.1307,
        "lon": -3.7837,
        "adult_pop": 2_500_000
    },
    "Northern Ireland": {
        "population": 1_910_000,
        "lat": 54.5973,
        "lon": -5.9301,
        "adult_pop": 1_500_000
    },
    "North East": {
        "population": 2_647_000,
        "lat": 54.9783,
        "lon": -1.6178,
        "adult_pop": 2_100_000
    }
}

# UK salary benchmarks
MIN_WAGE_ANNUAL = 22308  # National Living Wage 21+: £11.44/hr * 37.5hrs/wk * 52wks
MEDIAN_SALARY = 31285
AVERAGE_SALARY = 33000

# Marriage history (% of adults)
# Source: ONS Marriage statistics 2022
# Note: Same-sex marriage legalized in 2014, so currently married rates are lower for same-sex couples
MARRIAGE_HISTORY = {
    "opposite-sex": {
        "Never married": 0.42,
        "Currently married": 0.46,
        "Divorced": 0.09,
        "Widowed": 0.03
    },
    "same-sex": {
        "Never married": 0.89,  # Much higher as same-sex marriage only legal since 2014
        "Currently married": 0.08,  # Lower due to recent legalization
        "Divorced": 0.02,  # Lower due to shorter time period
        "Widowed": 0.01   # Lower due to younger average age and recent legalization
    }
}

# Marriage statistics by ethnicity (Census 2021 - % married or in civil partnership)
MARRIAGE_RATE_BY_ETHNICITY = {
    "Asian/Asian British - Indian": 0.658,
    "Asian/Asian British - Pakistani": 0.634,
    "Asian/Asian British - Bangladeshi": 0.621,
    "Asian/Asian British - Chinese": 0.548,
    "Asian/Asian British - Other": 0.512,
    "White British": 0.448,
    "White Irish": 0.442,
    "Arab": 0.438,
    "White Other": 0.423,
    "Black/Black British - African": 0.387,
    "Other ethnic group": 0.378,
    "Mixed - White & Asian": 0.361,
    "Black/Black British - Caribbean": 0.342,
    "Mixed - Other": 0.328,
    "Black/Black British - Other": 0.312,
    "Mixed - White & Black Caribbean": 0.298,
    "Mixed - White & Black African": 0.289
}

# Interracial/inter-ethnic marriage data
INTERRACIAL_MARRIAGE_DATA = {
    "same_ethnicity_marriages": 0.867,  # 86.7% marry same ethnicity
    "interracial_marriages": 0.133,     # 13.3% marry different ethnicity
    # Interracial rates by ethnicity
    "interracial_rate_by_ethnicity": {
        "Mixed - White & Black Caribbean": 0.87,
        "Mixed - White & Black African": 0.85,
        "Mixed - White & Asian": 0.84,
        "Mixed - Other": 0.83,
        "Black/Black British - Caribbean": 0.489,
        "Arab": 0.387,
        "Chinese": 0.365,
        "Black/Black British - Other": 0.360,
        "Asian/Asian British - Other": 0.342,
        "Asian/Asian British - Chinese": 0.318,
        "White Other": 0.156,
        "Asian/Asian British - Indian": 0.143,
        "White British": 0.112,
        "Asian/Asian British - Pakistani": 0.078,
        "Asian/Asian British - Bangladeshi": 0.063,
    },
    # Most common interracial pairings (% of all interracial marriages)
    "common_pairings": {
        "White British & White Other": 0.312,
        "White British & Asian Indian": 0.118,
        "White British & Black Caribbean": 0.094,
        "White British & Pakistani": 0.062,
        "White British & Black African": 0.058,
        "White British & Chinese": 0.054,
        "Other pairings": 0.302,
    },
}

# Baby and children health statistics
BABY_HEALTH_DATA = {
    "maternal_mortality": {
        # Maternal deaths per 100,000 live births
        "2011-2013": 12.2,
        "2014-2016": 11.0,
        "2017-2019": 9.1,
        "2020": 10.7,  # Slight increase due to COVID-19
        "2021": 8.9,
        "2022": 8.5,
        "trend": "declining",
        "note": "Significant improvement; Target: <7 per 100,000"
    },
    "stillbirth_rates": {
        # Stillbirths per 1,000 total births (birth + stillbirth)
        "2010": 5.2,
        "2015": 4.7,
        "2019": 3.9,
        "2020": 4.1,
        "2021": 4.0,
        "2022": 3.8,
        "trend": "declining",
        "note": "UK one of best rates globally"
    },
    "infant_mortality": {
        # Deaths per 1,000 live births (under 1 year)
        "2010": 4.7,
        "2015": 3.9,
        "2020": 3.8,
        "2021": 3.7,
        "2022": 3.5,
        "neonatal_mortality": {  # Deaths 0-28 days
            "2010": 3.3,
            "2015": 2.5,
            "2020": 2.3,
            "2021": 2.2,
        },
        "post_neonatal_mortality": {  # Deaths 28 days - 1 year
            "2010": 1.4,
            "2015": 1.4,
            "2020": 1.5,
            "2021": 1.5,
        },
    },
    "birth_defects": {
        # % of births with congenital anomalies
        "chromosomal_disorders": {
            "Down syndrome (Trisomy 21)": 0.144,  # per 1,000 live births
            "Edwards syndrome (Trisomy 18)": 0.076,
            "Patau syndrome (Trisomy 13)": 0.055,
            "Turner syndrome": 0.047,
            "Klinefelter syndrome": 0.094,
        },
        "structural_defects": {
            "congenital_heart_defects": 0.86,  # per 1,000 live births (most common)
            "cleft_lip_palate": 0.17,
            "neural_tube_defects": 0.06,
            "limb_defects": 0.16,
            "gastroschisis": 0.04,
        },
        "total_major_anomalies": 2.5,  # % of all births
        "trend": "stable_or_slight_increase",  # May reflect better detection
    },
    "maternal_complications": {
        "gestational_diabetes": {
            "2010": 3.2,  # % of pregnancies
            "2015": 4.5,
            "2020": 5.8,
            "2022": 6.1,
            "trend": "increasing",
            "note": "Linked to obesity rates"
        },
        "preeclampsia_eclampsia": {
            "2010": 3.8,  # % of pregnancies
            "2020": 3.9,
            "trend": "stable"
        },
        "hypertension": {
            "2010": 4.2,
            "2020": 4.5,
            "trend": "slight increase"
        },
    },
    "child_mental_health": {
        # Mental health disorder prevalence in children (ages 5-15)
        "overall_disorder_prevalence": {
            "2004": 9.6,  # % of children
            "2014": 11.4,
            "2017": 11.9,
            "2022": 15.3,  # Significant increase post-COVID
        },
        "anxiety_disorders": {
            "2004": 3.9,
            "2017": 4.8,
            "2022": 7.1,  # Increased post-COVID
        },
        "depression": {
            "2004": 0.9,
            "2017": 1.5,
            "2022": 2.4,
        },
        "conduct_disorders": {
            "2004": 5.4,
            "2017": 5.1,
            "2022": 6.2,
        },
        "ADHD": {
            "2004": 2.2,
            "2017": 2.8,
            "2022": 3.4,
        },
        "autism_spectrum_disorder": {
            "2004": 0.5,
            "2017": 1.2,
            "2022": 1.8,  # Higher detection rates
        },
    },
    "child_physical_health": {
        "childhood_obesity": {
            # % overweight or obese by age 11
            "2009-2010": 31.5,
            "2015": 34.2,
            "2020": 35.8,
            "2022": 38.3,  # Increased during COVID lockdowns
            "trend": "increasing"
        },
        "asthma": {
            # Diagnosed asthma prevalence
            "2010": 8.5,
            "2015": 9.2,
            "2020": 9.8,
            "2022": 10.1,
        },
        "allergies_eczema": {
            # Eczema/dermatitis prevalence
            "2010": 15.3,
            "2020": 17.8,
            "2022": 18.5,
        },
        "dental_health": {
            # Dental decay in 5-year-olds
            "2007": 31.0,  # % with decay
            "2012": 28.0,
            "2017": 23.0,
            "2022": 21.5,  # Slight improvement
        },
    },
    "parental_age_statistics": {
        # Average age of parents at childbirth
        "mother_mean_age": {
            "1990": 28.8,
            "2000": 29.5,
            "2010": 30.0,
            "2015": 30.7,
            "2020": 31.2,
            "2022": 31.5,
            "trend": "increasing"
        },
        "father_mean_age": {
            "1990": 31.8,
            "2000": 32.5,
            "2010": 33.2,
            "2015": 33.9,
            "2020": 34.4,
            "2022": 34.7,
            "trend": "increasing"
        },
        "mothers_over_35": {
            "1990": 15.2,  # % of all births
            "2000": 19.5,
            "2010": 23.8,
            "2015": 27.3,
            "2020": 29.4,
            "2022": 31.0,  # Now 1 in 3 births
            "trend": "rapid increase"
        },
        "mothers_over_40": {
            "1990": 3.2,
            "2000": 5.1,
            "2010": 7.9,
            "2015": 10.4,
            "2020": 11.8,
            "2022": 12.5,
            "trend": "rapid increase"
        },
        "teen_mothers_under_20": {
            "1990": 8.1,  # % of all births
            "2000": 6.5,
            "2010": 3.7,
            "2015": 2.5,
            "2020": 1.8,
            "2022": 1.5,  # Significant decline
            "trend": "declining"
        },
    },
    "pre_term_birth": {
        "overall_preterm": {
            # Birth before 37 weeks gestation
            "2010": 7.3,  # % of all births
            "2015": 7.8,
            "2020": 8.0,
            "2022": 7.9,
            "trend": "stable with slight increase"
        },
        "very_preterm": {
            # Birth before 32 weeks (more serious)
            "2010": 1.5,
            "2020": 1.7,
            "2022": 1.6,
        },
        "extremely_preterm": {
            # Birth before 28 weeks
            "2010": 0.4,
            "2020": 0.5,
            "2022": 0.5,
        },
    },
    "breast_feeding": {
        "initiation_rate": {
            # % who start breastfeeding
            "2010": 81.0,
            "2015": 83.2,
            "2020": 84.1,
            "2022": 84.5,
        },
        "exclusive_at_6_weeks": {
            "2010": 69.0,
            "2015": 70.5,
            "2020": 71.8,
            "2022": 72.3,
        },
        "continued_at_6_months": {
            "2010": 48.0,
            "2015": 49.2,
            "2020": 50.1,
            "2022": 50.5,
        },
    },
    "developmental_disorders": {
        "learning_disabilities": {
            # % of school-aged children
            "2010": 2.8,
            "2015": 3.2,
            "2020": 3.5,
            "2022": 3.7,
            "trend": "increasing_detection"
        },
        "speech_language_disorders": {
            "2010": 5.2,
            "2015": 5.8,
            "2020": 6.1,
            "2022": 6.5,
            "trend": "increasing"
        },
        "dyslexia": {
            "estimated_prevalence": 10.0,  # % of children
            "diagnosed_2022": 4.5,
            "note": "Often underdiagnosed"
        },
    },
    "birth_complications_by_maternal_age": {
        "under_20": {
            "preterm_birth": 8.5,  # % of births
            "low_birth_weight": 7.2,
            "stillbirth_rate": 4.8,  # per 1,000
            "c_section_rate": 28.0,
        },
        "20_29": {
            "preterm_birth": 7.2,
            "low_birth_weight": 5.8,
            "stillbirth_rate": 3.5,
            "c_section_rate": 30.5,
        },
        "30_34": {
            "preterm_birth": 7.5,
            "low_birth_weight": 6.1,
            "stillbirth_rate": 3.7,
            "c_section_rate": 35.2,
        },
        "35_39": {
            "preterm_birth": 8.2,
            "low_birth_weight": 6.8,
            "stillbirth_rate": 4.5,
            "c_section_rate": 42.8,
        },
        "40_plus": {
            "preterm_birth": 9.8,
            "low_birth_weight": 8.2,
            "stillbirth_rate": 6.4,
            "c_section_rate": 54.3,
        },
    },
    "genetic_conditions_risk_by_maternal_age": {
        "downs_syndrome_risk": {
            "age_20": "1 in 1,500",
            "age_25": "1 in 1,250",
            "age_30": "1 in 952",
            "age_35": "1 in 378",
            "age_40": "1 in 106",
            "age_45": "1 in 30",
        },
        "all_chromosomal_abnormalities": {
            "age_20": "1 in 526",
            "age_25": "1 in 476",
            "age_30": "1 in 385",
            "age_35": "1 in 192",
            "age_40": "1 in 66",
            "age_45": "1 in 21",
        },
    },
    "fertility_and_conception": {
        "ivf_cycles": {
            "2010": 61_000,
            "2015": 69_500,
            "2020": 52_800,  # COVID impact
            "2022": 68_700,
            "success_rate_under_35": 32.0,  # % per cycle
            "success_rate_35_37": 25.0,
            "success_rate_38_39": 19.0,
            "success_rate_40_42": 11.0,
            "success_rate_over_42": 4.0,
        },
        "miscarriage_rates": {
            "overall": 15.0,  # % of known pregnancies
            "by_age": {
                "under_30": 10.0,
                "30_34": 12.0,
                "35_39": 18.0,
                "40_44": 34.0,
                "45_plus": 53.0,
            },
        },
    },
    "neonatal_intensive_care": {
        "nicu_admissions": {
            "2015": 89_000,
            "2020": 94_500,
            "2022": 96_200,
            "admission_rate": 14.2,  # % of live births
        },
        "survival_rates_by_gestation": {
            "22_weeks": 10.0,  # %
            "23_weeks": 26.0,
            "24_weeks": 55.0,
            "25_weeks": 72.0,
            "26_weeks": 82.0,
            "27_weeks": 88.0,
            "28_weeks": 92.0,
            "32_weeks": 98.0,
        },
    },
}

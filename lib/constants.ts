/**
 * Constants for SmartCattle — Tamil Nadu Districts, Regions & Breeds
 */

export const TAMIL_NADU_DISTRICTS = [
  "Ariyalur",
  "Chengalpattu",
  "Chennai",
  "Coimbatore",
  "Cuddalore",
  "Dharmapuri",
  "Dindigul",
  "Erode",
  "Kallakurichi",
  "Kanchipuram",
  "Kanyakumari",
  "Karur",
  "Krishnagiri",
  "Madurai",
  "Mayiladuthurai",
  "Nagapattinam",
  "Namakkal",
  "Nilgiris",
  "Perambalur",
  "Pudukkottai",
  "Ramanathapuram",
  "Ranipet",
  "Salem",
  "Sivaganga",
  "Tenkasi",
  "Thanjavur",
  "Theni",
  "Thoothukudi",
  "Tiruchirappalli",
  "Tirunelveli",
  "Tirupathur",
  "Tiruppur",
  "Tiruvallur",
  "Tiruvannamalai",
  "Tiruvarur",
  "Vellore",
  "Viluppuram",
  "Virudhunagar",
] as const;

export const TAMIL_NADU_REGIONS = TAMIL_NADU_DISTRICTS;

export const CATTLE_BREEDS = [
  // Native Tamil Nadu Breeds
  "Kangayam (கங்கேயம் - Draught)",
  "Umblachery (உம்பளச்சேரி - Delta Draught)",
  "Bargur (பர்கூர் - Erode Hill)",
  "Alambadi (ஆலம்பாடி - Dharmapuri)",
  "Pulikulam / Jellicut (புலிகுளம் - Herd Breed)",
  "Manamurai (மணமுறை - South TN)",
  "Toda Buffalo (தோடா எருமை - Nilgiris)",
  // Popular Dairy Breeds in TN
  "Jersey Crossbred",
  "Holstein Friesian (HF) Crossbred",
  "Sahiwal",
  "Gir",
  "Murrah Buffalo",
  "Surti Buffalo",
  "Country / Desi (நாட்டு மாடு)",
  "Crossbred / Other",
] as const;

export const LACTATION_STATUSES = [
  "Lactating / Milking",
  "Dry",
  "Heifer (Young Female)",
  "Calf",
  "Bull / Breeding",
] as const;

export const VACCINATION_STATUSES = [
  "Fully Vaccinated",
  "Partially Vaccinated",
  "Needs Vaccination",
  "Not Vaccinated",
] as const;

// ─────────────────────────────────────────────────────────────
// CHDI Minimum Baseline Data Threshold Constants
// ─────────────────────────────────────────────────────────────

/**
 * Minimum number of entries required per signal type before computeCHDI()
 * exits the "abstain" phase and begins regular scoring.
 */
export const MIN_ENTRIES_FOR_BASELINE = 7;

/**
 * Minimum number of distinct calendar days required across the logged entries
 * per signal type before computeBaseline() and computeCHDI() activate.
 */
export const MIN_DAYS_FOR_BASELINE = 5;

// ─────────────────────────────────────────────────────────────
// Cattle Categories & Purpose
// ─────────────────────────────────────────────────────────────

export const CATTLE_PURPOSES = ["dairy", "breeding", "draft"] as const;
export type CattlePurpose = (typeof CATTLE_PURPOSES)[number];

export const AGE_GROUPS = ["calf", "adult", "senior"] as const;
export type AgeGroup = (typeof AGE_GROUPS)[number];

/**
 * Common bovine vaccines in India (Tamil Nadu animal husbandry protocol)
 */
export const COMMON_VACCINES = [
  "Foot and Mouth Disease (FMD)",
  "Brucellosis (Bruvax / S19)",
  "Anthrax Spore Vaccine",
  "Blackquarter (BQ)",
  "Hemorrhagic Septicemia (HS)",
  "Theileriosis Vaccine",
  "Rabies Post-Exposure / Prophylactic",
] as const;

/**
 * Derive ageGroup ("calf" | "adult" | "senior") from dateOfBirth or approxAge (in months or years).
 * - Calf: < 12 months (or < 1 year)
 * - Adult: 1 to 7 years (12 to 84 months)
 * - Senior: > 7 years (> 84 months)
 */
export function deriveAgeGroup(dobOrAge: Date | string | number): AgeGroup {
  let ageInMonths = 0;

  if (typeof dobOrAge === "number") {
    // Treat numbers <= 25 as years if > 0, or if given in months
    // We expect approxAge in years or months
    ageInMonths = dobOrAge <= 25 ? dobOrAge * 12 : dobOrAge;
  } else {
    const dob = new Date(dobOrAge);
    const now = new Date();
    const diffMs = now.getTime() - dob.getTime();
    ageInMonths = diffMs / (1000 * 60 * 60 * 24 * 30.4375);
  }

  if (ageInMonths < 12) return "calf";
  if (ageInMonths <= 84) return "adult";
  return "senior";
}


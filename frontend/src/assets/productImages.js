import amulMilk from "./products/amul-milk.webp";
import amulButter from "./products/amul-butter.webp";
import amulPaneer from "./products/amul-paneer.jpg";
import motherDairyCurd from "./products/mother-dairy-curd.webp";
import gheeAmul from "./products/ghee-amul.jpg";
import chitaleShrikhand from "./products/chitale-shrikhand.jpg";
import lassi from "./products/lassi.webp";
import buttermilk from "./products/buttermilk.webp";

const productImageMap = {
  "amul milk": amulMilk,
  "amul butter": amulButter,
  "amul paneer": amulPaneer,
  "mother dairy curd": motherDairyCurd,
  "ghee amul": gheeAmul,
  "chitale shrikhand": chitaleShrikhand,
  lassi,
  buttermilk,
};

const normalizeProductName = (name = "") =>
  name
    .toLowerCase()
    .replace(/[()]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

export const getProductImageByName = (name, fallbackImage) => {
  const normalizedName = normalizeProductName(name);
  return productImageMap[normalizedName] || fallbackImage;
};


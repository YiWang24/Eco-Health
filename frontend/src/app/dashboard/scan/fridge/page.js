"use client";

import { useState, useRef } from "react";
import Icon from "@/components/ui/Icon";
import DetectionBoxOverlay from "@/components/scan/DetectionBoxOverlay";
import DetectedIngredientList from "@/components/scan/DetectedIngredientList";
import FreshnessLegend from "@/components/scan/FreshnessLegend";

const TAB_SCAN = "scan";
const TAB_INVENTORY = "inventory";

const FRIDGE_INTERIOR_IMAGE =
  "https://lh3.googleusercontent.com/aida-public/AB6AXuDLgYvJbKOw6jSOoW8hpqd4W0uEfNL_sOuOnL8qfZf5wg4-FSNN3pq81nE50AnNnPaVBeAy4SUe7qlYeOd2kIeQYqtymDaZ7hlb05cSF3xXacpMZTXcR_w7WoENljvIWDkbZ5bUC3u4YFUZhBDZ5ojLYJkvAREjBpItluqiE5Ar-13GcxSQOsnTttEhvJMPBnZvu2QvOGOEol9fxXZbsLC2a07dSJWJiGbTUtDMCsDAYQFa_ZgupJPG9OioKTGp3fs1EJMmYDRmUQxr";

// 画框颜色按新鲜度：status = fresh(绿) | expiring_soon(橙) | critical(红)
const MOCK_DETECTIONS_INTERIOR = [
  { id: "1", label: "SPINACH", confidence: 98, box: { left: 18, top: 22, width: 20, height: 14 }, status: "expiring_soon" },
  { id: "2", label: "EGGS", confidence: 96, box: { left: 12, top: 52, width: 16, height: 18 }, status: "expiring_soon" },
  { id: "3", label: "CHICKEN BREAST", confidence: 94, box: { left: 35, top: 38, width: 22, height: 20 }, status: "fresh" },
  { id: "4", label: "GREEK YOGURT", confidence: 97, box: { left: 62, top: 55, width: 14, height: 16 }, status: "fresh" },
  { id: "5", label: "BLUEBERRIES", confidence: 92, box: { left: 68, top: 28, width: 18, height: 12 }, status: "fresh" },
];

const MOCK_INGREDIENTS_INTERIOR = [
  { id: "1", name: "Spinach", icon: "eco", status: "expiring_soon", statusText: "Expires in 2 days" },
  { id: "2", name: "Eggs (Large)", icon: "egg", status: "expiring_soon", statusText: "Only 2 left" },
  { id: "3", name: "Chicken Breast", icon: "restaurant", status: "fresh", statusText: "Fresh • 500g" },
  { id: "4", name: "Greek Yogurt", icon: "breakfast_dining", status: "fresh", statusText: "Full • 1kg" },
  { id: "5", name: "Blueberries", icon: "nutrition", status: "fresh", statusText: "Fresh • 250g" },
];

// 冰箱门示例检测（门架上的物品）
const MOCK_DETECTIONS_DOOR = [
  { id: "d1", label: "JUICE", confidence: 95, box: { left: 20, top: 15, width: 18, height: 22 }, status: "fresh" },
  { id: "d2", label: "MILK", confidence: 93, box: { left: 55, top: 25, width: 20, height: 28 }, status: "expiring_soon" },
];

const MOCK_INGREDIENTS_DOOR = [
  { id: "d1", name: "Juice", icon: "water_drop", status: "fresh", statusText: "Sealed • 1L" },
  { id: "d2", name: "Milk", icon: "water_drop", status: "expiring_soon", statusText: "Use within 3 days" },
];

const MOCK_FULL_INVENTORY = [
  ...MOCK_INGREDIENTS_INTERIOR,
  ...MOCK_INGREDIENTS_DOOR,
  { id: "6", name: "Cheddar Cheese", icon: "lunch_dining", status: "fresh", statusText: "Sealed • 200g" },
  { id: "7", name: "Lemons", icon: "nutrition", status: "fresh", statusText: "Fresh • 4 pcs" },
  { id: "8", name: "Butter", icon: "breakfast_dining", status: "fresh", statusText: "Fresh • 250g" },
  { id: "9", name: "Tomatoes", icon: "eco", status: "fresh", statusText: "Fresh • 3 pcs" },
];

const INITIAL_IMAGES = [
  { key: "interior", label: "Fridge interior", url: FRIDGE_INTERIOR_IMAGE, detections: MOCK_DETECTIONS_INTERIOR, ingredients: MOCK_INGREDIENTS_INTERIOR },
  { key: "door", label: "Fridge door", url: null, detections: [], ingredients: [] },
];

export default function FridgeScanPage() {
  const [activeTab, setActiveTab] = useState(TAB_SCAN);
  const [images, setImages] = useState(INITIAL_IMAGES);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const fileInputRefs = useRef({ interior: null, door: null });

  const currentSlot = images[selectedImageIndex];
  const mergedIngredients = images.flatMap((s) => s.ingredients).filter(Boolean);
  const hasAnyImage = images.some((s) => s.url);

  const handleFileChange = (slotIndex, e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setImages((prev) => {
      const next = [...prev];
      next[slotIndex] = {
        ...next[slotIndex],
        url,
        detections: slotIndex === 0 ? MOCK_DETECTIONS_INTERIOR : MOCK_DETECTIONS_DOOR,
        ingredients: slotIndex === 0 ? MOCK_INGREDIENTS_INTERIOR : MOCK_INGREDIENTS_DOOR,
      };
      return next;
    });
    e.target.value = "";
  };

  return (
    <div className="max-w-[960px] mx-auto flex flex-1 flex-col gap-8 py-8 px-4 w-full">
      <nav className="flex items-center gap-6 border-b border-primary/5 pb-2" role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === TAB_SCAN}
          onClick={() => setActiveTab(TAB_SCAN)}
          className={`pb-2 font-semibold text-sm flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === TAB_SCAN
              ? "text-primary border-primary"
              : "text-slate-500 dark:text-slate-400 border-transparent hover:text-primary"
          }`}
        >
          <Icon name="camera_alt" className="text-sm" /> Scan
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === TAB_INVENTORY}
          onClick={() => setActiveTab(TAB_INVENTORY)}
          className={`pb-2 font-semibold text-sm flex items-center gap-2 border-b-2 transition-colors ${
            activeTab === TAB_INVENTORY
              ? "text-primary border-primary"
              : "text-slate-500 dark:text-slate-400 border-transparent hover:text-primary"
          }`}
        >
          <Icon name="inventory_2" className="text-sm" /> Inventory
        </button>
      </nav>

      {activeTab === TAB_SCAN && (
        <>
          {/* Multiple images: interior / door switch and upload */}
          <div className="flex flex-wrap items-center gap-2">
            {images.map((slot, index) => (
              <div key={slot.key} className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setSelectedImageIndex(index)}
                  className={`flex items-center gap-2 rounded-xl border-2 px-4 py-2 text-sm font-semibold transition-colors ${
                    selectedImageIndex === index
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:border-primary/50"
                  }`}
                >
                  <Icon name={index === 0 ? "kitchen" : "door_front"} className="text-lg" />
                  {slot.label}
                </button>
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  ref={(el) => (fileInputRefs.current[slot.key] = el)}
                  onChange={(e) => handleFileChange(index, e)}
                />
                <button
                  type="button"
                  onClick={() => fileInputRefs.current[slot.key]?.click()}
                  className="text-xs text-primary font-medium hover:underline"
                >
                  {slot.url ? "Replace image" : "Upload image"}
                </button>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div className="lg:col-span-7 flex flex-col gap-6">
              <div className="relative group">
                <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl bg-slate-200 dark:bg-slate-800 flex items-center justify-center bg-cover bg-center shadow-2xl">
                  {currentSlot.url ? (
                    <>
                      <div
                        className="absolute inset-0 bg-cover bg-center"
                        style={{ backgroundImage: `url("${currentSlot.url}")` }}
                        aria-hidden
                      />
                      <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors" />
                      <DetectionBoxOverlay detections={currentSlot.detections || []} />
                    </>
                  ) : (
                    <div className="flex flex-col items-center justify-center gap-3 text-slate-500 dark:text-slate-400 p-6 text-center">
                      <Icon name="add_photo_alternate" className="text-4xl" />
                      <p className="text-sm font-medium">Click &quot;Upload image&quot; to take or select a photo of the {currentSlot.label.toLowerCase()}</p>
                    </div>
                  )}
                  <div className="absolute inset-0 p-6 flex flex-col justify-between pointer-events-none">
                    <div className="flex justify-between items-start">
                      <div className="bg-black/60 backdrop-blur-md text-white text-[10px] uppercase tracking-widest px-2 py-1 rounded border border-white/20 flex items-center gap-2">
                        AI Vision Active
                      </div>
                      {currentSlot.url && (
                        <span className="bg-primary/90 text-white text-[10px] font-bold px-2 py-1 rounded">
                          LIVE
                        </span>
                      )}
                    </div>
                    <div className="flex justify-center pointer-events-auto">
                      <div className="flex items-center gap-3">
                        <button
                          type="button"
                          className="p-2 rounded-full bg-white/20 text-white hover:bg-white/30 transition-colors"
                          aria-label="Mute or disable camera"
                        >
                          <Icon name="videocam_off" />
                        </button>
                        <button
                          type="button"
                          className="bg-primary text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg hover:opacity-90 transition-opacity"
                        >
                          <Icon name="camera_alt" />
                          Scan My Fridge
                        </button>
                        <button
                          type="button"
                          className="p-2 rounded-full bg-white/20 text-white hover:bg-white/30 transition-colors"
                          aria-label="Take photo"
                        >
                          <Icon name="photo_camera" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <FreshnessLegend />
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 text-center">
                  Position your camera to see all shelves for the best recognition
                  accuracy. You can upload both interior and door separately.
                </p>
              </div>
            </div>
            <div className="lg:col-span-5">
              <DetectedIngredientList
                items={mergedIngredients.length ? mergedIngredients : (currentSlot.ingredients || [])}
                newCount={mergedIngredients.length ? undefined : 0}
              />
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
            <span>Updated 2m ago</span>
            <div className="flex flex-wrap gap-3">
              <div className="px-4 py-2 rounded-xl bg-primary/15 text-primary font-bold">
                24 TOTAL ITEMS
              </div>
              <div className="px-4 py-2 rounded-xl bg-orange-500/15 text-orange-600 dark:text-orange-400 font-bold">
                3 EXPIRING SOON
              </div>
              <div className="px-4 py-2 rounded-xl bg-blue-500/15 text-blue-600 dark:text-blue-400 font-bold">
                82% HEALTH SCORE
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-primary/20 bg-primary/5 p-4 flex flex-col sm:flex-row sm:items-start gap-4">
            <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary/20 text-primary shrink-0">
              <Icon name="lightbulb" className="text-xl" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                <strong className="text-primary">Agentic Tip:</strong> I noticed your
                Spinach is expiring soon. Would you like me to suggest a recipe for a
                Spinach and Egg Scramble using your fresh chicken?
              </p>
              <button
                type="button"
                className="mt-3 bg-primary text-white px-4 py-2 rounded-xl text-sm font-bold hover:opacity-90 transition-opacity"
              >
                Generate Recipes Now
              </button>
            </div>
          </div>
        </>
      )}

      {activeTab === TAB_INVENTORY && (
        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-bold">All items</h2>
          <DetectedIngredientList items={MOCK_FULL_INVENTORY} />
          <div className="flex flex-wrap items-center gap-4 text-sm text-slate-500 dark:text-slate-400 mt-2">
            <span>Updated 2m ago</span>
            <div className="flex flex-wrap gap-3">
              <div className="px-4 py-2 rounded-xl bg-primary/15 text-primary font-bold">
                24 TOTAL ITEMS
              </div>
              <div className="px-4 py-2 rounded-xl bg-orange-500/15 text-orange-600 dark:text-orange-400 font-bold">
                3 EXPIRING SOON
              </div>
              <div className="px-4 py-2 rounded-xl bg-blue-500/15 text-blue-600 dark:text-blue-400 font-bold">
                82% HEALTH SCORE
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

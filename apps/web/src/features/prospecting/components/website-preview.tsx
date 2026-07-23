"use client";

import { useState } from "react";
import { X, Monitor, Smartphone, FileText, Briefcase, Users } from "lucide-react";

interface WebsitePreviewProps {
  screenshots: {
    homepage_desktop?: string;
    homepage_mobile?: string;
    contact?: string;
    services?: string;
    about?: string;
  };
  companyName: string;
}

export function WebsitePreview({ screenshots, companyName }: WebsitePreviewProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const screenshotItems = [
    {
      key: "homepage_desktop",
      url: screenshots.homepage_desktop,
      label: "Homepage Desktop",
      icon: Monitor,
    },
    {
      key: "homepage_mobile",
      url: screenshots.homepage_mobile,
      label: "Homepage Mobile",
      icon: Smartphone,
    },
    {
      key: "contact",
      url: screenshots.contact,
      label: "Contacto",
      icon: FileText,
    },
    {
      key: "services",
      url: screenshots.services,
      label: "Servicios",
      icon: Briefcase,
    },
    {
      key: "about",
      url: screenshots.about,
      label: "Nosotros",
      icon: Users,
    },
  ].filter((item) => item.url);

  if (screenshotItems.length === 0) {
    return null;
  }

  return (
    <>
      <div className="bg-white border border-gray-200 rounded-lg p-5">
        <div className="text-sm font-semibold text-gray-900 mb-4">
          Vista Previa del Sitio Web
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {screenshotItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.key}
                onClick={() => setSelectedImage(item.url!)}
                className="group relative aspect-[3/4] bg-gray-100 rounded-lg overflow-hidden border border-gray-200 hover:border-gray-300 transition-all hover:shadow-md"
              >
                <img
                  src={item.url}
                  alt={item.label}
                  className="w-full h-full object-cover object-top"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="absolute bottom-0 left-0 right-0 p-2 text-white opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="flex items-center gap-1.5">
                    <Icon className="w-3.5 h-3.5" />
                    <span className="text-xs font-medium">{item.label}</span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Lightbox Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <button
            onClick={() => setSelectedImage(null)}
            className="absolute top-4 right-4 p-2 bg-white/10 hover:bg-white/20 rounded-full text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
          <div className="max-w-6xl max-h-[90vh] overflow-auto">
            <img
              src={selectedImage}
              alt="Screenshot"
              className="w-full h-auto rounded-lg shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            />
          </div>
        </div>
      )}
    </>
  );
}

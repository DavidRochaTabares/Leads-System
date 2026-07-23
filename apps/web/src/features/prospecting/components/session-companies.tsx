"use client";

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card";
import { apiClient } from "@/shared/lib/api";
import { AIAnalysisCard } from "./ai-analysis-card";
import { PipelineStatus } from "./pipeline-status";

interface AIAnalysis {
  executive_summary?: string;
  website_score?: number;
  website_assessment?: string;
  business_opportunities?: string[];
  recommended_services?: Array<{
    service: string;
    why: string;
    impact: string;
    priority: string;
  }>;
  lead_score?: number;
  score_reasoning?: string;
  cold_email_subject?: string;
  cold_email_body?: string;
  linkedin_message?: string;
  whatsapp_message?: string;
  cold_call_script?: string;
  possible_objections?: Array<{
    objection: string;
    response: string;
  }>;
  next_best_action?: string;
}

interface Company {
  id: string;
  name: string;
  google_maps_url: string;
  website?: string;
  phone?: string;
  address?: string;
  rating?: number;
  review_count?: number;
  emails?: string[];
  social_links?: Record<string, string>;
  features?: Record<string, boolean>;
  recommended_services?: string[];
  ai_analysis?: AIAnalysis;
}

interface SessionCompaniesProps {
  sessionId: string | null;
  sessionStatus?: string;
}

function CompanyPipeline({ companyId }: { companyId: string }) {
  const { data: pipeline } = useQuery({
    queryKey: ["company-pipeline", companyId],
    queryFn: async (): Promise<any> => {
      try {
        const response = await apiClient.get(`/sales-pipeline/companies/${companyId}/active-pipeline`);
        return response;
      } catch (error) {
        return null;
      }
    },
    enabled: !!companyId,
  });

  return <PipelineStatus pipeline={pipeline || null} />;
}

export function SessionCompanies({ sessionId, sessionStatus }: SessionCompaniesProps) {
  const { data: companies, isLoading, refetch } = useQuery<Company[]>({
    queryKey: ["session-companies", sessionId],
    queryFn: async (): Promise<Company[]> => {
      if (!sessionId) return [];
      const response = await apiClient.get(`/prospecting/sessions/${sessionId}/companies`);
      return response as Company[];
    },
    enabled: !!sessionId,
    // Refetch while session is running OR analyzing (increased interval for Windows stability)
    refetchInterval: (sessionStatus === 'pending' || sessionStatus === 'running' || sessionStatus === 'analyzing') ? 5000 : false,
    // Refetch on window focus if completed (to get latest AI analysis)
    refetchOnWindowFocus: sessionStatus === 'completed',
    retry: 1, // Reduce retries to avoid socket saturation
  });

  // Refetch when status changes to completed (with small delay to ensure AI data is saved)
  useEffect(() => {
    if (sessionStatus === 'completed') {
      setTimeout(() => {
        refetch();
      }, 2000);
    }
  }, [sessionStatus, refetch]);

  if (!sessionId) return null;
  if (isLoading) return <div>Loading companies...</div>;
  if (!companies || companies.length === 0) return <div>No companies found yet.</div>;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Companies Found ({companies.length})</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {companies.map((company) => (
            <div key={company.id} className="border rounded-lg p-4">
              <h3 className="font-semibold text-lg">{company.name}</h3>
              
              {company.rating && (
                <div className="text-sm text-gray-600">
                  ⭐ {company.rating} ({company.review_count} reviews)
                </div>
              )}
              
              {company.address && (
                <div className="text-sm text-gray-600 mt-1">📍 {company.address}</div>
              )}
              
              {company.phone && (
                <div className="text-sm text-gray-600 mt-1">📞 {company.phone}</div>
              )}
              
              <div className="flex gap-2 mt-2">
                {company.website && (
                  <a
                    href={company.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:underline"
                  >
                    Website
                  </a>
                )}
                <a
                  href={company.google_maps_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:underline"
                >
                  Google Maps
                </a>
              </div>

              {/* Website Enrichment Data */}
              {company.emails && company.emails.length > 0 && (
                <div className="mt-3 pt-3 border-t">
                  <div className="text-sm font-medium mb-1">📧 Emails:</div>
                  <div className="flex flex-wrap gap-2">
                    {company.emails.map((email: string, idx: number) => (
                      <a key={idx} href={`mailto:${email}`} className="text-xs bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700 font-medium">
                        {email}
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {company.social_links && Object.keys(company.social_links).length > 0 && (
                <div className="mt-2">
                  <div className="text-sm font-medium mb-1">🌐 Social Media:</div>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(company.social_links).map(([platform, url]: [string, any]) => (
                      <a
                        key={platform}
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs bg-purple-600 text-white px-3 py-1.5 rounded hover:bg-purple-700 capitalize font-medium"
                      >
                        {platform}
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {company.features && Object.values(company.features).some((v: any) => v === true) && (
                <div className="mt-2">
                  <div className="text-sm font-medium mb-1">✅ Features:</div>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(company.features)
                      .filter(([_, value]: [string, any]) => value === true)
                      .map(([feature]: [string, any]) => (
                        <span key={feature} className="text-xs bg-green-600 text-white px-3 py-1.5 rounded font-medium">
                          {feature.replace('has_', '').replace('_', ' ')}
                        </span>
                      ))}
                  </div>
                </div>
              )}

              {company.recommended_services && company.recommended_services.length > 0 && (
                <div className="mt-2">
                  <div className="text-sm font-medium mb-1">💡 Recommended Services:</div>
                  <div className="flex flex-wrap gap-2">
                    {company.recommended_services.map((service: string, idx: number) => (
                      <span key={idx} className="text-xs bg-amber-600 text-white px-3 py-1.5 rounded font-medium">
                        {service}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* AI Commercial Assessment */}
              {company.ai_analysis && (
                <AIAnalysisCard analysis={company.ai_analysis} companyName={company.name} />
              )}

              {/* Sales Pipeline */}
              <CompanyPipeline companyId={company.id} />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

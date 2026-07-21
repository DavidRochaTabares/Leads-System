"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card";
import { apiClient } from "@/shared/lib/api";

interface AIAnalysis {
  summary?: string;
  website_assessment?: string;
  branding_assessment?: string;
  pain_points?: string[];
  business_opportunities?: string[];
  recommended_services?: Array<{service: string; justification: string}>;
  lead_score?: number;
  score_reason?: string;
  sales_strategy?: string;
  personalized_email?: string;
  linkedin_message?: string;
  whatsapp_message?: string;
  cold_call_script?: string;
  possible_objections?: string[];
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

export function SessionCompanies({ sessionId, sessionStatus }: SessionCompaniesProps) {
  const { data: companies, isLoading } = useQuery<Company[]>({
    queryKey: ["session-companies", sessionId],
    queryFn: async (): Promise<Company[]> => {
      if (!sessionId) return [];
      const response = await apiClient.get(`/prospecting/sessions/${sessionId}/companies`);
      return response as Company[];
    },
    enabled: !!sessionId,
    refetchInterval: sessionStatus === 'pending' || sessionStatus === 'running' ? 5000 : false,
  });

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
                      <a key={idx} href={`mailto:${email}`} className="text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200">
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
                        className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200 capitalize"
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
                        <span key={feature} className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
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
                      <span key={idx} className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                        {service}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* AI Analysis Section */}
              {company.ai_analysis && (
                <div className="mt-4 pt-4 border-t-2 border-purple-200">
                  <div className="text-lg font-bold mb-3 text-purple-700">🤖 AI Analysis</div>
                  
                  {/* Lead Score */}
                  {company.ai_analysis.lead_score !== undefined && (
                    <div className="mb-3 p-3 bg-purple-50 rounded">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold">Lead Score:</span>
                        <span className="text-2xl font-bold text-purple-700">{company.ai_analysis.lead_score}/100</span>
                      </div>
                      {company.ai_analysis.score_reason && (
                        <p className="text-sm text-gray-600 mt-1">{company.ai_analysis.score_reason}</p>
                      )}
                    </div>
                  )}

                  {/* Summary */}
                  {company.ai_analysis.summary && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">📋 Summary:</div>
                      <p className="text-sm text-gray-700">{company.ai_analysis.summary}</p>
                    </div>
                  )}

                  {/* Website Assessment */}
                  {company.ai_analysis.website_assessment && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">🌐 Website Assessment:</div>
                      <p className="text-sm text-gray-700">{company.ai_analysis.website_assessment}</p>
                    </div>
                  )}

                  {/* Branding Assessment */}
                  {company.ai_analysis.branding_assessment && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">🎨 Branding Assessment:</div>
                      <p className="text-sm text-gray-700">{company.ai_analysis.branding_assessment}</p>
                    </div>
                  )}

                  {/* Pain Points */}
                  {company.ai_analysis.pain_points && company.ai_analysis.pain_points.length > 0 && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">⚠️ Pain Points:</div>
                      <ul className="list-disc list-inside text-sm text-gray-700">
                        {company.ai_analysis.pain_points.map((point, idx) => (
                          <li key={idx}>{point}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Business Opportunities */}
                  {company.ai_analysis.business_opportunities && company.ai_analysis.business_opportunities.length > 0 && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">💼 Business Opportunities:</div>
                      <ul className="list-disc list-inside text-sm text-gray-700">
                        {company.ai_analysis.business_opportunities.map((opp, idx) => (
                          <li key={idx}>{opp}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* AI Recommended Services */}
                  {company.ai_analysis.recommended_services && company.ai_analysis.recommended_services.length > 0 && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">🎯 AI Recommended Services:</div>
                      <div className="space-y-2">
                        {company.ai_analysis.recommended_services.map((rec, idx) => (
                          <div key={idx} className="bg-blue-50 p-2 rounded">
                            <div className="font-medium text-sm text-blue-900">{rec.service}</div>
                            <div className="text-xs text-gray-600">{rec.justification}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Sales Strategy */}
                  {company.ai_analysis.sales_strategy && (
                    <div className="mb-3">
                      <div className="font-semibold text-sm mb-1">📈 Sales Strategy:</div>
                      <p className="text-sm text-gray-700 whitespace-pre-wrap">{company.ai_analysis.sales_strategy}</p>
                    </div>
                  )}

                  {/* Next Best Action */}
                  {company.ai_analysis.next_best_action && (
                    <div className="mb-3 p-3 bg-green-50 rounded border border-green-200">
                      <div className="font-semibold text-sm mb-1 text-green-800">✅ Next Best Action:</div>
                      <p className="text-sm text-green-900 font-medium">{company.ai_analysis.next_best_action}</p>
                    </div>
                  )}

                  {/* Outreach Content - Collapsible */}
                  <details className="mb-2">
                    <summary className="cursor-pointer font-semibold text-sm mb-1 hover:text-purple-700">📧 Personalized Email</summary>
                    <div className="mt-2 p-3 bg-gray-50 rounded text-sm whitespace-pre-wrap">{company.ai_analysis.personalized_email}</div>
                  </details>

                  <details className="mb-2">
                    <summary className="cursor-pointer font-semibold text-sm mb-1 hover:text-purple-700">💼 LinkedIn Message</summary>
                    <div className="mt-2 p-3 bg-gray-50 rounded text-sm whitespace-pre-wrap">{company.ai_analysis.linkedin_message}</div>
                  </details>

                  <details className="mb-2">
                    <summary className="cursor-pointer font-semibold text-sm mb-1 hover:text-purple-700">💬 WhatsApp Message</summary>
                    <div className="mt-2 p-3 bg-gray-50 rounded text-sm whitespace-pre-wrap">{company.ai_analysis.whatsapp_message}</div>
                  </details>

                  <details className="mb-2">
                    <summary className="cursor-pointer font-semibold text-sm mb-1 hover:text-purple-700">📞 Cold Call Script</summary>
                    <div className="mt-2 p-3 bg-gray-50 rounded text-sm whitespace-pre-wrap">{company.ai_analysis.cold_call_script}</div>
                  </details>

                  {/* Possible Objections */}
                  {company.ai_analysis.possible_objections && company.ai_analysis.possible_objections.length > 0 && (
                    <details className="mb-2">
                      <summary className="cursor-pointer font-semibold text-sm mb-1 hover:text-purple-700">🛡️ Possible Objections</summary>
                      <ul className="mt-2 list-disc list-inside text-sm text-gray-700">
                        {company.ai_analysis.possible_objections.map((obj, idx) => (
                          <li key={idx}>{obj}</li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

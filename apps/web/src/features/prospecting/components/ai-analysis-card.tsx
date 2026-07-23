"use client";

import { useState } from "react";
import { 
  Copy, 
  Check, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle2, 
  XCircle,
  Mail,
  Linkedin,
  MessageCircle,
  Phone,
  Shield,
  ChevronDown,
  ChevronUp
} from "lucide-react";

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

interface AIAnalysisCardProps {
  analysis: AIAnalysis;
  companyName: string;
}

export function AIAnalysisCard({ analysis, companyName }: AIAnalysisCardProps) {
  const [copiedField, setCopiedField] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});

  // Debug: Log analysis to console
  console.log('[AIAnalysisCard] Analysis data:', analysis);

  const copyToClipboard = async (text: string, field: string) => {
    await navigator.clipboard.writeText(text);
    setCopiedField(field);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const getLeadStatus = (score: number) => {
    if (score >= 80) return { 
      text: "Excelente Prospecto", 
      color: "text-green-700 bg-green-50 border-green-200",
      icon: TrendingUp,
      iconColor: "text-green-600"
    };
    if (score >= 65) return { 
      text: "Buen Prospecto", 
      color: "text-blue-700 bg-blue-50 border-blue-200",
      icon: CheckCircle2,
      iconColor: "text-blue-600"
    };
    if (score >= 50) return { 
      text: "Oportunidad Media", 
      color: "text-yellow-700 bg-yellow-50 border-yellow-200",
      icon: AlertCircle,
      iconColor: "text-yellow-600"
    };
    return { 
      text: "Baja Prioridad", 
      color: "text-gray-700 bg-gray-50 border-gray-200",
      icon: XCircle,
      iconColor: "text-gray-600"
    };
  };

  const getPriorityBadge = (priority: string) => {
    if (priority === "Alta") return "bg-red-100 text-red-700 border-red-200";
    if (priority === "Media") return "bg-yellow-100 text-yellow-700 border-yellow-200";
    return "bg-gray-100 text-gray-600 border-gray-200";
  };

  const CopyButton = ({ text, field }: { text: string; field: string }) => (
    <button
      onClick={() => copyToClipboard(text, field)}
      className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-600 bg-white border border-gray-200 rounded-md hover:bg-gray-50 hover:border-gray-300 transition-all"
    >
      {copiedField === field ? (
        <>
          <Check className="w-3.5 h-3.5" />
          Copiado
        </>
      ) : (
        <>
          <Copy className="w-3.5 h-3.5" />
          Copiar
        </>
      )}
    </button>
  );

  // Show analysis even if lead_score is missing
  const leadStatus = analysis.lead_score ? getLeadStatus(analysis.lead_score) : {
    text: "Sin Evaluar",
    color: "bg-gray-100 border-gray-300 text-gray-700",
    icon: AlertCircle,
    iconColor: "text-gray-500"
  };
  const StatusIcon = leadStatus.icon;

  return (
    <div className="mt-8 space-y-6">
      {/* LEVEL 1: Executive Dashboard - Always Visible */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        {/* Lead Score */}
        {analysis.lead_score !== undefined && (
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <div className="text-sm font-medium text-gray-500 mb-1">Puntuación de Lead</div>
              <div className="flex items-baseline gap-3">
                <div className="text-5xl font-bold text-gray-900">{analysis.lead_score}</div>
                <div className="text-lg text-gray-400">/100</div>
              </div>
            </div>
            <div className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${leadStatus.color}`}>
              <StatusIcon className={`w-5 h-5 ${leadStatus.iconColor}`} />
              <span className="font-semibold text-sm">{leadStatus.text}</span>
            </div>
          </div>
        )}

        {/* Key Findings Grid */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          {analysis.business_opportunities?.slice(0, 6).map((opp, idx) => {
            const isPositive = opp.toLowerCase().includes('tiene') || opp.toLowerCase().includes('detectó');
            return (
              <div key={idx} className="flex items-start gap-2">
                {isPositive ? (
                  <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                )}
                <span className="text-sm text-gray-700 leading-tight">{opp}</span>
              </div>
            );
          })}
        </div>

        {/* Top 3 Services */}
        {analysis.recommended_services && analysis.recommended_services.length > 0 && (
          <div className="mb-6">
            <div className="text-sm font-semibold text-gray-900 mb-3">Servicios Recomendados</div>
            <div className="space-y-2">
              {analysis.recommended_services.slice(0, 3).map((service, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-100">
                  <div className="flex-1">
                    <div className="font-medium text-sm text-gray-900">{service.service}</div>
                    <div className="text-xs text-gray-600 mt-0.5">{service.why}</div>
                  </div>
                  <span className={`ml-3 px-2 py-1 rounded text-xs font-semibold border ${getPriorityBadge(service.priority)}`}>
                    {service.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Next Best Action */}
        {analysis.next_best_action && (
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start gap-3">
              <TrendingUp className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <div className="text-sm font-semibold text-blue-900 mb-1">Siguiente Acción</div>
                <div className="text-sm text-blue-800">{analysis.next_best_action}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* LEVEL 2: Compact Information Cards */}
      <div className="grid gap-4">
        {/* Executive Summary */}
        {analysis.executive_summary && (
          <div className="bg-white border border-gray-200 rounded-lg p-5">
            <div className="text-sm font-semibold text-gray-900 mb-2">Resumen Ejecutivo</div>
            <div className="text-sm text-gray-600 leading-relaxed line-clamp-5">
              {analysis.executive_summary}
            </div>
          </div>
        )}

        {/* Website Assessment */}
        {analysis.website_assessment && (
          <div className="bg-white border border-gray-200 rounded-lg p-5">
            <div className="flex items-center justify-between mb-3">
              <div className="text-sm font-semibold text-gray-900">Evaluación del Sitio Web</div>
              {analysis.website_score !== undefined && (
                <div className="text-2xl font-bold text-gray-900">{analysis.website_score}<span className="text-sm text-gray-400">/100</span></div>
              )}
            </div>
            <div className="text-sm text-gray-600 leading-relaxed line-clamp-3">
              {analysis.website_assessment}
            </div>
          </div>
        )}

        {/* Business Opportunities */}
        {analysis.business_opportunities && analysis.business_opportunities.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-lg p-5">
            <div className="text-sm font-semibold text-gray-900 mb-3">Oportunidades de Negocio</div>
            <div className="space-y-2">
              {analysis.business_opportunities.slice(0, 5).map((opp, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <div className="w-1 h-1 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-sm text-gray-600 leading-tight">{opp}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* LEVEL 3: Sales Content - Collapsible */}
      <div className="space-y-2">
        {/* Cold Email */}
        {analysis.cold_email_subject && analysis.cold_email_body && (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection('email')}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Mail className="w-4 h-4 text-gray-400" />
                <span className="text-sm font-medium text-gray-900">Correo Personalizado</span>
              </div>
              {expandedSections['email'] ? (
                <ChevronUp className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              )}
            </button>
            {expandedSections['email'] && (
              <div className="px-4 pb-4 border-t border-gray-100">
                <div className="flex justify-end mb-3 pt-3">
                  <CopyButton text={`${analysis.cold_email_subject}\n\n${analysis.cold_email_body}`} field="email" />
                </div>
                <div className="mb-3">
                  <div className="text-xs font-medium text-gray-500 mb-1">Asunto</div>
                  <div className="text-sm font-medium text-gray-900">{analysis.cold_email_subject}</div>
                </div>
                <div className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                  {analysis.cold_email_body}
                </div>
              </div>
            )}
          </div>
        )}

        {/* LinkedIn Message */}
        {analysis.linkedin_message && (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection('linkedin')}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Linkedin className="w-4 h-4 text-gray-400" />
                <span className="text-sm font-medium text-gray-900">Mensaje de LinkedIn</span>
              </div>
              {expandedSections['linkedin'] ? (
                <ChevronUp className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              )}
            </button>
            {expandedSections['linkedin'] && (
              <div className="px-4 pb-4 border-t border-gray-100">
                <div className="flex justify-end mb-3 pt-3">
                  <CopyButton text={analysis.linkedin_message} field="linkedin" />
                </div>
                <div className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                  {analysis.linkedin_message}
                </div>
              </div>
            )}
          </div>
        )}

        {/* WhatsApp Message */}
        {analysis.whatsapp_message && (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection('whatsapp')}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <MessageCircle className="w-4 h-4 text-gray-400" />
                <span className="text-sm font-medium text-gray-900">Mensaje de WhatsApp</span>
              </div>
              {expandedSections['whatsapp'] ? (
                <ChevronUp className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              )}
            </button>
            {expandedSections['whatsapp'] && (
              <div className="px-4 pb-4 border-t border-gray-100">
                <div className="flex justify-end mb-3 pt-3">
                  <CopyButton text={analysis.whatsapp_message} field="whatsapp" />
                </div>
                <div className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                  {analysis.whatsapp_message}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Cold Call Script */}
        {analysis.cold_call_script && (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection('call')}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Phone className="w-4 h-4 text-gray-400" />
                <span className="text-sm font-medium text-gray-900">Guion de Llamada</span>
              </div>
              {expandedSections['call'] ? (
                <ChevronUp className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              )}
            </button>
            {expandedSections['call'] && (
              <div className="px-4 pb-4 border-t border-gray-100">
                <div className="flex justify-end mb-3 pt-3">
                  <CopyButton text={analysis.cold_call_script} field="call" />
                </div>
                <div className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                  {analysis.cold_call_script}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Objections */}
        {analysis.possible_objections && analysis.possible_objections.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection('objections')}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Shield className="w-4 h-4 text-gray-400" />
                <span className="text-sm font-medium text-gray-900">Posibles Objeciones</span>
              </div>
              {expandedSections['objections'] ? (
                <ChevronUp className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              )}
            </button>
            {expandedSections['objections'] && (
              <div className="px-4 pb-4 border-t border-gray-100 pt-3">
                <div className="space-y-3">
                  {analysis.possible_objections.map((obj, idx) => (
                    <div key={idx} className="space-y-2">
                      <div className="flex items-start gap-2">
                        <XCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                        <div className="text-sm font-medium text-gray-900">{obj.objection}</div>
                      </div>
                      <div className="flex items-start gap-2 ml-6">
                        <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                        <div className="text-sm text-gray-600">{obj.response}</div>
                      </div>
                      {idx < (analysis.possible_objections?.length ?? 0) - 1 && (
                        <div className="border-t border-gray-100 mt-3"></div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Debug: Show if analysis exists but nothing is displayed */}
      {!analysis.lead_score && !analysis.executive_summary && !analysis.business_opportunities?.length && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="text-sm font-medium text-yellow-900 mb-2">⚠️ Análisis recibido pero sin datos estructurados</div>
          <div className="text-xs text-yellow-700">
            <pre className="whitespace-pre-wrap overflow-auto max-h-40">
              {JSON.stringify(analysis, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

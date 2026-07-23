"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card";
import { Badge } from "@/shared/components/ui/badge";

interface CommercialOpportunity {
  description: string;
}

interface BusinessStrength {
  strength: string;
  opportunity: string;
}

interface SalesBrief {
  primary_service?: string;
  secondary_service?: string;
  estimated_opportunity?: string;
  why_this_service?: string[];
  why_this_company?: string[];
  lead_with?: string;
  main_business_benefit?: string;
  communication_style?: string;
  decision_maker?: string;
  commercial_opportunities?: CommercialOpportunity[];
  business_strengths?: BusinessStrength[];
  estimated_success_probability?: number;
}

interface SalesPipeline {
  id: string;
  company_id: string;
  status: string;
  current_stage: string;
  strategy?: SalesBrief;
  strategy_status: string;
  next_action?: string;
  next_action_date?: string;
  last_activity?: string;
  created_at: string;
}

interface PipelineStatusProps {
  pipeline: SalesPipeline | null;
}

async function regenerateStrategy(pipelineId: string) {
  const button = document.querySelector('[data-regenerate]') as HTMLButtonElement;
  if (button) {
    button.disabled = true;
    button.textContent = 'Regenerating...';
  }
  
  try {
    console.log('[REGENERATE] Starting strategy regeneration for pipeline:', pipelineId);
    const response = await fetch(`http://localhost:8000/sales-pipeline/pipelines/${pipelineId}/generate-strategy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    console.log('[REGENERATE] Response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('[REGENERATE] Strategy regenerated successfully:', data);
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      const error = await response.text();
      console.error('[REGENERATE] Failed:', error);
      alert('Failed to regenerate strategy. Check console for details.');
      if (button) {
        button.disabled = false;
        button.textContent = 'Regenerate';
      }
    }
  } catch (error) {
    console.error('[REGENERATE] Error:', error);
    alert('Error regenerating strategy. Check console for details.');
    if (button) {
      button.disabled = false;
      button.textContent = 'Regenerate';
    }
  }
}

function OpportunityBadge({ level }: { level: string }) {
  const variants: Record<string, string> = {
    High: 'bg-green-500/20 text-green-600 border-green-500/30',
    Medium: 'bg-yellow-500/20 text-yellow-600 border-yellow-500/30',
    Low: 'bg-blue-500/20 text-blue-600 border-blue-500/30',
  };

  return (
    <Badge variant="outline" className={`${variants[level] || variants.Medium} font-semibold`}>
      {level} Opportunity
    </Badge>
  );
}

function SuccessProbability({ probability }: { probability: number }) {
  const stars = Math.round((probability / 100) * 5);
  const fullStars = '★'.repeat(stars);
  const emptyStars = '☆'.repeat(5 - stars);

  const colorClass = 
    probability >= 75 ? 'text-green-500' :
    probability >= 50 ? 'text-yellow-500' :
    'text-orange-500';

  return (
    <div className="flex items-center gap-3">
      <span className={`text-3xl font-bold ${colorClass}`}>{probability}%</span>
      <span className={`text-2xl ${colorClass}`}>{fullStars}{emptyStars}</span>
    </div>
  );
}

export function PipelineStatus({ pipeline }: PipelineStatusProps) {
  if (!pipeline) {
    return null;
  }

  const brief = pipeline.strategy;

  if (!brief) {
    return null;
  }

  return (
    <div className="space-y-4 mt-6">
      {/* Next Step - Prominent */}
      <Card className="border-yellow-500 bg-yellow-500/5">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Next Step</p>
              <p className="text-xl font-bold">Generate WhatsApp Message</p>
            </div>
            <Badge className="bg-yellow-500 text-white hover:bg-yellow-600">
              Action Required
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Sales Brief - Cheat Sheet */}
      <Card className="border-blue-500/30">
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3">
                <CardTitle className="text-xl">Sales Brief</CardTitle>
                <button
                  data-regenerate
                  onClick={() => regenerateStrategy(pipeline.id)}
                  className="text-xs bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Regenerate
                </button>
              </div>
              <p className="text-sm text-muted-foreground mt-1">
                Everything you need to know before messaging this company
              </p>
            </div>
            {brief.estimated_success_probability !== undefined && (
              <SuccessProbability probability={brief.estimated_success_probability} />
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* 1. WHAT WE SHOULD SELL */}
          <div className="space-y-3">
            <h3 className="font-semibold text-base uppercase text-muted-foreground tracking-wide">
              What We Should Sell
            </h3>
            <div className="space-y-3">
              {brief.primary_service && (
                <div className="flex items-center gap-2">
                  <Badge className="bg-blue-600 text-white">Primary</Badge>
                  <span className="font-semibold text-lg">{brief.primary_service}</span>
                </div>
              )}
              {brief.secondary_service && (
                <div className="flex items-center gap-2">
                  <Badge variant="outline">Secondary</Badge>
                  <span className="text-sm">{brief.secondary_service}</span>
                </div>
              )}
              {brief.estimated_opportunity && (
                <div className="mt-2">
                  <OpportunityBadge level={brief.estimated_opportunity} />
                </div>
              )}
              
              {/* WHY THIS SERVICE */}
              {brief.why_this_service && brief.why_this_service.length > 0 && (
                <div className="mt-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg p-3">
                  <p className="text-xs font-semibold text-blue-600 dark:text-blue-400 mb-2 uppercase tracking-wide">
                    Why This Service?
                  </p>
                  <ul className="space-y-1.5">
                    {brief.why_this_service.map((reason, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-blue-500 mt-0.5">•</span>
                        <span>{reason}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* 2. WHY THIS COMPANY */}
          {brief.why_this_company && brief.why_this_company.length > 0 && (
            <div className="space-y-3 border-t pt-4">
              <h3 className="font-semibold text-base uppercase text-muted-foreground tracking-wide">
                Why This Company
              </h3>
              <ul className="space-y-2">
                {brief.why_this_company.map((reason, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-green-500 text-lg mt-0.5 font-bold">•</span>
                    <span className="font-medium">{reason}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 3. HOW TO SELL */}
          <div className="space-y-4 border-t pt-4">
            <h3 className="font-semibold text-base uppercase text-muted-foreground tracking-wide">
              How To Sell
            </h3>
            
            {brief.lead_with && (
              <div className="bg-green-50 dark:bg-green-950/20 rounded-lg p-4">
                <p className="text-xs font-semibold text-green-600 dark:text-green-400 mb-2 uppercase tracking-wide">
                  Lead With
                </p>
                <p className="font-semibold text-base">{brief.lead_with}</p>
              </div>
            )}
            
            {brief.main_business_benefit && (
              <div className="bg-purple-50 dark:bg-purple-950/20 rounded-lg p-4">
                <p className="text-xs font-semibold text-purple-600 dark:text-purple-400 mb-2 uppercase tracking-wide">
                  Main Business Benefit
                </p>
                <p className="font-semibold text-base">{brief.main_business_benefit}</p>
              </div>
            )}
            
            <div className="grid gap-3">
              {brief.communication_style && (
                <div>
                  <p className="text-xs text-muted-foreground mb-2 font-semibold uppercase tracking-wide">
                    Communication Style
                  </p>
                  <p className="text-sm bg-muted/50 rounded p-3">{brief.communication_style}</p>
                </div>
              )}
              
              {brief.decision_maker && (
                <div>
                  <p className="text-xs text-muted-foreground mb-2 font-semibold uppercase tracking-wide">
                    Decision Maker
                  </p>
                  <p className="text-sm font-medium">{brief.decision_maker}</p>
                </div>
              )}
            </div>
          </div>

          {/* COMMERCIAL OPPORTUNITIES */}
          {brief.commercial_opportunities && brief.commercial_opportunities.length > 0 && (
            <div className="space-y-3 border-t pt-4">
              <h3 className="font-semibold text-base uppercase text-muted-foreground tracking-wide">
                Commercial Opportunities
              </h3>
              <ul className="space-y-2">
                {brief.commercial_opportunities.map((opp, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-blue-500 text-lg mt-0.5">→</span>
                    <span className="text-sm">{opp.description}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* BUSINESS STRENGTHS */}
          {brief.business_strengths && brief.business_strengths.length > 0 && (
            <div className="space-y-3 border-t pt-4">
              <h3 className="font-semibold text-base uppercase text-muted-foreground tracking-wide">
                Business Strengths
              </h3>
              <div className="space-y-3">
                {brief.business_strengths.map((item, idx) => {
                  const strength = typeof item === 'string' ? item : item.strength;
                  const opportunity = typeof item === 'object' && item.opportunity ? item.opportunity : null;
                  
                  return (
                    <div key={idx} className="bg-muted/50 rounded-lg p-3">
                      <p className="font-medium text-sm mb-1">✓ {strength}</p>
                      {opportunity && (
                        <p className="text-xs text-muted-foreground">→ {opportunity}</p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

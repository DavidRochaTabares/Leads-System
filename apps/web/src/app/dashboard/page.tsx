import { DashboardLayout } from '@/features/dashboard/components/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Rocket, Wrench, Zap } from 'lucide-react';

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="space-y-2">
          <h2 className="text-4xl font-bold tracking-tight">Welcome to SpineDev Platform</h2>
          <p className="text-lg text-muted-foreground">
            Your internal operating system for growth and efficiency
          </p>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card className="border-primary/20 hover:border-primary/40 transition-colors">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Rocket className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <CardTitle>Platform Ready</CardTitle>
                  <CardDescription>Foundation is set</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Clean Architecture with FastAPI backend and Next.js 15 frontend, ready for scaling.
              </p>
            </CardContent>
          </Card>
          
          <Card className="border-secondary/20 hover:border-secondary/40 transition-colors">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-secondary/10">
                  <Wrench className="h-6 w-6 text-secondary" />
                </div>
                <div>
                  <CardTitle>Build Tools</CardTitle>
                  <CardDescription>Start creating</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Prospecting Engine, Proposal Generator, SEO Auditor - build what you need.
              </p>
            </CardContent>
          </Card>
          
          <Card className="border-accent/20 hover:border-accent/40 transition-colors">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-accent/10">
                  <Zap className="h-6 w-6 text-accent" />
                </div>
                <div>
                  <CardTitle>AI Powered</CardTitle>
                  <CardDescription>Claude & Gemini ready</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Integrated with Anthropic Claude and Google Gemini for intelligent automation.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}

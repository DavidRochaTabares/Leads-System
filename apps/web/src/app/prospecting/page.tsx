import { DashboardLayout } from '@/features/dashboard/components/dashboard-layout';
import { ProspectingContent } from '@/features/prospecting/components/prospecting-content';

export default function ProspectingPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="space-y-2">
          <h2 className="text-4xl font-bold tracking-tight">Prospecting Engine</h2>
          <p className="text-lg text-muted-foreground">
            Discover companies with automated mining sessions.
          </p>
        </div>

        <ProspectingContent />
      </div>
    </DashboardLayout>
  );
}

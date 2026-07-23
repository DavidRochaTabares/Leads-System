import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { ProspectingSession } from '../types';

interface SessionStatusProps {
  session: ProspectingSession | null;
}

function formatDate(value: string | null): string {
  if (!value) return '-';
  return new Date(value).toLocaleString();
}

function StatusBadge({ status }: { status: string }) {
  const variants: Record<string, string> = {
    pending: 'bg-muted text-muted-foreground',
    running: 'bg-secondary text-secondary-foreground animate-pulse',
    analyzing: 'bg-blue-500/20 text-blue-500 animate-pulse',
    completed: 'bg-green-500/20 text-green-500',
    failed: 'bg-destructive/20 text-destructive',
  };

  const labels: Record<string, string> = {
    pending: 'Pending',
    running: 'Mining',
    analyzing: 'Analyzing',
    completed: 'Completed',
    failed: 'Failed',
  };

  return (
    <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${variants[status] || variants.pending}`}>
      {labels[status] || status}
    </span>
  );
}

export function SessionStatus({ session }: SessionStatusProps) {
  if (!session) {
    return (
      <Card className="border-muted">
        <CardHeader>
          <CardTitle>Current Session Status</CardTitle>
          <CardDescription>No session has been created yet.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="border-muted">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Current Session Status</CardTitle>
            <CardDescription>
              {session.industry} in {session.location}
            </CardDescription>
          </div>
          <StatusBadge status={session.status} />
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Progress</span>
            <span className="font-medium">{session.progress}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
            <div
              className="h-full bg-secondary transition-all duration-500"
              style={{ width: `${session.progress}%` }}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-muted-foreground">Created At</p>
            <p className="font-medium">{formatDate(session.created_at)}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Started At</p>
            <p className="font-medium">{formatDate(session.started_at)}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Finished At</p>
            <p className="font-medium">{formatDate(session.finished_at)}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Max Companies</p>
            <p className="font-medium">{session.max_companies}</p>
          </div>
        </div>

        {session.error_message && (
          <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
            {session.error_message}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

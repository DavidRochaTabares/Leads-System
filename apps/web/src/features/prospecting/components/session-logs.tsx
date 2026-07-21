import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { ProspectingSessionLog } from '../types';

interface SessionLogsProps {
  logs: ProspectingSessionLog[];
}

function LogLevelDot({ level }: { level: string }) {
  const colors: Record<string, string> = {
    info: 'bg-primary',
    error: 'bg-destructive',
    warn: 'bg-secondary',
  };

  return (
    <span className={`h-2 w-2 rounded-full ${colors[level] || colors.info}`} />
  );
}

export function SessionLogs({ logs }: SessionLogsProps) {
  return (
    <Card className="border-muted">
      <CardHeader>
        <CardTitle>Live Logs</CardTitle>
        <CardDescription>Real-time worker output</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-64 overflow-y-auto rounded-md bg-muted/50 p-4 space-y-2">
          {logs.length === 0 ? (
            <p className="text-sm text-muted-foreground">No logs yet.</p>
          ) : (
            logs.map((log) => (
              <div key={log.id} className="flex items-start gap-3 text-sm">
                <LogLevelDot level={log.level} />
                <span className="text-muted-foreground whitespace-nowrap">
                  {new Date(log.created_at).toLocaleTimeString()}
                </span>
                <span>{log.message}</span>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}

'use client';

import { ProspectingForm } from './prospecting-form';
import { SessionStatus } from './session-status';
import { SessionLogs } from './session-logs';
import { SessionCompanies } from './session-companies';
import { useProspectingSession, useProspectingSessionLogs } from '../hooks/use-prospecting';

export function ProspectingContent() {
  const { data: session, isLoading } = useProspectingSession();
  const { data: logs = [] } = useProspectingSessionLogs(session?.id, session?.status);

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-6">
          <ProspectingForm />
          {isLoading && !session ? (
            <p className="text-sm text-muted-foreground">Loading session...</p>
          ) : (
            <SessionStatus session={session ?? null} />
          )}
        </div>
        <div>
          <SessionLogs logs={logs} />
        </div>
      </div>
      {session && <SessionCompanies sessionId={session.id} sessionStatus={session.status} />}
    </div>
  );
}

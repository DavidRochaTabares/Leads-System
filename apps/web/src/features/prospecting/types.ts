export interface ProspectingSessionLog {
  id: string;
  level: string;
  message: string;
  created_at: string;
}

export interface ProspectingSession {
  id: string;
  industry: string;
  location: string;
  max_companies: number;
  status: 'pending' | 'running' | 'analyzing' | 'completed' | 'failed';
  progress: number;
  error_message: string | null;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  logs: ProspectingSessionLog[];
}

export interface ProspectingSessionCreatePayload {
  industry: string;
  location: string;
  max_companies: number;
}

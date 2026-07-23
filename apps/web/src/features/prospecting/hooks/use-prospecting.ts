import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/shared/lib/api';
import {
  ProspectingSession,
  ProspectingSessionCreatePayload,
  ProspectingSessionLog,
} from '../types';

const POLLING_INTERVAL = 3000; // Increased for Windows stability

async function createSession(payload: ProspectingSessionCreatePayload): Promise<ProspectingSession> {
  return apiClient.post<ProspectingSession>('/prospecting/sessions', payload);
}

async function fetchLatestSession(): Promise<ProspectingSession | null> {
  try {
    return await apiClient.get<ProspectingSession>('/prospecting/sessions/latest');
  } catch (error) {
    return null;
  }
}

async function fetchSessionLogs(sessionId: string): Promise<ProspectingSessionLog[]> {
  return apiClient.get<ProspectingSessionLog[]>(`/prospecting/sessions/${sessionId}/logs`);
}

export function useProspectingSession() {
  return useQuery({
    queryKey: ['prospecting', 'latest'],
    queryFn: fetchLatestSession,
    refetchInterval: (query) => {
      const data = query.state.data as ProspectingSession | null;
      if (!data) return false;
      return data.status === 'pending' || data.status === 'running' || data.status === 'analyzing' ? POLLING_INTERVAL : false;
    },
    retry: 1, // Reduce retries to avoid socket saturation
  });
}

export function useProspectingSessionLogs(sessionId: string | undefined, sessionStatus?: string) {
  return useQuery({
    queryKey: ['prospecting', 'logs', sessionId],
    queryFn: () => fetchSessionLogs(sessionId!),
    enabled: !!sessionId,
    refetchInterval: sessionStatus === 'pending' || sessionStatus === 'running' || sessionStatus === 'analyzing' ? POLLING_INTERVAL : false,
    retry: 1, // Reduce retries to avoid socket saturation
  });
}

export function useCreateProspectingSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createSession,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['prospecting', 'latest'] });
      queryClient.invalidateQueries({ queryKey: ['prospecting', 'logs', data.id] });
    },
  });
}

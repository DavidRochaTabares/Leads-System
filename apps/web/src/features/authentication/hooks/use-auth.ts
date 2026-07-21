import { useEffect } from 'react';
import { supabase } from '@/shared/lib/supabase';
import { useAuthStore } from '@/shared/stores/auth-store';
import { apiClient } from '@/shared/lib/api';

export function useAuth() {
  const { user, isLoading, setUser, setLoading } = useAuthStore();

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      if (session?.access_token) {
        apiClient.setToken(session.access_token);
      }
      setLoading(false);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
      if (session?.access_token) {
        apiClient.setToken(session.access_token);
      } else {
        apiClient.setToken(null);
      }
    });

    return () => subscription.unsubscribe();
  }, [setUser, setLoading]);

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    apiClient.setToken(null);
  };

  return {
    user,
    isLoading,
    signIn,
    signOut,
    isAuthenticated: !!user,
  };
}

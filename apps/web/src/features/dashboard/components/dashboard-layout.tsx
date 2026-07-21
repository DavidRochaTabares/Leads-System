'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { useAuth } from '@/features/authentication/hooks/use-auth';
import { Button } from '@/shared/components/ui/button';
import { LogOut, Menu } from 'lucide-react';
import { useEffect } from 'react';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading, signOut, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const handleSignOut = async () => {
    await signOut();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <button className="lg:hidden">
              <Menu className="h-6 w-6" />
            </button>
            <Image
              src="/spinedev logo horizontal blanco.png"
              alt="SpineDev"
              width={140}
              height={35}
              priority
            />
            <nav className="hidden md:flex items-center gap-4">
              <Link
                href="/dashboard"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/prospecting"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Prospecting
              </Link>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">{user?.email}</span>
            <Button variant="ghost" size="icon" onClick={handleSignOut}>
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}

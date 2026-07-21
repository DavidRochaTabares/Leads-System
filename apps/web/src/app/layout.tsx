import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from '@/shared/providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SpineDev Platform',
  description: 'Internal operating platform for SpineDev',
  icons: {
    icon: [
      {
        url: '/spinedev-text-dark.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/spinedev-text-light.png',
        media: '(prefers-color-scheme: dark)',
      },
    ],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

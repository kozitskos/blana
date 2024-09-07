// app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { NotesPanel } from '@/components/notes-panel';

export default function Page() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');

    // If no token, redirect to login page
    if (!token) {
      router.push('/login');
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  // Show loading state or redirect to login
  if (!isAuthenticated) {
    return <p>Loading...</p>;
  }

  return <NotesPanel />;
}

'use client';

import { useState } from 'react';
import { Button } from '@/shared/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { useCreateProspectingSession } from '../hooks/use-prospecting';

export function ProspectingForm() {
  const [industry, setIndustry] = useState('');
  const [location, setLocation] = useState('');
  const [maxCompanies, setMaxCompanies] = useState(10);
  const createSession = useCreateProspectingSession();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Submitting session:', { industry, location, max_companies: maxCompanies });
    createSession.mutate(
      {
        industry,
        location,
        max_companies: maxCompanies,
      },
      {
        onSuccess: (data) => {
          console.log('Session created successfully:', data);
        },
        onError: (error) => {
          console.error('Error creating session:', error);
        },
      }
    );
  };

  const isRunning = createSession.isPending;
  
  if (createSession.isError) {
    console.error('Mutation error:', createSession.error);
  }

  return (
    <Card className="border-primary/20">
      <CardHeader>
        <CardTitle>Start Prospecting</CardTitle>
        <CardDescription>
          Define the target criteria for your mining session.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="industry" className="text-sm font-medium">
              Industry
            </label>
            <input
              id="industry"
              type="text"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              placeholder="e.g. Software Development"
              className="w-full px-3 py-2 border rounded-md bg-background"
              required
              disabled={isRunning}
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="location" className="text-sm font-medium">
              Location
            </label>
            <input
              id="location"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Miami, FL"
              className="w-full px-3 py-2 border rounded-md bg-background"
              required
              disabled={isRunning}
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="maxCompanies" className="text-sm font-medium">
              Maximum Companies
            </label>
            <input
              id="maxCompanies"
              type="number"
              min={1}
              max={100}
              value={maxCompanies}
              onChange={(e) => setMaxCompanies(Number(e.target.value))}
              className="w-full px-3 py-2 border rounded-md bg-background"
              required
              disabled={isRunning}
            />
          </div>

          <Button
            type="submit"
            className="w-full bg-secondary hover:bg-secondary/90 text-secondary-foreground"
            disabled={isRunning}
          >
            {isRunning ? 'Starting...' : 'Start Mining'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

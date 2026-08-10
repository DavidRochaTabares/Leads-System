"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card";
import { Badge } from "@/shared/components/ui/badge";

interface WhatsAppMessage {
  message?: string; // Legacy field
  preview?: string; // Template preview
  template_name?: string;
  variables?: string[];
  status: string;
  version: number;
  generated_at: string;
}

interface WhatsAppMessageCardProps {
  pipelineId: string;
  message: WhatsAppMessage | null;
  deliveryStatus?: string;
  messageSentAt?: string;
  lastError?: string;
}

async function regenerateMessage(pipelineId: string, setLoading: (loading: boolean) => void) {
  setLoading(true);
  try {
    console.log('[WHATSAPP] Regenerating message for pipeline:', pipelineId);
    const response = await fetch(`http://localhost:8000/sales-pipeline/pipelines/${pipelineId}/regenerate-whatsapp-message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (response.ok) {
      console.log('[WHATSAPP] Message regenerated successfully');
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      const error = await response.text();
      console.error('[WHATSAPP] Failed:', error);
      alert('Failed to regenerate message. Check console for details.');
      setLoading(false);
    }
  } catch (error) {
    console.error('[WHATSAPP] Error:', error);
    alert('Error regenerating message. Check console for details.');
    setLoading(false);
  }
}

function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text);
  alert('Message copied to clipboard!');
}

async function generateMessage(pipelineId: string, setLoading: (loading: boolean) => void) {
  setLoading(true);
  try {
    console.log('[WHATSAPP] Generating message for pipeline:', pipelineId);
    const response = await fetch(`http://localhost:8000/sales-pipeline/pipelines/${pipelineId}/generate-whatsapp-message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (response.ok) {
      console.log('[WHATSAPP] Message generated successfully');
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      const error = await response.text();
      console.error('[WHATSAPP] Failed:', error);
      alert('Failed to generate message. Check console for details.');
      setLoading(false);
    }
  } catch (error) {
    console.error('[WHATSAPP] Error:', error);
    alert('Error generating message. Check console for details.');
    setLoading(false);
  }
}

async function sendMessage(pipelineId: string, setLoading: (loading: boolean) => void) {
  setLoading(true);
  try {
    console.log('[WHATSAPP] Sending message for pipeline:', pipelineId);
    const response = await fetch(`http://localhost:8000/sales-pipeline/pipelines/${pipelineId}/send-whatsapp-message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (response.ok) {
      console.log('[WHATSAPP] Message sent successfully');
      alert('Message sent successfully!');
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      const error = await response.text();
      console.error('[WHATSAPP] Failed:', error);
      alert('Failed to send message. Check console for details.');
      setLoading(false);
    }
  } catch (error) {
    console.error('[WHATSAPP] Error:', error);
    alert('Error sending message. Check console for details.');
    setLoading(false);
  }
}

export function WhatsAppMessageCard({ pipelineId, message, deliveryStatus, messageSentAt, lastError }: WhatsAppMessageCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedMessage, setEditedMessage] = useState(message?.message || '');
  
  const isSent = deliveryStatus === 'sent' || deliveryStatus === 'delivered';
  const isFailed = deliveryStatus === 'failed';

  if (!message) {
    return (
      <Card className="border-muted">
        <CardHeader>
          <CardTitle>WhatsApp Message</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm text-muted-foreground">No message generated yet.</p>
          <button
            onClick={() => generateMessage(pipelineId, setIsLoading)}
            disabled={isLoading}
            className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {isLoading ? 'Generating...' : 'Generate WhatsApp Message'}
          </button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-green-500/30">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-xl flex items-center gap-2">
              WhatsApp Message
              <Badge className="bg-green-500 text-white">
                {message.status === 'ready' ? 'Ready' : message.status}
              </Badge>
            </CardTitle>
            <p className="text-xs text-muted-foreground mt-1">
              Version {message.version} • Generated {new Date(message.generated_at).toLocaleString()}
            </p>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Message Preview */}
        {!isEditing ? (
          <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
              {message.preview || message.message}
            </p>
            {message.variables && (
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Template: {message.template_name || 'cold_outreach_v2'}</p>
              </div>
            )}
          </div>
        ) : (
          <textarea
            value={editedMessage}
            onChange={(e) => setEditedMessage(e.target.value)}
            className="w-full p-4 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 text-sm text-gray-800 dark:text-gray-200 min-h-[200px]"
            placeholder="Edit your WhatsApp message..."
          />
        )}
        {/* Character Count */}
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>{(message.preview || message.message || '').length} characters</span>
          <span>{(message.preview || message.message || '').split(' ').length} words</span>
        </div>

        {/* Delivery Status */}
        {isSent && (
          <div className="bg-green-50 dark:bg-green-950/20 rounded-lg p-3 border border-green-200 dark:border-green-800">
            <p className="text-sm font-medium text-green-800 dark:text-green-200">
              ✓ Message Sent
            </p>
            {messageSentAt && (
              <p className="text-xs text-green-600 dark:text-green-400 mt-1">
                Sent at {new Date(messageSentAt).toLocaleString()}
              </p>
            )}
          </div>
        )}

        {isFailed && lastError && (
          <div className="bg-red-50 dark:bg-red-950/20 rounded-lg p-3 border border-red-200 dark:border-red-800">
            <p className="text-sm font-medium text-red-800 dark:text-red-200">
              ✗ Failed to Send
            </p>
            <p className="text-xs text-red-600 dark:text-red-400 mt-1">
              {lastError}
            </p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2">
          {!isSent ? (
            <button
              onClick={() => sendMessage(pipelineId, setIsLoading)}
              disabled={isLoading}
              className="flex-1 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
            >
              {isLoading ? 'Sending...' : 'Send WhatsApp'}
            </button>
          ) : (
            <button
              onClick={() => sendMessage(pipelineId, setIsLoading)}
              disabled={isLoading}
              className="flex-1 bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
            >
              {isLoading ? 'Resending...' : 'Resend'}
            </button>
          )}
          
          <button
            onClick={() => regenerateMessage(pipelineId, setIsLoading)}
            disabled={isLoading}
            className="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {isLoading ? 'Regenerating...' : 'Regenerate'}
          </button>
          
          <button
            onClick={() => {
              if (isEditing) {
                setIsEditing(false);
              } else {
                setEditedMessage(message.preview || message.message || '');
                setIsEditing(true);
              }
            }}
            disabled={isSent}
            className="flex-1 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {isEditing ? 'Cancel' : 'Edit'}
          </button>
          
          <button
            onClick={() => copyToClipboard(message.preview || message.message || '')}
            className="flex-1 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 text-sm font-medium"
          >
            Copy
          </button>
        </div>

        {/* Note */}
        <div className="bg-yellow-50 dark:bg-yellow-950/20 rounded-lg p-3 border border-yellow-200 dark:border-yellow-800">
          <p className="text-xs text-yellow-800 dark:text-yellow-200">
            <strong>Note:</strong> Review the message before sending. Make sure it sounds natural and personalized.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

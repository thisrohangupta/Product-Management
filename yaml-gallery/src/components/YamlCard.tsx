'use client';
import { useState } from 'react';
import type { YamlFile } from '../lib/getYamls';

export default function YamlCard({ file }: { file: YamlFile }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border rounded-lg p-4 bg-white shadow">
      <h2 className="font-semibold text-sm break-all">{file.relativePath}</h2>
      <button
        className="mt-2 text-sm text-blue-600 underline"
        onClick={() => setOpen(true)}
      >
        View
      </button>

      {open && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white max-w-3xl w-full p-4 rounded shadow-lg relative">
            <button
              className="absolute top-2 right-2 text-sm" 
              onClick={() => setOpen(false)}
            >
              Close
            </button>
            <pre className="whitespace-pre-wrap text-xs overflow-auto max-h-[80vh]">
{file.content}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import React from "react";

interface CleanAnswerRendererProps {
  content: string;
}

/**
 * Cleanly renders answer text without exposing raw Markdown syntax (*, **, ###).
 * Ensures student-friendly typography, highlighted keywords, clean lists, and neat headings.
 */
export function CleanAnswerRenderer({ content }: CleanAnswerRendererProps) {
  if (!content) return null;

  // Split content by lines
  const lines = content.split("\n");
  const elements: React.ReactNode[] = [];

  let currentList: { type: "bullet" | "number"; items: string[] } | null = null;

  const flushList = () => {
    if (!currentList) return;
    const listKey = `list-${elements.length}`;
    if (currentList.type === "bullet") {
      elements.push(
        <ul key={listKey} className="my-3 space-y-2 pl-1">
          {currentList.items.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2.5 text-body text-slate-800 leading-relaxed">
              <span className="w-1.5 h-1.5 rounded-full bg-gold-500 mt-2.5 shrink-0" aria-hidden="true" />
              <span>{renderInlineFormatting(item)}</span>
            </li>
          ))}
        </ul>
      );
    } else {
      elements.push(
        <ol key={listKey} className="my-3 space-y-2 pl-1">
          {currentList.items.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2.5 text-body text-slate-800 leading-relaxed">
              <span className="font-semibold text-gold-600 text-body-sm min-w-5 shrink-0">{idx + 1}.</span>
              <span>{renderInlineFormatting(item)}</span>
            </li>
          ))}
        </ol>
      );
    }
    currentList = null;
  };

  lines.forEach((rawLine, lineIndex) => {
    const line = rawLine.trim();

    if (!line) {
      flushList();
      return;
    }

    // Horizontal rule
    if (line === "---" || line === "***" || line === "===") {
      flushList();
      elements.push(<hr key={`hr-${lineIndex}`} className="my-4 border-slate-200" />);
      return;
    }

    // Headings (### or ## or #)
    if (line.startsWith("#")) {
      flushList();
      const headingText = line.replace(/^#+\s*/, "").replace(/\*\*/g, "");
      elements.push(
        <h4
          key={`heading-${lineIndex}`}
          className="text-body-lg font-bold text-navy-900 mt-4 mb-2 tracking-tight"
        >
          {headingText}
        </h4>
      );
      return;
    }

    // Bullet items (* item or - item or • item)
    const bulletMatch = line.match(/^[\*\-•]\s+(.*)$/);
    if (bulletMatch) {
      if (!currentList || currentList.type !== "bullet") {
        flushList();
        currentList = { type: "bullet", items: [] };
      }
      currentList.items.push(bulletMatch[1]);
      return;
    }

    // Numbered items (1. item)
    const numberMatch = line.match(/^\d+[\.\)]\s+(.*)$/);
    if (numberMatch) {
      if (!currentList || currentList.type !== "number") {
        flushList();
        currentList = { type: "number", items: [] };
      }
      currentList.items.push(numberMatch[1]);
      return;
    }

    // Standard paragraph
    flushList();
    elements.push(
      <p key={`p-${lineIndex}`} className="text-body text-slate-800 leading-relaxed mb-3">
        {renderInlineFormatting(line)}
      </p>
    );
  });

  flushList();

  return <div className="space-y-1">{elements}</div>;
}

/**
 * Parses inline formatting like **bold**, *italic*, and `code`.
 */
function renderInlineFormatting(text: string): React.ReactNode {
  // Regex to split by bold (**bold**), italic (*italic*), and inline code (`code`)
  const regex = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  const parts = text.split(regex);

  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      const clean = part.slice(2, -2);
      return (
        <strong key={index} className="font-semibold text-navy-900">
          {clean}
        </strong>
      );
    }
    if (part.startsWith("*") && part.endsWith("*")) {
      const clean = part.slice(1, -1);
      return (
        <em key={index} className="italic text-slate-700">
          {clean}
        </em>
      );
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      const clean = part.slice(1, -1);
      return (
        <code key={index} className="px-1.5 py-0.5 rounded bg-slate-100 text-navy-800 font-mono text-caption">
          {clean}
        </code>
      );
    }
    return part;
  });
}

import { useState } from "react";

interface SpoilerTextProps {
  text: string;
}

export function SpoilerText({ text }: SpoilerTextProps) {
  const [revealed, setRevealed] = useState(false);

  if (revealed) {
    return <p className="leading-relaxed text-muted-foreground">{text}</p>;
  }

  return (
    <button
      type="button"
      onClick={() => setRevealed(true)}
      className="relative cursor-pointer text-left"
    >
      <p aria-hidden="true" className="leading-relaxed text-muted-foreground blur-sm select-none">
        {text}
      </p>
      <span className="absolute inset-0 flex items-center justify-center text-sm font-medium">
        Unhide Spoiler!
      </span>
    </button>
  );
}
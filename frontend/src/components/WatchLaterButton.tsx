import { useState } from "react";
import { Bookmark, BookmarkCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { authFetch } from "@/lib/api";

interface WatchLaterButtonProps {
  tmdbId: number;
}

export function WatchLaterButton({ tmdbId }: WatchLaterButtonProps) {
  const [status, setStatus] = useState<"idle" | "saving" | "saved" | "error">("idle");

  async function save() {
    setStatus("saving");
    try {
      const response = await authFetch("/api/watch-later", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tmdb_id: tmdbId }),
      });
      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }
      setStatus("saved");
    } catch (err) {
      console.error("Failed to save film:", err);
      setStatus("error");
    }
  }

  if (status === "saved") {
    return (
      <Button variant="secondary" size="sm" disabled>
        <BookmarkCheck data-icon="inline-start" />
        Saved
      </Button>
    );
  }

  return (
    <Button variant="outline" size="sm" onClick={save} disabled={status === "saving"}>
      <Bookmark data-icon="inline-start" />
      {status === "saving" ? "Saving..." : status === "error" ? "Try again" : "Watch later"}
    </Button>
  );
}
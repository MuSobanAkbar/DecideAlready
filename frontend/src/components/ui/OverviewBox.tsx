import { useEffect, useState } from "react";

interface OverviewBoxProps {
  movieId: number;
}

export function OverviewBox({ movieId }: OverviewBoxProps) {
  const [overview, setOverview] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/overview/${movieId}`)
      .then((response) => response.json())
      .then((data) => setOverview(data.overview));
  }, [movieId]);

  return <p>{overview}</p>;
}
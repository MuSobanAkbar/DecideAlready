import { useState } from 'react'
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface MovieResponse
{
    title: string;
    overview: string;
    date: string;
    poster_path: string | null;
}

export default function App() {

  const [movie, setMovie] = useState<MovieResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
 

  async function fetchRandomMovie() {
    setIsLoading(true);
 
    try {

      const response = await fetch("/api/random");
 

      const data: MovieResponse = await response.json();
 
      
      setMovie(data);
    } catch (error) {
      console.error("Failed to fetch movie:", error);

    } finally {
      setIsLoading(false);
    }
  }
 

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "sans-serif " }}>
      <h1>Random Movie Picker</h1>
 

      <button
        onClick={fetchRandomMovie}
        disabled={isLoading}
        style={{ padding: "10px 20px", fontSize: "16px", cursor: "pointer" }}
      >
        {isLoading ? "Picking..." : "Get Random Movie"}
      </button>
      {movie && (
        <>
          <h2 style={{ marginTop: "30px" }}>{movie.title}</h2>
          <p style={{ maxWidth: "600px", margin: "20px auto" }}>{movie.overview}</p>
          <p>Release Date: {movie.date}</p>
          <img
            src={movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : ""}
            alt={movie.title}
            style={{ maxWidth: "300px", marginTop: "20px" }}
          />
        </>
      )}
    </div>
  );
}
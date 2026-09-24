import { useState } from 'react'


interface MovieResponse
{
    title: string;
}

export default function App() {

  const [movieTitle, setMovieTitle] = useState("");
  const [isLoading, setIsLoading] = useState(false);
 

  async function fetchRandomMovie() {
    setIsLoading(true);
 
    try {

      const response = await fetch("http://localhost:8000/api/random");
 

      const data: MovieResponse = await response.json();
 

      setMovieTitle(data.title);
    } catch (error) {
      console.error("Failed to fetch movie:", error);
      setMovieTitle("Failed to load movie. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  }
 

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "sans-serif" }}>
      <h1>Random Movie Picker</h1>
 

      <button
        onClick={fetchRandomMovie}
        disabled={isLoading}
        style={{ padding: "10px 20px", fontSize: "16px", cursor: "pointer" }}
      >
        {isLoading ? "Picking..." : "Get Random Movie"}
      </button>
 
      {movieTitle && <h2 style={{ marginTop: "30px" }}>{movieTitle}</h2>}
    </div>
  );
}
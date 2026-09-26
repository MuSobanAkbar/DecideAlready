**Problem Statement**   
“Sometimes me and my friend have trouble finding movies. There’s so many of them, and we want a quick way to find random movies, with details, and keep track of them.”

**Goals**  
Click on a button, and it will give back a movie name.

**Non Goals**

- It does not show anything other than the movie name.   
- Web page, but also working on mobile.  
- No sign-in page.  
- No AI-review.

**Success Criteria**  
\- Upon clicking on a button, a title and poster shows.

- Clicking again, gives a different film.  
- If the API fails, it shows an error for that 

**Solution:** one HTML page, fetch to TMDB, render the result.

**Alternatives considered:** OMDb  rejected, movies only and 1,000/day. Hardcoding a list rejected, defeats the point.

**Risks:** the API key is visible in client-side code. For a personal project that's an accepted risk but when I deploy it publicly, I’ll put a small backend in front and keep the token there.


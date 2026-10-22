import { useState, type FormEvent } from "react";
import { useSession } from "@/hooks/useSession";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { supabase } from "@/lib/supabase";
import { authFetch } from "@/lib/api";
export function AuthBar() {
  const session = useSession();
  const userEmail = session?.user.email ?? null;
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);



  async function sendLink(event: FormEvent) {
    event.preventDefault();
    setError(null);
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: window.location.origin },
    });
    if (error) {
      setError(error.message);
    } else {
      setSent(true);
    }
  }

  if (userEmail) {
    return (
      <div className="flex items-center gap-3 text-sm">
        <span className="text-muted-foreground">Signed in as {userEmail}</span>
        <Button
          variant="ghost"
          size="sm"
          onClick={async () => {
            const response = await authFetch("/api/me");
            alert(JSON.stringify(await response.json()));
          }}
        >
          Who am I?
        </Button>
        <Button variant="outline" size="sm" onClick={() => supabase.auth.signOut()}>
          Sign out
        </Button>
      </div>
    );
  }
<Button
  variant="ghost"
  size="sm"
  onClick={async () => {
    const response = await authFetch("/api/me");
    alert(JSON.stringify(await response.json()));
  }}
>
  Who am I?
</Button>
  if (sent) {
    return <p className="text-sm text-muted-foreground">Check your email for the sign-in link.</p>;
  }

  return (
    <form onSubmit={sendLink} className="flex items-center gap-2">
      <Input
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@email.com"
        className="w-56"
      />
      <Button type="submit" size="sm">Email me a link</Button>
      {error && <p className="text-sm text-destructive">{error}</p>}
    </form>
  );
}
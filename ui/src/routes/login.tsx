import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState, useEffect } from "preact/hooks";
import { useAuth } from "../lib/auth";

export const Route = createFileRoute("/login")({
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const { isLoggedIn, login, error } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (isLoggedIn) {
      navigate({ to: "/" });
    }
  }, [isLoggedIn, navigate]);

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setIsSubmitting(true);
    const success = await login(username, password);
    setIsSubmitting(false);
    if (success) {
      navigate({ to: "/" });
    }
  };

  if (isLoggedIn) {
    return null; // Or a loading spinner, as the redirect will happen immediately
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-100">
      <div className="rounded-lg overflow-hidden border border-neutral-200/60 bg-white text-neutral-700 shadow-sm w-[380px] p-7">
        <h2 className="mb-4 text-2xl font-bold text-center text-neutral-800">Login</h2>
        {error && (
          <div className="relative w-full rounded-lg border bg-white p-4 mb-4 [&>svg]:absolute [&>svg]:text-foreground [&>svg]:left-4 [&>svg]:top-4 [&>svg+div]:translate-y-[-3px] [&:has(svg)]:pl-11 text-red-700 border-red-300 bg-red-50">
            <svg className="w-4 h-4 text-red-500" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" x2="20" y1="19" y2="19"></line></svg>
            <h5 className="mb-1 font-medium leading-none tracking-tight">Login Error</h5>
            <div className="text-sm opacity-70">{error}</div>
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-neutral-700 mb-1">Username</label>
            <input
              type="text"
              id="username"
              className="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-neutral-400"
              placeholder="username"
              value={username}
              onInput={(e) => setUsername((e.target as HTMLInputElement).value)}
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-neutral-700 mb-1">Password</label>
            <input
              type="password"
              id="password"
              className="w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-neutral-400"
              placeholder="password"
              value={password}
              onInput={(e) => setPassword((e.target as HTMLInputElement).value)}
              required
            />
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="inline-flex items-center justify-center w-full px-4 py-2 text-sm font-medium tracking-wide text-white transition-colors duration-200 rounded-md bg-neutral-950 hover:bg-neutral-900 focus:ring-2 focus:ring-offset-2 focus:ring-neutral-900 focus:shadow-outline focus:outline-none"
          >
            {isSubmitting ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}


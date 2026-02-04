import { createFileRoute, useNavigate } from "@tanstack/react-router";
import type { TargetedSubmitEvent } from "preact";
import { useEffect, useState } from "preact/hooks";
import z from "zod";
import { account } from "../lib/appwrite";
import type { AppwriteException } from "appwrite";

const SigninSchema = z.object({
  email: z.email("Invalid Email"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(255, "Password must be less then 255 characters"),
});

export const Route = createFileRoute("/login")({
  component: LoginPage,
});

function LoginPage() {
  const [fieldErrors, setFieldErrors] = useState<Record<string, string[]>>({});
  const navigate = useNavigate();


  useEffect(() => {
    const verifySession = async () => {
      try {
        await account.get();
        // If this succeeds, they are logged in. Redirect them!
        navigate({ to: '/' });
      } catch (error) {
        // They aren't logged in. Stay on this page.
      }
    };

    verifySession();
  }, []);


  const onLoginFormSubmit = async (
    event: TargetedSubmitEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data = Object.fromEntries(formData.entries());
    const result = SigninSchema.safeParse(data);
    if (!result.success) {
      const flattened = result.error.flatten().fieldErrors;
      setFieldErrors(flattened);
      return;
    }
    setFieldErrors({});
    try {
      const session = await account.createEmailPasswordSession(result.data);

      navigate({ to: "/" });
    } catch (error) {
      setFieldErrors({
        form: [
          (error as AppwriteException).message || "Invalid email or password",
        ],
      });
    }
  };
  return (
    <main style={{ padding: "1rem" }}>
      <h1>Signup</h1>
      <form onSubmit={onLoginFormSubmit}>
        <input
          name="email"
          type="email"
          placeholder="me@example.com"
          id="email"
        />
        <input name="password" type="password" id="password" />
        <button type="submit">Login</button>
      </form>
      <div>
        {Object.entries(fieldErrors).map(([field, messages]) => (
          <div key={field} style={{ color: "red", marginBottom: "0.5rem" }}>
            <strong>{field}:</strong>
            <ul>
              {messages.map((msg, index) => (
                <li key={index}>{msg}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </main>
  );
}


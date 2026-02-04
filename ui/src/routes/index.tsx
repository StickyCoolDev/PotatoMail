import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  component: Home,
});

function Home() {
  return (
    <main style={{ padding: '1rem' }}>
      <h1>Welcome to the Preact Homepage</h1>
      <p>This is rendered via TanStack Router!</p>
    </main>
  );
}


import { createFileRoute, useNavigate } from '@tanstack/react-router';


export const Route = createFileRoute('/')({
  component: Home,
});

function Home() {
  const navigate = useNavigate();


  
  return (
    <main style={{ padding: '2rem' }}>
      <h1>Admin Portal</h1>
      <p>The Admin Portal of 🥔PotatoMail</p>
    </main>
  );
}


// src/routes/__root.tsx
import { createRootRoute, Link, Outlet } from '@tanstack/react-router'
import { useAuth } from '../lib/auth';

export const Route = createRootRoute({
  component: () => {
    const { isLoggedIn, logout } = useAuth();
    return (
      <>
        <div className="p-4 flex gap-4 bg-neutral-900 text-white">
          <Link to="/" className="[&.active]:font-bold">
            Home
          </Link>
          {!isLoggedIn ? (
            <Link to="/login" className="[&.active]:font-bold">
              Login
            </Link>
          ) : (
            <button
              onClick={logout}
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium tracking-wide text-white transition-colors duration-200 rounded-md bg-red-600 hover:bg-red-700 focus:ring-2 focus:ring-offset-2 focus:ring-red-600 focus:shadow-outline focus:outline-none"
            >
              Sign Out
            </button>
          )}
        </div>
        <hr />
        <Outlet />
      </>
    );
  },
})



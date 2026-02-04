import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface AuthContextType {
  isLoggedIn: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(() => {
    const storedLoginStatus = localStorage.getItem('isLoggedIn');
    return storedLoginStatus === 'true';
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    localStorage.setItem('isLoggedIn', String(isLoggedIn));
  }, [isLoggedIn]);

  const login = async (username: string, password: string) => {
    // In a real application, you would send these credentials to a backend
    // and receive a token or session cookie.
    // For this example, we'll use a simple hardcoded check.
    if (username === 'user' && password === 'password') {
      setIsLoggedIn(true);
      setError(null);
      return true;
    } else {
      setError('Invalid username or password.');
      return false;
    }
  };

  const logout = () => {
    setIsLoggedIn(false);
    setError(null);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout, error }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

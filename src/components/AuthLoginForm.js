import React, { useState } from 'react';

const AuthLoginForm = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Por favor completa todos los campos');
      return;
    }
    onLogin({ email, password });
  };

  return (
    <div className="max-w-md mx-auto bg-white p-10 rounded-2xl shadow-xl border border-gray-100">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <img 
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMUNZL2_9W52Eyri9sTGKNboQd_-Vt8Il5fA&s" 
            alt="Teus delivery"
            className="h-24"
          />
        </div>
        <h1 className="text-3xl font-bold text-[#004aad] mb-2">Teus</h1>
        <p className="text-xl text-gray-600 font-medium">Delivery</p>
      </div>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700 text-sm font-medium mb-1" htmlFor="email">
            Correo Institucional
          </label>
          <input
            id="email"
            type="email"
            className="w-full px-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#004aad] focus:border-transparent"
            placeholder="tu@tec.mx"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        
        <div>
          <label className="block text-gray-700 text-sm font-medium mb-1" htmlFor="password">
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            className="w-full px-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#004aad] focus:border-transparent"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="pt-2">
          <button
            type="submit"
            className="w-full bg-[#004aad] text-white py-2 px-4 rounded-lg hover:bg-[#003b8a] transition-colors focus:outline-none focus:ring-2 focus:ring-[#004aad] focus:ring-offset-2 font-medium"
          >
            Iniciar Sesión
          </button>
        </div>
      </form>

      <div className="mt-6 text-center text-sm text-gray-500">
        <p>¿No tienes cuenta? <a href="#" className="text-[#004aad] hover:underline">Regístrate aquí</a></p>
      </div>
    </div>
  );
};

export default AuthLoginForm;
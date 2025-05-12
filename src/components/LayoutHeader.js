import React from 'react';
import CartIcon from './CartIcon';

const LayoutHeader = ({ user, onLogout, cartItems, onCartClick }) => {
  return (
    <header className="bg-[#004aad] shadow-sm sticky top-0 z-10">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-white">Teus</h1>
          <span className="ml-1 text-white">Delivery</span>
        </div>
        {user ? (
          <div className="flex items-center space-x-6">
            <CartIcon itemCount={cartItems} onClick={onCartClick} />
            <span className="text-white text-sm">Hola, {user.name.split(' ')[0]}</span>
            <button
              onClick={onLogout}
              className="bg-white text-[#004aad] px-3 py-1 rounded-lg text-sm hover:bg-gray-100 transition-colors"
            >
              Salir
            </button>
          </div>
        ) : null}
      </div>
    </header>
  );
};

export default LayoutHeader;
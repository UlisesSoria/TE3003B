import React from 'react';
import CartItem from './CartItem';

const CartSidebar = ({ cart, isOpen, onClose, onRemoveItem, onCheckout }) => {
  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className={`fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-xl transform ${isOpen ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300 ease-in-out z-20`}>
      <div className="flex flex-col h-full">
        <div className="flex justify-between items-center p-4 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">Tu Carrito</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex-grow overflow-y-auto p-4">
          {cart.length === 0 ? (
            <p className="text-gray-500 text-center py-8">Tu carrito está vacío</p>
          ) : (
            cart.map(item => (
              <CartItem 
                key={item.id} 
                item={item} 
                onRemove={onRemoveItem}
              />
            ))
          )}
        </div>

        {cart.length > 0 && (
          <div className="border-t border-gray-200 p-4">
            <div className="flex justify-between mb-4">
              <span className="font-medium">Total:</span>
              <span className="font-bold">${total.toFixed(2)}</span>
            </div>
            <button
              onClick={onCheckout}
              className="w-full bg-[#004aad] text-white py-2 px-4 rounded-lg hover:bg-[#003b8a] transition-colors"
            >
              Finalizar Compra
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default CartSidebar;
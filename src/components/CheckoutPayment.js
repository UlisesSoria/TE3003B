import React, { useState } from 'react';

const CheckoutPayment = ({ cart, total, onBack, onCompleteOrder }) => {
  const [paymentMethod, setPaymentMethod] = useState('card');

  const handleSubmit = (e) => {
    e.preventDefault();
    onCompleteOrder(paymentMethod);
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md border border-gray-100">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Finalizar Pedido</h2>
      
      <div className="mb-6">
        <h3 className="font-medium text-gray-700 mb-3">Resumen del Pedido</h3>
        <div className="space-y-2 mb-4">
          {cart.map(item => (
            <div key={item.id} className="flex justify-between text-sm">
              <span>{item.name}</span>
              <span>${item.price.toFixed(2)}</span>
            </div>
          ))}
        </div>
        <div className="flex justify-between border-t border-gray-200 pt-2 font-medium">
          <span>Total:</span>
          <span className="text-[#004aad]">${total.toFixed(2)}</span>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <h3 className="font-medium text-gray-700 mb-3">Método de Pago</h3>
          <div className="space-y-3">
            <label className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:border-[#004aad] cursor-pointer">
              <input
                type="radio"
                name="payment"
                value="card"
                checked={paymentMethod === 'card'}
                onChange={() => setPaymentMethod('card')}
                className="h-4 w-4 text-[#004aad] focus:ring-[#004aad]"
              />
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              <span>Tarjeta de Crédito/Débito</span>
            </label>

            <label className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:border-[#004aad] cursor-pointer">
              <input
                type="radio"
                name="payment"
                value="paypal"
                checked={paymentMethod === 'paypal'}
                onChange={() => setPaymentMethod('paypal')}
                className="h-4 w-4 text-[#004aad] focus:ring-[#004aad]"
              />
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M7.5 11.5h1.5v-4h-1.5v4zm3.5 0h1.5v-4H11v4zm3.5 0h1.5v-4h-1.5v4zm-10-8c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h13c1.1 0 2-.9 2-2v-10c0-1.1-.9-2-2-2h-13zm13 1.5c.3 0 .5.2.5.5v10c0 .3-.2.5-.5.5h-13c-.3 0-.5-.2-.5-.5v-10c0-.3.2-.5.5-.5h13z" />
              </svg>
              <span>PayPal</span>
            </label>

            <label className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:border-[#004aad] cursor-pointer">
              <input
                type="radio"
                name="payment"
                value="apple"
                checked={paymentMethod === 'apple'}
                onChange={() => setPaymentMethod('apple')}
                className="h-4 w-4 text-[#004aad] focus:ring-[#004aad]"
              />
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-black" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
              </svg>
              <span>Apple Pay</span>
            </label>
          </div>
        </div>

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={onBack}
            className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Volver
          </button>
          <button
            type="submit"
            className="flex-1 bg-[#004aad] text-white py-2 px-4 rounded-lg hover:bg-[#003b8a] transition-colors"
          >
            Confirmar Pedido
          </button>
        </div>
      </form>
    </div>
  );
};

export default CheckoutPayment;
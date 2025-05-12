import React, { useState, useEffect } from 'react';
import users from './mock/users';
import products from './mock/products';
import stores from './mock/stores';
import AuthLoginForm from './components/AuthLoginForm';
import LayoutHeader from './components/LayoutHeader';
import ProductGrid from './components/ProductGrid';
import StoreGrid from './components/StoreGrid';
import CartSidebar from './components/CartSidebar';
import CheckoutPayment from './components/CheckoutPayment';
import OrderConfirmation from './components/OrderConfirmation';
import ToastNotification from './components/ToastNotification';

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [cart, setCart] = useState([]);
  const [currentView, setCurrentView] = useState('login');
  const [selectedStore, setSelectedStore] = useState(null);
  const [storeProducts, setStoreProducts] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  const handleLogin = ({ email, password }) => {
    const user = users.find(
      (u) => u.email === email && u.password === password
    );
    if (user) {
      setCurrentUser(user);
      setCurrentView('stores');
      localStorage.setItem('currentUser', JSON.stringify(user));
    } else {
      alert('Credenciales incorrectas');
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setCurrentView('login');
    setCart([]);
    localStorage.removeItem('currentUser');
  };

  const handleAddToCart = (product) => {
    setCart([...cart, product]);
    setToastMessage(`${product.name} añadido al carrito`);
    setShowToast(true);
  };

  const handleRemoveFromCart = (productId) => {
    setCart(cart.filter(item => item.id !== productId));
  };

  const handleSelectStore = (store) => {
    setSelectedStore(store);
    const filteredProducts = products.filter(p => p.storeId === store.id);
    setStoreProducts(filteredProducts);
    setCurrentView('products');
  };

  const handleBackToStores = () => {
    setSelectedStore(null);
    setCurrentView('stores');
  };

  const handleCompleteOrder = (paymentMethod) => {
    setIsCheckoutOpen(false);
    setShowConfirmation(true);
    // En una app real, aquí se enviaría el pedido al backend
  };

  const handleCloseConfirmation = () => {
    setShowConfirmation(false);
    setCart([]);
    setCurrentView('stores');
  };

  useEffect(() => {
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      setCurrentUser(JSON.parse(storedUser));
      setCurrentView('stores');
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {currentUser && (
        <LayoutHeader 
          user={currentUser} 
          onLogout={handleLogout} 
          cartItems={cart.length}
          onCartClick={() => setIsCartOpen(true)}
        />
      )}

      <CartSidebar
        cart={cart}
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        onRemoveItem={handleRemoveFromCart}
        onCheckout={() => {
          setIsCartOpen(false);
          setIsCheckoutOpen(true);
        }}
      />

      {isCheckoutOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-30">
          <CheckoutPayment
            cart={cart}
            total={cart.reduce((sum, item) => sum + item.price, 0)}
            onBack={() => setIsCheckoutOpen(false)}
            onCompleteOrder={handleCompleteOrder}
          />
        </div>
      )}

      {showConfirmation && (
        <OrderConfirmation 
          orderDetails={{
            items: cart,
            total: cart.reduce((sum, item) => sum + item.price, 0),
            store: selectedStore?.name
          }}
          onClose={handleCloseConfirmation}
        />
      )}

      {showToast && (
        <ToastNotification 
          message={toastMessage}
          onClose={() => setShowToast(false)}
        />
      )}

      <main className={currentView === 'login' ? 'bg-gradient-to-b from-[#f0f7ff] to-white' : ''}>
        {currentView === 'login' && !currentUser && (
          <div className="flex items-center justify-center min-h-screen p-4">
            <AuthLoginForm onLogin={handleLogin} />
          </div>
        )}
        {currentView === 'stores' && currentUser && (
          <StoreGrid stores={stores} onSelectStore={handleSelectStore} />
        )}
        {currentView === 'products' && currentUser && (
          <>
            <div className="container mx-auto px-4 pt-6">
              <button 
                onClick={handleBackToStores}
                className="flex items-center text-[#004aad] hover:text-[#003b8a] mb-4"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
                </svg>
                Volver a tiendas
              </button>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">{selectedStore.name}</h2>
            </div>
            <ProductGrid products={storeProducts} onAddToCart={handleAddToCart} />
          </>
        )}
      </main>
    </div>
  );
};

export default App;

// DONE
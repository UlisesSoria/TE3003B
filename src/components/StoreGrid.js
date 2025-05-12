import React from 'react';
import StoreCard from './StoreCard';

const StoreGrid = ({ stores, onSelectStore }) => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Selecciona una tienda</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {stores.map((store) => (
          <div key={store.id} className="transition-transform duration-300 hover:scale-[1.03]">
            <StoreCard
              store={store}
              onSelect={onSelectStore}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default StoreGrid;
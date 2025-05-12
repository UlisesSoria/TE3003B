import React from 'react';

const StoreCard = ({ store, onSelect }) => {
  return (
    <div 
      className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] cursor-pointer"
      onClick={() => onSelect(store)}
    >
      <div className="h-40 bg-gray-100 flex items-center justify-center p-4 transition-all duration-300 hover:bg-gray-50">
        <img 
          src={store.logo} 
          alt={store.name}
          className="max-h-full max-w-full object-contain transition-transform duration-300 hover:scale-105"
        />
      </div>
      <div className="p-4">
        <h3 className="font-bold text-lg text-gray-800 group-hover:text-[#004aad] transition-colors duration-300">{store.name}</h3>
        <p className="text-gray-600 text-sm">{store.category}</p>
        <div className="mt-2 flex items-center">
          <span className="text-xs text-[#004aad] bg-[#004aad]/10 px-2 py-1 rounded-full transition-all duration-300 group-hover:bg-[#004aad]/20">
            Ver productos
          </span>
        </div>
      </div>
    </div>
  );
};

export default StoreCard;
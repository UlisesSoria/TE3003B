import React from 'react';
import AddToCartButton from './AddToCartButton';

const ProductCard = ({ product, onAddToCart }) => {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:scale-[1.02] group">
      <div className="h-48 overflow-hidden relative">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </div>
      <div className="p-4">
        <h3 className="font-bold text-lg text-gray-800 group-hover:text-[#004aad] transition-colors duration-300">{product.name}</h3>
        <p className="text-gray-600 text-sm line-clamp-2">{product.description}</p>
        <div className="flex justify-between items-center mt-3">
          <span className="font-bold text-gray-800 group-hover:text-[#004aad] transition-colors duration-300">${product.price.toFixed(2)}</span>
          <AddToCartButton onClick={() => onAddToCart(product)} />
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
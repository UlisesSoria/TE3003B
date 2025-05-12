import React, { useState } from 'react';

const AddToCartButton = ({ onClick }) => {
  const [isAnimating, setIsAnimating] = useState(false);

  const handleClick = () => {
    setIsAnimating(true);
    onClick();
    setTimeout(() => setIsAnimating(false), 1000);
  };

  return (
    <button
      onClick={handleClick}
      className={`bg-[#004aad] text-white px-3 py-1 rounded-lg text-sm hover:bg-[#003b8a] transition-all duration-300 transform ${isAnimating ? 'animate-bounce' : 'hover:scale-110'}`}
    >
      Añadir
    </button>
  );
};

export default AddToCartButton;

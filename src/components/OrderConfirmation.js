import React, {useEffect} from 'react';
import mqtt from 'mqtt';
import stores from '../mock/stores';

const OrderConfirmation = ({ orderDetails, onClose }) => {
  // React: enviar orden de delivery
  /*fetch("http://10.25.85.208:8000/send-command/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cmd: "deliver_order_123" })
  })
  .then(res => res.json())
  .then(data => console.log(data));
*/
  // MQTT Implementation
  useEffect(() => {
    const client = mqtt.connect("ws://10.25.101.96:9001");

    client.on("connect", () => {
      console.log("Connected to MQTT broker (Websocket connection)");
    // Coordinates by restaurant
      const coords = {
        "Starbucks": {x: 1.0, y: 1.1, theta: 0.0},
        "Sinforosa": {x: 1.5, y: 0.2, theta: 0.0},
        "Tec Store": {x: 0.8, y: 1.6, theta: 0.0},
        "Subway": {x: 0.5, y: 1.2, theta: 0.0},
        "Tim Hortons": {x: 1.7, y: 2.2, theta: 0.0},
        "Nutrisa": {x: 0.3, y: 1.2, theta: 0.0},
        "Lechuguini": {x: 0.2, y: 2.7, theta: 0.0},
        "Cinnabon": {x: 2.7, y: 2.7, theta: 0.0},
        "Yukapioca": {x: 2.8, y: 1.2, theta: 0.0},
        "Yellow Spot": {x: 2.3, y: 1.0, theta: 0.0},
        "Mr. Grill": {x: 2.3, y: 0.3, theta: 0.0},
        "Daisuki Sushi": {x: 2.8, y: 0.8, theta: 0.0},
      };
      console.log("📦 orderDetails:", orderDetails);

      const restaurantName = orderDetails?.store?.trim?.(); 
      // console.log("🏪 Store recibido:", stores);
      const coord = coords[restaurantName];
      console.log("🏪 Restaurante recibido:", restaurantName);

      if (coord) {
        client.publish("puzzlebot/goal", JSON.stringify(coord));
        console.log(`📡 Coordenadas publicadas para ${restaurantName}:`, coord);
      } else {
        console.warn("⚠️ Restaurante no reconocido o faltan detalles:", restaurantName);
      }
    });

    return () => {
      client.end();
    };
  }, [orderDetails]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-40">
      <div className="bg-white rounded-xl p-6 max-w-md w-full">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-[#004aad] mb-2">¡Pedido Confirmado!</h2>
          <p className="text-gray-600">Tu pedido está siendo preparado</p>
          <p className="text-gray-600">TeusDelivery te pedirá el siguiente código QR.</p>
          <p className="text-gray-600"> Posiciónate frente a Teus y escanea el código QR para recibir tu pedido.</p>
        </div>

        <div className="flex justify-center mb-6">
          <div className="bg-white p-4 rounded-lg border-2 border-dashed border-[#004aad]">
            {/* QR Code Placeholder - En producción usaría una librería QR generator */}
            <div className="w-48 h-48 bg-gray-100 flex items-center justify-center text-gray-400">
              
              <img
                src="https://play-lh.googleusercontent.com/lomBq_jOClZ5skh0ELcMx4HMHAMW802kp9Z02_A84JevajkqD87P48--is1rEVPfzGVf" 
                alt="QR Code"  
              />
            </div>
          </div>
        </div>

        <div className="space-y-4 mb-6">
          <div className="flex items-start">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-[#004aad] mr-2 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <div>
              <h3 className="font-bold text-gray-800">Ubicación de recolección</h3>
              <p className="text-gray-600">Punto de entrega principal - Edificio 3</p>
              <img
                src = "https://www.uber-assets.com/image/upload/f_auto,q_auto:eco,c_fill,h_270,w_1152/v1675303138/assets/43/96f57a-b9ac-4507-a15a-307ed37ae6a1/original/SmartApp-GTM_Web_Divider_D.png"
                alt = "Ubicación de recolección"
                className="w-full h-auto mt-2 rounded-lg"
              />
            </div>
          </div>

          <div className="flex items-start">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-[#004aad] mr-2 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h3 className="font-bold text-gray-800">Tiempo estimado</h3>
              <p className="text-gray-600">15-20 minutos</p>
            </div>
          </div>
        </div>

        <button
          onClick={onClose}
          className="w-full bg-[#004aad] text-white py-3 rounded-lg hover:bg-[#003b8a] transition-colors"
        >
          Entendido
        </button>
      </div>
    </div>
    
  );
  
};

export default OrderConfirmation;
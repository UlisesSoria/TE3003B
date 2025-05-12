const products = [
  {
    id: 1,
    name: "Café Americano",
    description: "Café caliente tamaño grande",
    price: 35.00,
    image: "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5",
    storeId: 1
  },
  {
    id: 2,
    name: "Sandwich de pavo y panela",
    description: "Sandwich fresco con jamón y queso",
    price: 80.00,
    image: "https://djftrby1k8irl.cloudfront.net/s3fs-public/2022-02%2FSandwich%20Pavo%20Panela_1.png?auto=format,compress&q=70&crop=focalpoint&ar=1:1.0&w=180&fit=crop",
    storeId: 1
  },
  {
    id: 3,
    name: "Ensalada de quinoa",
    description: "Ensalada fresca con aderezo de mostaza",
    price: 180.00,
    image: "https://images.rappi.com.mx/products/tmpImgd1eb66a1-1a16-4270-acea-d76317a9fab0.png?d=300x300&e=webp&q=10",
    storeId: 2
  },
  {
    id: 4,
    name: "French Toast",
    description: "French toast con jarabe de arce",
    price: 180.00,
    image: "https://images.rappi.com.mx/products/tmpImgb4f286ee-daa5-4376-bb3d-3e469db5ca00.png?d=300x300&e=webp&q=10",
    storeId: 2
  },
  {
    id: 5,
    name: "Moras",
    description: "Es una bebida a base de jamaica con frutos rojos.",
    price: 70.00,
    image: "https://images.rappi.com.mx/products/tmpImgec4dfce9-4a8b-4ba6-a1db-871bb301d798.png?d=300x300&e=webp&q=10",
    storeId: 2
  },
  {
    id: 6,
    name: "Gorra G47 Mvp Clasic TEC Azul",
    description: "Gorra de beisbol con logo del Tec de Monterrey",
    price: 599.00,
    image: "https://tecstore.mx/cdn/shop/files/WS-MVP213WBV-SB-HR-F_490x.progressive.jpg?v=1708442245",
    storeId: 3
  },
  {
    id: 7,
    name: "Sudadera Essential Borregos Unisex Azul",
    description: "Sudadera de algodón con logo del Tec de Monterrey",
    price: 899.00,
    image: "https://tecstore.mx/cdn/shop/products/Sudadera-Essential-BORREGOS-unisex-azul_01_490x.progressive.jpg?v=1703631248",
    storeId: 3
  },
  {
    id: 8,
    name: "2 Subs x 119",
    description: "Elige 2 Subs 15 cms entre Jamón, Milanesa 3 Quesos o Atún",
    price: 119.00,
    image: "https://cdn.urbanpiper.com/media/bizmedia/2025/05/02/iDis-ef70ef5e-8a21-4b2d-aa83-52918d7cd104.png?width=300",
    storeId: 4
  },
  {
    id: 9,
    name: "Galleta de chocolate",
    description: "Galleta de chocolate con chispas de chocolate",
    price: 30.00,
    image: "https://cdn.urbanpiper.com/media/bizmedia/2025/05/02/eblEl8Y-0fa3df9a-af5c-46a1-aca7-653c6eebf79c.jpg?width=300",
    storeId: 4
  },
  {
    id: 10,
    name: "American Teriyaki Subs 15 CM",
    description: "Pan integral con tiras de pechuga de pollo estilo teriyaki, doble porción de queso americano, cebollitas crujientes, lechuga, jitomates, pimientos verdes y aderezo de cebolla dulce.",
    price: 100.00,
    image: "https://cdn.urbanpiper.com/media/bizmedia/2025/05/02/zrqnJ-e928a0b9-25df-4d39-8a5e-7524ae7f0f8e.jpg",
    storeId: 4
  },
  {
    id: 11,
    name: "Combo Frappe Oreo + 3 Timbits",
    description: "Compra un frappé de oreo mediano y 3 timbits a precio especial.",
    price: 80.00,
    image: "https://images.rappi.com.mx/products/2117489881-1746079833481.png?d=300x300&e=webp&q=10",
    storeId: 5
  },
  {
    id: 12,
    name: "Cold Matcha Latte",
    description: "Latte de matcha orgánico a las rocas con un toque de vainilla regular o sugar free.",
    price: 65.00,
    image: "https://images.rappi.com.mx/products/2115493971-1704751444297.png?d=300x300&e=webp&q=10",
    storeId: 5
  },
  {
    id: 13,
    name: "Croissant Salchicha, Huevo y Queso",
    description: "Inigualable sándwich de desayuno con un Croissant esponjoso, calientito y recién horneado con torta de huevo, queso derretido tipo cheddar y salchicha. Ideal para acompañar tu café recién hecho.",
    price: 60.00,
    image: "https://images.rappi.com.mx/products/977566650-1652834918709_hq.jpeg?d=300x300&e=webp&q=10",
    storeId: 5
  },
  {
    id: 14,
    name: "Helado Suave Sencillo Natural",
    description: "Helado de yogurt sabor natural, 120g aprox.",
    price: 75.00,
    image: "https://images.rappi.com.mx/products/tmp1367805663049737501662924023.png?d=300x300&e=webp&q=10",
    storeId: 6
  },
  {
    id: 15,
    name: "Helado Suave Sencillo Maracuyá",
    description: "Helado de yogurt sabor maracuyá, 120g aprox.",
    price: 75.00,
    image: "https://images.rappi.com.mx/products/tmp1421347095512721213230150854.png?d=300x300&e=webp&q=10",
    storeId: 6
  },
  {
    id: 16,
    name: "Helado Suave Doble Natural",
    description: "Helado de yogurt sabor natural, 150g aprox.",
    price: 85.00,
    image: "https://images.rappi.com.mx/products/tmp1421347095512721213230150854.png?d=300x300&e=webp&q=10",
    storeId: 6
  },
  {
    id: 17,
    name: "Helado Suave Doble Maracuyá",
    description: "Helado de yogurt sabor maracuyá, 150g aprox.",
    price: 85.00,
    image: "https://images.rappi.com.mx/products/tmp1421346664027723987781164679.png?d=300x300&e=webp&q=10",
    storeId: 6
  },
  {
    id: 18,
    name: "Ensalada Chica",
    description: "Incluye base de lechuga mixta, 1 proteína, 3 ingredientes de barra fría y 1 aderezo.",
    price: 128.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZLMmK01ttTQPf7Hfew12vY9LmwYPXdg1OnQ&s",
    storeId: 7
  },
  {
    id: 19,
    name: "Ensalada Mediana",
    description: "Incluye base de lechuga mixta, 2 proteínas, 3 ingredientes de barra fría y 1 aderezo.",
    price: 153.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZLMmK01ttTQPf7Hfew12vY9LmwYPXdg1OnQ&s",
    storeId: 7
  },
  {
    id: 20,
    name: "Ensalada Grande",
    description: "Incluye base de lechuga mixta, 2 proteínas, 5 ingredientes de barra fría y 1 aderezo.",
    price: 178.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZLMmK01ttTQPf7Hfew12vY9LmwYPXdg1OnQ&s",
    storeId: 7
  },
  {
    id: 21,
    name: "Chapata de Pollo",
    description: "Incluye mayonesa, chipotle, jitomate, cebolla morada, queso gouda y lechuga + 1 ensalada de acompañamiento (lechuga mixta, 2 ingredientes de barra fría y 1 aderezo). Especificar en comentarios el tipo de pollo a preparar.",
    price: 150.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkdjqfYSmJaHqGqCmNfX_sWAgZlXxsw8E1Vg&s",
    storeId: 7
  },
  {
    id: 22,
    name: "Classic Roll",
    description: "El rollo. El mito. La leyenda.",
    price: 91.00,
    image: "https://cinnabon.mx/wp-content/uploads/2019/01/cinnabon_classic_latte6.jpg",
    storeId: 8
  },
  {
    id: 23,
    name: "Cinnapack cinnabon clásico (2)",
    description: "Cinnapack con 2 rollos clásicos y 2 bebidas de 16 oz.",
    price: 164.00,
    image: "https://cinnabon.mx/wp-content/uploads/2019/01/cinnapacks-1.jpg",
    storeId: 8
  },
  {
    id: 24,
    name: "Cinnapack cinnabon clásico (4)",
    description: "Cinnapack con 4 rollos clásicos y 4 bebidas de 16 oz.",
    price: 328.00,
    image: "https://cinnabon.mx/wp-content/uploads/2019/01/cinnapacks-1.jpg",
    storeId: 8
  },
  {
    id: 25,
    name: "Bubble Tea Mango",
    description: "Té de burbujas base de yogurt sabor mango, 500ml.",
    price: 80.00,
    image: "https://yukapioca.com/static/voissImages/menu/bebidas/base_yogurt/7.png",
    storeId: 9
  },
  {
    id: 26,
    name: "Bubble Tea Lychee",
    description: "Té de burbujas base gourmet sabor lychee, 500ml.",
    price: 95.00,
    image: "https://yukapioca.com/static/voissImages/menu/bebidas/base_gourmet/7.png",
    storeId: 9
  },
  {
    id: 27,
    name: "Bubble Tea Fresa",
    description: "Té de burbujas base de leche sabor melón, 500ml.",
    price: 80.00,
    image: "https://yukapioca.com/static/voissImages/menu/bebidas/base_leche/5.png",
    storeId: 9
  },
  {
    id: 28,
    name: "Bubble Tea Taro",
    description: "Té de burbujas base oriental sabor taro, 500ml.",
    price: 80.00,
    image: "https://yukapioca.com/static/voissImages/menu/bebidas/base_orientales/4.png",
    storeId: 9
  },
  {
    id: 29,
    name: "Hamburguesa Clásica",
    description: "Hamburguesa clásica con lechuga, jitomate y cebolla.",
    price: 120.00,
    image: "https://www.liderempresarial.com/wp-content/uploads/2022/05/Hamburguesas-en-Quere%CC%81taro.jpg",
    storeId: 10
  },
  {
    id: 30,
    name: "Boneless de pollo",
    description: "Boneless de pollo con salsa y aderezo de tu elección.", 
    price: 120.00,
    image: "https://www.recetasnestlecam.com/sites/default/files/srh_recipes/f14d9b7c65adc43c076e137d5ca685f6.jpeg",
    storeId: 10
  },
  {
    id: 31,
    name: "Tacos de arrachera",
    description: "Carne 100% de res con cebolla asada, cilantro y salsa.",
    price: 20.00,
    image: "https://qualisa.com.mx/wp-content/uploads/2024/03/3-2.jpg",
    storeId: 11
  },
  {
    id: 32,
    name: "Tacos campechanos",
    description: "Cecina de res y chorizo artesanal a la parrilla, chicharrón, cebolla asada, cilantro y salsa.",
    price: 20.00,
    image: "https://i.ytimg.com/vi/s1Qe6Wdwxvw/maxresdefault.jpg",
    storeId: 11
  },
  {
    id: 33,
    name: "Empanizado",
    description: "Rollo empanizado con ingrediente de tu elección. Todos los rollos tienen aguacate, pepino y philadelphia. 12 rollos.",
    price: 150.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiSAFscQoZq-A9lPdimG9dvFNpegThW5ae3w&s",
    storeId: 12
  },
  {
    id: 34,
    name: "Emperador",
    description: "Rollo fresco o empanizado, relleno de un ingrediente de tu elección, cubierto de queso gratinado, jalapeño y tocino. Todos los rollos tienen aguacate, pepino y philadelphia. 12 rollos.",
    price: 155.00,
    image: "https://d1ralsognjng37.cloudfront.net/08e8ff37-0cc4-4a8a-ab6e-4a6a44f7dcd4.jpeg",
    storeId: 12
  },
  {
    id: 35,
    name: "Fusion Wok",
    description: "Tallarín, champiñones, espinaca, elote, queso, carne de res, 3 quesos y chipotle.",
    price: 105.00,
    image: "https://tb-static.uber.com/prod/image-proc/processed_images/48230340309ffbf8b6fe04f6b3d327ae/3ac2b39ad528f8c8c5dc77c59abb683d.jpeg",
    storeId: 13
  },
  {
    id: 36,
    name: "Mexican Hot Cheese",
    description: "Penne, mozzarella, zanahoria, elote, carne de res y jalapeño.",
    price: 105.00,
    image: "https://tb-static.uber.com/prod/image-proc/processed_images/48230340309ffbf8b6fe04f6b3d327ae/3ac2b39ad528f8c8c5dc77c59abb683d.jpeg",
    storeId: 13
  },
  {
    id: 37,
    name: "Ono",
    description: "Arroz blanco, pepino, edamames, aguacate, chiles toreados, atun spicy, spicy mayo y cebolla frita.",
    price: 110.00,
    image: "https://static.wixstatic.com/media/670418_3d78bbd0d1b9451ab5d3fdc45e8235c0~mv2_d_5184_3456_s_4_2.jpg/v1/fill/w_320,h_213,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/670418_3d78bbd0d1b9451ab5d3fdc45e8235c0~mv2_d_5184_3456_s_4_2.jpg",
    storeId: 14
  },
  {
    id: 39,
    name: "Maikai",
    description: "Arroz integral, noodles pepino, aguacate, mango, chiles toreados, salmón, thai, cacahuate",
    price: 110.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXVvFbS0laIR-cYWNnlGOxzDz1L_5yTl4Q6Q&s",
    storeId: 14
  },
  {
    id: 40,
    name: "Sandwichote EL LLANO EN LLAMAS",
    description: "NUESTRO SPICY AMIGO.",
    price: 65.00,
    image: "https://m.media-amazon.com/images/I/61q1i7KrMML.jpg",
    storeId: 15
  }
  ,
  {
    id: 41,
    name: "Sandwichote BALDOR",
    description: "NUESTRO VEGAN BEST SELLER.",
    price: 55.00,
    image: "https://img.buzzfeed.com/buzzfeed-static/static/2017-08/16/16/asset/buzzfeed-prod-fastlane-01/sub-buzz-3303-1502915977-1.png?downsize=900:*&output-format=auto&output-quality=auto",
    storeId: 15
  },
  {
    id: 42,
    name: "Sandwichote FRANCIS BACON",
    description: "BACON LETTUCE TOMATO (BLT)",
    price: 65.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPrKs59SeDeQwBM0gYpN3e3_f99qnPOkrCwA&s",
    storeId: 15
  },
  {
    id: 43,
    name: "Orden completa",
    description: "Tortilla frita, queso chihuahua, salsa roja o verde y frijoles. 480 g , 1,171 Kcal.",
    price: 75.00,
    image: "https://tb-static.uber.com/prod/image-proc/processed_images/63993a0df2b83a1e1f888d53c6ac71c9/58f691da9eaef86b0b51f9b2c483fe63.jpeg",
    storeId: 16
  },
  {
    id: 44,
    name: "Media orden",
    description: "Tortilla frita, queso chihuahua, salsa roja o verde y frijoles. 300 g ,586 kcal.",
    price: 55.00,
    image: "https://conecta.tec.mx/sites/default/files/inline-images/chilaquiles-tec.jpg",
    storeId: 16
  },
  {
    id: 45,
    name: "Pizza Margarita",
    description: "Pizza de masa delgada con salsa de jitomate, queso mozzarella y albahaca.",
    price: 150.00,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTY7RbPLpeQGEKr-JMLB6L9kRdCTMtUbFJfJw&s",
    storeId: 17
  },
  {
    id: 46,
    name: "Pizza Pepperoni",
    description: "Pizza de masa delgada con salsa de jitomate, queso mozzarella y pepperoni.",
    price: 150.00,
    image: "https://eu.ooni.com/cdn/shop/articles/pepperoni-pizza_6ac5fa40-65b7-4e3b-a8b9-7ca5ccc05dfd.jpg?crop=center&height=800&v=1737105987&width=800",
    storeId: 17
  }
];

export default products;
INSERT INTO categories (name, emoji, budget) VALUES ('Arriendo','🏠', 500000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Luz','💡', 50000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Agua','🚰', 30000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Gas','🔥', 20000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Gastos comunes','🏢', 40000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Transporte','⛽', 100000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Estadio español','🎾', 30000) ON CONFLICT (name) DO NOTHING;
--INSERT INTO categories (name, emoji, budget) VALUES ('Llacolen','🏊', 50000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Doctor','🩺', 80000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Farmacia','💊', 30000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Internet','🌐', 35000) ON CONFLICT (name) DO NOTHING;
--INSERT INTO categories (name, emoji, budget) VALUES ('Seguro auto','🚗', 60000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Suscripciones','🔁', 40000) ON CONFLICT (name) DO NOTHING;
--INSERT INTO categories (name, emoji, budget) VALUES ('Celular','📱', 30000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Supermercado','🛒', 200000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Gastos Boni','🐶', 50000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Comida afuera','🍽️', 100000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Entretenimiento','🎬', 60000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Ropa y cuidado personal','👕', 80000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Regalos / detalles','🎁', 40000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Otros','📦', 50000) ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji, budget) VALUES ('Gimnasio','🏋️', 50000) ON CONFLICT (name) DO NOTHING;


INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'arriendo' FROM categories WHERE name='Arriendo'
ON CONFLICT (category_id, keyword) DO NOTHING;



INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'enel' FROM categories WHERE name='Luz'
  UNION ALL
  SELECT id, 'luz' FROM categories WHERE name='Luz'
  UNION ALL
  SELECT id, 'electricidad' FROM categories WHERE name='Luz'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'essbio' FROM categories WHERE name='Agua'
  UNION ALL
  SELECT id, 'aguas andinas' FROM categories WHERE name='Agua'
  UNION ALL
  SELECT id, 'agua' FROM categories WHERE name='Agua'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'abastible' FROM categories WHERE name='Gas'
  UNION ALL
  SELECT id, 'lipigas' FROM categories WHERE name='Gas'
  UNION ALL
  SELECT id, 'gas' FROM categories WHERE name='Gas'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'gastos comunes' FROM categories WHERE name='Gastos comunes'
  UNION ALL
  SELECT id, 'edificio' FROM categories WHERE name='Gastos comunes'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'copec' FROM categories WHERE name='Transporte'
  UNION ALL
  SELECT id, 'shell' FROM categories WHERE name='Transporte'
  UNION ALL
  SELECT id, 'terpel' FROM categories WHERE name='Transporte'
  UNION ALL
  SELECT id, 'combustible' FROM categories WHERE name='Transporte'
  UNION ALL
  SELECT id, 'bencina' FROM categories WHERE name='Transporte'
  UNION ALL
  SELECT id, 'uber' FROM categories WHERE name='Transporte'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'estadio español' FROM categories WHERE name='Estadio español'
ON CONFLICT (category_id, keyword) DO NOTHING;

--INSERT INTO category_keywords (category_id, keyword)
--  SELECT id, 'llacolen' FROM categories WHERE name='Llacolen'
--ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'consulta' FROM categories WHERE name='Doctor'
  UNION ALL
  SELECT id, 'isapre' FROM categories WHERE name='Doctor'
  UNION ALL
  SELECT id, 'medico' FROM categories WHERE name='Doctor'
  UNION ALL
  SELECT id, 'examen' FROM categories WHERE name='Doctor'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'cruz verde' FROM categories WHERE name='Farmacia'
  UNION ALL
  SELECT id, 'salcobrand' FROM categories WHERE name='Farmacia'
  UNION ALL
  SELECT id, 'farmacia' FROM categories WHERE name='Farmacia'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'telsur' FROM categories WHERE name='Internet'
  UNION ALL
  SELECT id, 'vtr' FROM categories WHERE name='Internet'
  UNION ALL
  SELECT id, 'entel fibra' FROM categories WHERE name='Internet'
  UNION ALL
  SELECT id, 'internet' FROM categories WHERE name='Internet'
ON CONFLICT (category_id, keyword) DO NOTHING;

--INSERT INTO category_keywords (category_id, keyword)
--  SELECT id, 'seguro auto' FROM categories WHERE name='Seguro auto'
--  UNION ALL
--  SELECT id, 'hdI' FROM categories WHERE name='Seguro auto'
--  UNION ALL
--  SELECT id, 'mapfre' FROM categories WHERE name='Seguro auto'
--  UNION ALL
--  SELECT id, 'seguros falabella' FROM categories WHERE name='Seguro auto'
--ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'netflix' FROM categories WHERE name='Suscripciones'
  UNION ALL
  SELECT id, 'spotify' FROM categories WHERE name='Suscripciones'
  UNION ALL
  SELECT id, 'amazon prime' FROM categories WHERE name='Suscripciones'
  UNION ALL
  SELECT id, 'disney' FROM categories WHERE name='Suscripciones'
  UNION ALL
  SELECT id, 'hbo' FROM categories WHERE name='Suscripciones'
  UNION ALL
  SELECT id, 'chatgpt' FROM categories WHERE name='Suscripciones'
  UNION ALL
  SELECT id, 'copilot' FROM categories WHERE name='Suscripciones'
ON CONFLICT (category_id, keyword) DO NOTHING;

--INSERT INTO category_keywords (category_id, keyword)
--  SELECT id, 'entel' FROM categories WHERE name='Celular'
--  UNION ALL
--  SELECT id, 'claro' FROM categories WHERE name='Celular'
--  UNION ALL
--  SELECT id, 'wom' FROM categories WHERE name='Celular'
--  UNION ALL
--  SELECT id, 'movistar' FROM categories WHERE name='Celular'
--  UNION ALL
--  SELECT id, 'celular' FROM categories WHERE name='Celular'
--ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'lider' FROM categories WHERE name='Supermercado'
  UNION ALL
  SELECT id, 'jumbo' FROM categories WHERE name='Supermercado'
  UNION ALL
  SELECT id, 'tottus' FROM categories WHERE name='Supermercado'
  UNION ALL
  SELECT id, 'unimarc' FROM categories WHERE name='Supermercado'
  UNION ALL
  SELECT id, 'supermercado' FROM categories WHERE name='Supermercado'
  UNION ALL
  SELECT id, 'blasoni' FROM categories WHERE name='Supermercado'
  UNION ALL
  SELECT id, 'emporio agricola' FROM categories WHERE name='Supermercado'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'veterinaria' FROM categories WHERE name='Gastos Boni'
  UNION ALL
  SELECT id, 'veterinario' FROM categories WHERE name='Gastos Boni'
  UNION ALL
  SELECT id, 'boni' FROM categories WHERE name='Gastos Boni'
  UNION ALL
  SELECT id, 'comida boni' FROM categories WHERE name='Gastos Boni'
  UNION ALL
  SELECT id, 'vacunas' FROM categories WHERE name='Gastos Boni'
  UNION ALL
  SELECT id, 'dog chow' FROM categories WHERE name='Gastos Boni'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'mcdonalds' FROM categories WHERE name='Comida afuera'
  UNION ALL
  SELECT id, 'pedidosya' FROM categories WHERE name='Comida afuera'
  UNION ALL
  SELECT id, 'rappi' FROM categories WHERE name='Comida afuera'
  UNION ALL
  SELECT id, 'sushi' FROM categories WHERE name='Comida afuera'
  UNION ALL
  SELECT id, 'restaurante' FROM categories WHERE name='Comida afuera'
  UNION ALL
  SELECT id, 'cafe' FROM categories WHERE name='Comida afuera'
  UNION ALL
  SELECT id, 'uber eats' FROM categories WHERE name='Comida afuera'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'cine' FROM categories WHERE name='Entretenimiento'
  UNION ALL
  SELECT id, 'concierto' FROM categories WHERE name='Entretenimiento'
  UNION ALL
  SELECT id, 'teatro' FROM categories WHERE name='Entretenimiento'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'h&m' FROM categories WHERE name='Ropa y cuidado personal'
  UNION ALL
  SELECT id, 'zara' FROM categories WHERE name='Ropa y cuidado personal'
  UNION ALL
  SELECT id, 'ropa' FROM categories WHERE name='Ropa y cuidado personal'
  UNION ALL
  SELECT id, 'falabella' FROM categories WHERE name='Ropa y cuidado personal'
  UNION ALL
  SELECT id, 'perfume' FROM categories WHERE name='Ropa y cuidado personal'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'regalo' FROM categories WHERE name='Regalos / detalles'
  UNION ALL
  SELECT id, 'detalle' FROM categories WHERE name='Regalos / detalles'
  UNION ALL
  SELECT id, 'floreria' FROM categories WHERE name='Regalos / detalles'
  UNION ALL
  SELECT id, 'chocolates' FROM categories WHERE name='Regalos / detalles'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'otros' FROM categories WHERE name='Otros'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'proteina' FROM categories WHERE name='Gimnasio'
  UNION ALL
  SELECT id, 'creatina' FROM categories WHERE name='Gimnasio'
  UNION ALL
  SELECT id, 'felipe coach' FROM categories WHERE name='Gimnasio'
  UNION ALL
  SELECT id, 'gimnasio' FROM categories WHERE name='Gimnasio'
  UNION ALL
  SELECT id, 'gym' FROM categories WHERE name='Gimnasio'
ON CONFLICT (category_id, keyword) DO NOTHING;
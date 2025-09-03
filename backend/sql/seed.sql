INSERT INTO categories (name, emoji) VALUES ('Arriendo','🏠') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Luz','💡') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Agua','🚰') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Gas','🔥') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Gastos comunes','🏢') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Combustible','⛽') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Estadio español','🎾') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Llacolen','🏊') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Salud (Médico)','🩺') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Farmacia','💊') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Internet','🌐') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Seguro auto','🚗') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Suscripciones','🔁') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Celular','📱') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Supermercado','🛒') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Gastos Boni','🐶') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Comida afuera','🍽️') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Entretenimiento','🎬') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Ropa y cuidado personal','👕') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Regalos / detalles','🎁') ON CONFLICT (name) DO NOTHING;
INSERT INTO categories (name, emoji) VALUES ('Otros','📦') ON CONFLICT (name) DO NOTHING;

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
  SELECT id, 'copec' FROM categories WHERE name='Combustible'
  UNION ALL
  SELECT id, 'shell' FROM categories WHERE name='Combustible'
  UNION ALL
  SELECT id, 'terpel' FROM categories WHERE name='Combustible'
  UNION ALL
  SELECT id, 'combustible' FROM categories WHERE name='Combustible'
  UNION ALL
  SELECT id, 'bencina' FROM categories WHERE name='Combustible'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'estadio español' FROM categories WHERE name='Estadio español'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'llacolen' FROM categories WHERE name='Llacolen'
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'consulta' FROM categories WHERE name='Salud (Médico)'
  UNION ALL
  SELECT id, 'isapre' FROM categories WHERE name='Salud (Médico)'
  UNION ALL
  SELECT id, 'medico' FROM categories WHERE name='Salud (Médico)'
  UNION ALL
  SELECT id, 'examen' FROM categories WHERE name='Salud (Médico)'
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

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'seguro auto' FROM categories WHERE name='Seguro auto'
  UNION ALL
  SELECT id, 'hdI' FROM categories WHERE name='Seguro auto'
  UNION ALL
  SELECT id, 'mapfre' FROM categories WHERE name='Seguro auto'
  UNION ALL
  SELECT id, 'seguros falabella' FROM categories WHERE name='Seguro auto'
ON CONFLICT (category_id, keyword) DO NOTHING;

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
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'entel' FROM categories WHERE name='Celular'
  UNION ALL
  SELECT id, 'claro' FROM categories WHERE name='Celular'
  UNION ALL
  SELECT id, 'wom' FROM categories WHERE name='Celular'
  UNION ALL
  SELECT id, 'movistar' FROM categories WHERE name='Celular'
  UNION ALL
  SELECT id, 'celular' FROM categories WHERE name='Celular'
ON CONFLICT (category_id, keyword) DO NOTHING;

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
ON CONFLICT (category_id, keyword) DO NOTHING;

INSERT INTO category_keywords (category_id, keyword)
  SELECT id, 'veterinaria' FROM categories WHERE name='Gastos Boni'
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

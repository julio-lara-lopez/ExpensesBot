INSERT OR IGNORE INTO categories (name, emoji) VALUES
  ('Arriendo','🏠'),
  ('Luz','💡'),
  ('Agua','🚰'),
  ('Gas','🔥'),
  ('Gastos comunes','🏢'),
  ('Combustible','⛽'),
  ('Estadio español','🎾'),
  ('Llacolen','🏊'),
  ('Salud (Médico)','🩺'),
  ('Farmacia','💊'),
  ('Internet','🌐'),
  ('Seguro auto','🚗'),
  ('Suscripciones','🔁'),
  ('Celular','📱'),
  ('Supermercado','🛒'),
  ('Gastos Boni','🐶'),
  ('Comida afuera','🍽️'),
  ('Entretenimiento','🎬'),
  ('Ropa y cuidado personal','👕'),
  ('Regalos / detalles','🎁'),
  ('Otros','📦');

-- Luz
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('enel'),('luz'),('electricidad'))
  WHERE name='Luz';

-- Agua
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('essbio'),('aguas andinas'),('agua'))
  WHERE name='Agua';

-- Gas
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('abastible'),('lipigas'),('gas'))
  WHERE name='Gas';

-- Gastos comunes
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('gastos comunes'),('edificio'))
  WHERE name='Gastos comunes';

-- Combustible
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('copec'),('shell'),('terpel'),('combustible'),('bencina'))
  WHERE name='Combustible';

-- Estadio español
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('estadio español'))
  WHERE name='Estadio español';

-- Llacolen
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('llacolen'))
  WHERE name='Llacolen';

-- Salud (Médico)
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('consulta'),('isapre'),('medico'),('examen'))
  WHERE name='Salud (Médico)';

-- Farmacia
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('cruz verde'),('salcobrand'),('farmacia'))
  WHERE name='Farmacia';

-- Internet
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('telsur'),('vtr'),('entel fibra'),('internet'))
  WHERE name='Internet';

-- Seguro auto
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('seguro auto'),('hdI'),('mapfre'),('seguros falabella'))
  WHERE name='Seguro auto';

-- Suscripciones
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('netflix'),('spotify'),('amazon prime'),('disney'),('hbo'))
  WHERE name='Suscripciones';

-- Celular
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('entel'),('claro'),('wom'),('movistar'),('celular'))
  WHERE name='Celular';

-- Supermercado
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('lider'),('jumbo'),('tottus'),('unimarc'),('supermercado'))
  WHERE name='Supermercado';

-- Gastos Boni
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('veterinaria'),('comida boni'),('vacunas'),('dog chow'))
  WHERE name='Gastos Boni';

-- Comida afuera
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('mcdonalds'),('pedidosya'),('rappi'),('sushi'),('restaurante'))
  WHERE name='Comida afuera';

-- Entretenimiento
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('cine'),('concierto'),('teatro'))
  WHERE name='Entretenimiento';

-- Ropa y cuidado personal
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('h&m'),('zara'),('ropa'),('falabella'),('perfume'))
  WHERE name='Ropa y cuidado personal';

-- Regalos / detalles
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('regalo'),('detalle'),('floreria'),('chocolates'))
  WHERE name='Regalos / detalles';

-- Otros
INSERT INTO category_keywords (category_id, keyword)
  SELECT id, kw FROM categories, (VALUES ('otros'))
  WHERE name='Otros';

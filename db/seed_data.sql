-- Seed sample users
INSERT INTO users (id, email, password_hash, eco_score) VALUES
(1, 'user1@example.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 85.5),
(2, 'user2@example.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 72.3),
(3, 'admin@example.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 90.0);

-- Seed sample stations (these will be replaced by OCM data)
INSERT INTO stations (id, name, latitude, longitude, energy_type, available) VALUES
(1, 'Downtown Charging Station', 37.7749, -122.4194, 'Level 2', true),
(2, 'Mall Parking Garage', 37.7849, -122.4094, 'DC Fast', false),
(3, 'Airport Terminal A', 37.7949, -122.3994, 'Level 2', true),
(4, 'Shopping Center', 37.8049, -122.3894, 'Level 1', true),
(5, 'Office Building', 37.8149, -122.3794, 'DC Fast', true);

-- Seed sample sessions
INSERT INTO sessions (user_id, station_id, timestamp) VALUES
(1, 1, '2024-01-15 10:30:00'),
(1, 3, '2024-01-16 14:20:00'),
(2, 2, '2024-01-15 09:15:00'),
(2, 4, '2024-01-17 16:45:00'),
(3, 5, '2024-01-18 11:00:00'); 